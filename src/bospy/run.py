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
TXN = os.environ.get('TXN_ID', 0)
FLOW = os.environ.get('FLOW_ID', 0)
NODE = os.environ.get('NODE_ID', 0)

DEFAULT_TOKEN = "000000000000"

# used write output from this transaction
WRITE_TOKEN = os.environ.get('WRITE_TOKEN', DEFAULT_TOKEN)

# used to load output from the previous instantiations of this FLOW
READ_TOKEN = os.environ.get('READ_TOKEN', DEFAULT_TOKEN)

positionRe = re.compile('^\\$(?P<position>[0-9]+)$')

# client calls
def Get(keys:list[str], infer_type=True, token:str=None) -> dict[str,Any]:
    if token is None:
        token = WRITE_TOKEN

    response: common_pb2.GetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        header = common_pb2.Header(Src="python_client", Dst=SCHEDULER_ADDR, SessionToken=token)
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Get(common_pb2.GetRequest(
            Header=header,
            Keys=keys,
        ))
        if response.Error > 0:
            print("error:", response.Error, ", errorMsg:", response.ErrorMsg)

    values:dict={}
    for p in response.Pairs:
        v:int|float|bool|str
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

def Return(*_args, **_kwargs) -> common_pb2.SetResponse:
    """ Return exposes all positional and keywork arguments provided to shared
        memory in the BOS.

        Exposing variables requires a valid transaction number and session 
        token. These are typically set automatically by the BOS Scheduler when
        it starts the container but these may be overwritten with:
            kwarg['txn_id'] = TXN_ID
            kwarg['session_token'] = SESSION_TOKEN
    """
    pairs:list[common_pb2.SetPair] = []
    hash_key = _kwargs.get("__key__")
    if hash_key is not None:
        pairs.append(common_pb2.SetPair(Key="__key__", Value='output'))
    for i, _ in enumerate(_args):
        pairs.append(common_pb2.SetPair(Key="${}".format(i+1), Value=str(_args[i])))
        i+=1
    
    for k, v in _kwargs.items():
        pairs.append(common_pb2.SetPair(Key=k, Value=str(v)))
    
    # the default txn_id of 0 and token of 000000000000 will succeed
    txn_id = int(kwargs.get('txn_id', 0))
    session_token = kwargs.get('session_token', "000000000000")
    print("Return - txn: {}, session_id: {}".format(txn_id, session_token))
    header = common_pb2.Header(
                TxnId=txn_id,
                SessionToken=session_token
            )
    print("trying to write return values to scheduler at {}".format(SCHEDULER_ADDR))
    print("txn id: {}, token: '{}'".format(header.TxnId, header.SessionToken))
    print("pairs:")
    for p in pairs:
        print(p.Key, "->", p.Value)
    
    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Set(common_pb2.SetRequest(
            Header=header,
            Pairs=pairs,
        ))
    print("error:", response.Error, ", errMsg:",response.ErrorMsg)
    return response


def LoadInput(last_call:bool=False, node:int=-1) -> dict[str,str]:
    """ Load results is used to get the output of a previous container execution.
        
        If node <= -1, the target node if assumed to be the current NODE
        from the last transaction through this FLOW.

        If last_call is True, LoadInput() attempts to access the last output of 
        the from_node of this FLOW.

        In the future we'll add support for other FLOW
    """
    call:str="THIS" # for debug
    session_token:str=CURRENT_TOKEN
    if last_call:
        session_token = FLOW_TOKEN
        call = "LAST"        

    if node < 0:
        node = NODE

    print("requesting output of node {} from {} call of flow {} with session token '{}'".format(
        NODE, call, FLOW, session_token))

    header = common_pb2.Header(Src="python_client", Dst=SCHEDULER_ADDR,
                                SessionToken=session_token)

    # call the Get method of the Scheduler services
    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        # When no Pairs are set all variables are returned if the token is valid
        stub = common_pb2_grpc.ScheduleStub(channel)
        response = stub.Get(common_pb2.GetRequest(
            Header=header,
        ))
        print("error:", response.Error, ", errMsg:",response.ErrorMsg)
        if response.Error != common_pb2.ServiceError.SERVICE_ERROR_NONE:
            return {}
        
        # parse values and add to run.args and run.kwargs\
    

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

    return s



def GetGlobal(key:str, infer_type=True) -> (int|float|bool|str):
    """ returns the global variable with the key provided, if it exists.
        By default GetGlobal returns a typed version of the value.
    """
    

def LoadInput(values:dict[str,str]=None) -> tuple[list[str], dict[str,str]]|None:
    # otherwise clear out any default values and populate from the provided dict
    positional_dict:dict[int, str] = {}
    remaining_kwargs = values.copy()
    for k, v in values.items():
        m = positionRe.match(k)
        if m is not None:
            positional_dict[int(m.group('position'))] = v
            remaining_kwargs.pop(k)
        # else:
        #     print("'{}' did not match the positional argument pattern".format(k))
    
    args = [None] * len(positional_dict)
    for i, v in positional_dict.items():
        args[i-1] = v
    return args, remaining_kwargs

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
    try:
        TXN = os.environ.pop("TXN_ID")
        TXN = int(TXN)
    except KeyError:
        TXN = 0
        
    try:
        FLOW = os.environ.pop("FLOW_ID")
        FLOW = int(FLOW)
    except KeyError:
        FLOW = 0

    try:
        NODE = os.environ.pop("NODE_ID")
        NODE = int(NODE)
    except KeyError:
        NODE = 0        
            
    LoadArgs()
    LoadKwargs()

LoadEnv()