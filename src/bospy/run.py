from bospy import common_pb2_grpc, common_pb2
from typing import Any
import grpc
import os
import re

envVars:dict[str,str]
args:list[str] = []
kwargs:dict[str, str] = {}

SCHEDULER_ADDR = os.environ.get('SCHEDULER_ADDR', "localhost:2824")

# values will be set by the Scheduler and are constant for lifetime of a container
NS:str = os.environ.get('NS', "flows")
TXN = os.environ.get('TXN_ID', 0)
FLOW = os.environ.get('FLOW_ID', 0)
NODE = os.environ.get('NODE_ID', 0)
DEFAULT_TOKEN = "000000000000"

# used write output from this transaction
WRITE_TOKEN = os.environ.get('WRITE_TOKEN', DEFAULT_TOKEN)

# used to load output from the previous instantiations of this FLOW
READ_TOKEN = os.environ.get('READ_TOKEN', DEFAULT_TOKEN)

OUTPUT_HASH = "OUTPUT"

keyRe = re.compile(r"^(?:(?P<ns>[a-zA-Z0-9\/\-\/.]+):)?(?:(?P<scope>[^:]*):)?(?:(?P<txn>[0-9]+):)?(?P<key>[^\/\n\r]+)(\/)?(?:(\$)?(?P<field>[^\/\n\r]+))?")
scopeRe = re.compile(r"^(?P<flow>[0-9]+)(?:\.(?P<node>[0-9]+))?")
positionRe = re.compile(r'^\\$(?P<position>[0-9]+)$')

def CreateDefaultRWSession():
    kwargs["FLOW_ID"] = 9
    kwargs["NODE_ID"] = 8
    kwargs["TXN_ID"] = 7
    kwargs["WRITE_TOKEN"] = "1234567890ab"
    kwargs["READ_TOKEN"] = kwargs["WRITE_TOKEN"]
    print(kwargs)

class Key:
    def __init__(self, key:str, field:str|None=None, isHash:bool=False, ns:str=NS):
        self.ns = ns
        self.flow = kwargs["FLOW_ID"]
        self.node = kwargs["NODE_ID"]
        self.txn = kwargs["TXN_ID"]

        self.key:str = key
        self.field = None
        self.isHash = isHash
        self.isPositional = False

        if field is not None:
            self.field = field
            self.isHash = True

    def StrFmt(self, scope:bool=True, txn:bool=False, field:bool=False) -> str:
        s:str = self.ns + ":"
        if self.ns == NS and scope:
            s += "{}.{}:".format(self.flow, self.node) 
        if txn and self.txn != 0:
            s += "{}:".format(self.txn)
        s += self.key
        if self.isHash:
            s += "/"
            if self.field is not None:
                s += self.field
        return s
    
    def __str__(self):
        return self.StrFmt()
    
def ParseKey(s:str) -> Key|None:
    match = keyRe.match(s)
    if match:
        m = match.groups()
        if m[3]:
            k=Key(m[3])
            if m[0]:
                k.ns = m[0]
            if m[1]:
                scope = m[1]
                match_scope = scopeRe.match(scope)
                if match_scope:
                    ms = match_scope.groups()
                    k.flow = int(ms[0])
                    if ms[1]:
                        k.node = int(ms[1])
            if m[4]:
                k.isHash = True
            if m[5]:
                k.isPositional = True
                if m[6]:
                    k.field = m[5]+m[6]
            elif m[6]:
                k.field = m[6] 
            return k          
        else:
            return None
    return None        


# client calls
def Get(keys:str|list[str], infer_type=True, token:str=None) -> dict[str,Any]:
    if isinstance(keys, str):
        keys = [keys]
    if token is None:
        token = kwargs["READ_TOKEN"]

    for i, key in enumerate(keys):
        k = ParseKey(key)
        keys[i] = k.__str__()

    response: common_pb2.GetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        header = common_pb2.Header(Src="python_client", Dst=SCHEDULER_ADDR, 
                                   SessionToken=token)
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Get(common_pb2.GetRequest(
            Header=header,
            Keys=keys,
        ))
        if response.Error > 0:
            print("error:", response.Error, ", errorMsg:", response.ErrorMsg)

    values:dict={}
    for p in response.Pairs:
        v:int|float|bool|str|None
        if infer_type:
            v = InferType(p.Value)
        values[p.Key] = v

    return values


def Run(image:str, *args, envVars:dict[str, str]=None, **kwargs) -> common_pb2.RunResponse:
    response: common_pb2.RunResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Run(common_pb2.RunRequest(
            Image=image, 
            EnvVars=envVars,
            Args=args,
            Kwargs=kwargs,
        ))
        if response.ExitCode > 0:
            print("scheduler.Run error:", response.ErrorMsg)
    
    return response

def Set(pairs:str|dict[str,Any], value:Any|None=None) -> common_pb2.SetResponse:
    """ Set writes the a dictionary of keys and values to the subnamespace
        allocated to this flow.
    """
    if isinstance(pairs, str) and value is not None:
        pairs = {pairs: value}
    if not isinstance(pairs, dict):
        print(f"set error: pairs not a str or dict (type={type(pairs)})")
        return None
    txn = int(kwargs.get('TXN_ID', 0))
    token = kwargs.get('WRITE_TOKEN', DEFAULT_TOKEN)

    setPairs:list[common_pb2.SetPair] = [None] * len(pairs)
    for i, k in enumerate(pairs):
        v = pairs[k]
        setPairs[i] = common_pb2.SetPair(Key=k, Value=str(v))

    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        stub = common_pb2_grpc.ScheduleStub(channel)
        header = common_pb2.Header(TxnId=txn, SessionToken=token)
        response = stub.Set(common_pb2.SetRequest(
            Header=header,
            Pairs=setPairs,
        ))
    if response.Error > 0:
        print("error:", response.Error, ", errMsg:",response.ErrorMsg)
    return response

def Return(*_args, **_kwargs) -> common_pb2.SetResponse:
    """ Return exposes all positional and keywork arguments provided to shared
        memory in the BOS.

        Exposing variables requires a valid transaction number and session 
        token. These are typically set automatically by the BOS Scheduler when
        it starts the container but these may be overwritten with:
            kwarg['txn_id'] = TXN_ID
            kwarg['session_token'] = SESSION_TOKEN
    """
    _kwargs = {f"{OUTPUT_HASH}/{k}":v for k,v in _kwargs.items()}
    for i, arg in enumerate(_args):
        # key = ParseKey("{}/${}".format(OUTPUT_HASH, i+1))
        # pairs.append(common_pb2.SetPair(Key=key.__str__(), Value=str(_args[i])))
        _kwargs[f"{OUTPUT_HASH}/${i+1}"] = arg
    return Set(_kwargs)


def LoadInput(*keys:str, flow:int=None, node:int=None, token:str=None, txn:int=None) -> tuple[list[str], dict[str,Any]]:
    """ Load results is used to get the output of a previous container execution.

        If flow is not passed, flow is assumed to be THIS flow.
        If node is not passed, node is assumed to be THIS node.
    """
    if flow is None:
        flow = kwargs["FLOW_ID"]
    if node is None:
        node = kwargs["NODE_ID"]
    if token is None:
        token = kwargs["READ_TOKEN"]
    if txn is None:
        txn = kwargs["TXN_ID"]
    if len(keys) == 0:
        keys = [Key("OUTPUT", isHash=True).__str__()]

    print("requesting output of flow {} node {} with read token '{}'".format(
        flow, node, token))
    print(keys)

    header = common_pb2.Header(SessionToken=token, Src="python_client", Dst=SCHEDULER_ADDR)

    # call the Get method of the Scheduler services
    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        # When no Pairs are set all variables are returned if the token is valid
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Get(common_pb2.GetRequest(
            Header=header,
            Keys=keys,
        ))
        print("error:", response.Error, ", errMsg:",response.ErrorMsg)
        if response.Error != common_pb2.ServiceError.SERVICE_ERROR_NONE:
            return {}

        print(response.Pairs)
        if len(response.Pairs) > 0:
            _args_dict = {}
            _kwargs = {}
            for p in response.Pairs:
                m = positionRe.match(p.Key)
                if m is None:
                    # found a kwarg
                    _kwargs[p.Key] = p.Value
                else:
                    # found a positional int
                    i = int(m.group("position"))
                    _args_dict[i] = p.Value
            
            _args = [None] * len(_args_dict)
            for i, v in _args_dict.items():
                _args[i] = v
            return _args, _kwargs


def InferType(s:str) -> (int|float|bool|str):
    """ InferType takes a str typed value and converts to an int, float, bool,
        or falls back on str.
    """
    try:
        typed = int(s)
        return typed
    except ValueError:
        pass
    try:
        typed = float(s)
        return typed
    except ValueError:
        pass

    if s.lower() == "true":
        typed = True
        return typed
    elif s.lower() == "false":
        typed = False
        return typed
    
    if s == "":
        return None

    return s

# def GetGlobal(key:str, infer_type=True) -> (int|float|bool|str):
#     """ returns the global variable with the key provided, if it exists.
#         By default GetGlobal returns a typed version of the value.
#     """
    

# container management functions 
def LoadArgs(values:dict[str,str]=None) -> list[str]|None:
    if values is None:
        # populate args from the OS environment
        i = 1
        while True:
            try:
                arg = os.environ.pop("arg:{}".format(i))
                args.append(arg)
                i += 1
            except KeyError:
                break
        return
        

def LoadKwargs(values:dict[str,str]=None):
    # collect all the args
    for k, v in os.environ.items():
        if "kwarg:" in k:
            kwargs[k[6:]] = os.environ.pop(k)

def LoadEnv():      
    FLOW = int(os.environ.pop("FLOW_ID", 0))
    kwargs["FLOW_ID"] = FLOW

    NODE = int(os.environ.pop("NODE_ID", 0))
    kwargs["NODE_ID"] = NODE

    TXN = int(os.environ.pop("TXN_ID", 0))
    kwargs["TXN_ID"] = TXN
    
    WRITE_TOKEN = os.environ.pop('WRITE_TOKEN', DEFAULT_TOKEN)
    READ_TOKEN = os.environ.pop('READ_TOKEN', DEFAULT_TOKEN)
    kwargs["WRITE_TOKEN"] = WRITE_TOKEN
    kwargs["READ_TOKEN"] = READ_TOKEN
    LoadArgs()
    LoadKwargs()

LoadEnv()
print(kwargs)