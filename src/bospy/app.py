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
DEFAULT_TOKEN = ""

# used write output from this transaction
TOKEN = os.environ.get('TOKEN', DEFAULT_TOKEN)

OUTPUT_HASH = "OUTPUT"

keyRe = re.compile(r"^(?:(?P<ns>[a-zA-Z0-9\/\-\/.]+):)?(?:(?P<scope>[^:]*):)?(?:(?P<txn>[0-9]+):)?(?P<key>[^\/\n\r]+)(\/)?(?:(\$)?(?P<field>[^\/\n\r]+))?")
scopeRe = re.compile(r"^(?P<flow>[0-9]+)(?:\.(?P<node>[0-9]+))?")
positionRe = re.compile(r'^\\$(?P<position>[0-9]+)$')

# client calls
def Get(keys:str|list[str], infer_type=True, token:str=None, txn:int=0) -> dict[str,Any]:
    """
    Passing no namespace implies flows. Keys returned from the server have their 
    scopes and txns removed so the returned keys are NS:KEY.
    
    :param keys: Description
    :type keys: str | list[str]
    :param infer_type: Description
    :param token: Description
    :type token: str
    :param txn: Description
    :type txn: int
    :return: Description
    :rtype: dict[str, Any]
    """
    if isinstance(keys, str):
        keys = [keys]
    if token is None:
        token = kwargs["TOKEN"]
    if txn==0:
        txn = int(kwargs.get('TXN_ID', 0))

    response: common_pb2.GetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        header = common_pb2.Header(Src="python_client",
                                   Dst=SCHEDULER_ADDR, 
                                   SessionToken=token,
                                   TxnId=txn)
        if app := kwargs.get("APP"):
            header.app = app
        stub = common_pb2_grpc.SchedulerStub(channel)
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


def Run(image:str, *args, envVars:dict[str, str]=None, timeout=0, **_kwargs) -> common_pb2.RunResponse:
    """
    Docstring for Run
    
    :param image: Description
    :type image: str
    :param args: Description
    :param envVars: Description
    :type envVars: dict[str, str]
    :param timeout: -1 = return immediately, 0 = wait forever, >= 1 wait timeout seconds
    :param kwargs: Description
    :return: Description
    :rtype: RunResponse
    """
    # global DEFAULT_SESSION_ACTIVE, kwargs
    # if DEFAULT_SESSION_ACTIVE:
    #     if envVars is None:
    #         envVars = {}
    #     envVars = envVars | {
    #         "TXN_ID": str(kwargs["TXN_ID"]),
    #         "TOKEN": str(kwargs["TOKEN"]),
    #     }
    if len(_kwargs) > 0:
        for k, v in _kwargs:
            _kwargs[k] = str(v)
            print(f'{k} {type(k)} {v} {type(v)}')
    
    # print(f'the type of kwargs is {type(_kwargs)}')
    # print(f'the type of envVArs is {type(envVars)}')

    response: common_pb2.RunResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        response = stub.Run(common_pb2.RunRequest(
            Image=image, 
            EnvVars=envVars,
            Args=args,
            Kwargs=_kwargs,
            Timeout=timeout,
        ))
        if response.ExitCode > 0:
            print("scheduler.Run error:", response.ErrorMsg)
    
    return response

def Set(pairs:str|dict[str,Any], value:Any|None=None) -> common_pb2.SetResponse:
    """ Set writes the a dictionary of keys and values to the subnamespace
        allocated to this flow.
    """
    # TODO: decide how to make a Set request use the global name space. Cannot 
    # use the global kwarg because it is protected in python. Should users have
    # to prepend this explicitly? This already is supported as of 11/20/2025. 
    if isinstance(pairs, str) and value is not None:
        pairs = {pairs: value}
    if not isinstance(pairs, dict):
        print(f"set error: pairs not a str or dict (type={type(pairs)})")
        return None
    txn = int(kwargs.get('TXN_ID', 0))
    token = kwargs.get('TOKEN', DEFAULT_TOKEN)

    setPairs:list[common_pb2.SetPair] = [None] * len(pairs)
    for i, k in enumerate(pairs):
        v = pairs[k]
        setPairs[i] = common_pb2.SetPair(Key=k, Value=str(v))

    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        header = common_pb2.Header(TxnId=txn, SessionToken=token)
        if app := kwargs.get("APP"):
            header.app = app
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


def LoadInput(*keys:str, app:str=None, token:str=None, txn:int=None) -> tuple[list[str], dict[str,Any]]:
    """ Load results is used to get the output of a previous container execution.
    """
    if app is None:
        app_name = kwargs["IMAGE"]
    if token is None:
        token = kwargs["TOKEN"]
    if txn is None:
        txn = kwargs["TXN_ID"]
    if len(keys) == 0:
        keys = ["OUTPUT/"]

    print("requesting output of app {} with token '{}'".format(app_name, token))
    print(keys)

    header = common_pb2.Header(SessionToken=token, Src="python_client", Dst=SCHEDULER_ADDR)

    # call the Get method of the Scheduler services
    response:common_pb2.SetResponse
    with grpc.insecure_channel(SCHEDULER_ADDR) as channel:
        # When no Pairs are set all variables are returned if the token is valid
        stub = common_pb2_grpc.SchedulerStub(channel)
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


def SetAppName(name:str):
    """
    ** testing only ** This manually sets the app name. Only applies to test apps
    writing to the "tmp" namespace. This will be overridden if call in a production app.
    
    :param image: Description
    :type image: str
    """
    APP = name
    kwargs["IMAGE"] = APP

def LoadEnv():      
    APP = os.environ.pop("IMAGE", "")
    kwargs["IMAGE"] = APP

    TXN = int(os.environ.pop("TXN_ID", 0))
    kwargs["TXN_ID"] = TXN
    
    # TOKEN = os.environ.pop('READ_TOKEN', DEFAULT_TOKEN)
    TOKEN = os.environ.pop('TOKEN', DEFAULT_TOKEN)
    kwargs["TOKEN"] = TOKEN
    # kwargs["READ_TOKEN"] = READ_TOKEN
    LoadArgs()
    LoadKwargs()

LoadEnv()
# print(kwargs)