from bospy import common_pb2_grpc, common_pb2
import grpc
import os

envVars:dict[str,str]
args:list[str] = []
kwargs:dict[str, str] = {}

SCHEDULER_ADDR = os.environ.get('SCHEDULER_ADDR', "localhost:2824")

# client calls
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
    pairs:list[common_pb2.SetPair] = []
    hash_key = _kwargs.get("__key__")
    if hash_key is not None:
        pairs.append(common_pb2.SetPair(Key="__key__", Value='output'))
    for i, _ in enumerate(_args):
        pairs.append(common_pb2.SetPair(Key="${}".format(i+1), Value=str(_args[i])))
        i+=1
    
    for k, v in _kwargs.items():
        pairs.append(common_pb2.SetPair(Key=k, Value=str(v)))
    
    txn_id = int(kwargs.get('txn_id'), 0)
    session_token = kwargs.get('session_token')
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


def LoadInput(previous_session_token:str|list[str]) -> dict[str,str]:
    """ Load results is used to get the output of a previous container execution.
        A session token is uniquely defined for a given transaction, flow, and node.
        
        If a new transaction wants to load results from a previous call to the
        same flow the Scheduler must have retained the session details and passed 
        them to the next invocation of that flow.

        What the current node needs is a "pointer" to the the flow and node the 
        current node wanted to load the output of. The session token is accepted
        in lieu of the transaction id.

        The pointer will look like '<TXN>.<FLOW>.<NODE>:<KEY>[/<FIELD>]'. The 
        scheduler will only confirm that there exists a valid session token 
        matching the flow and node.        
    """
    
    

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
    """ returns a typed version of the global variable with the provided key.
    """
    



# container management functions 
def LoadArgs():
    # collect all the args
    i = 1
    while True:
        try:
            arg = os.environ.pop("arg:{}".format(i))
            args.append(arg)
            i += 1
        except KeyError:
            break

def LoadKwargs():
    # collect all the args
    for k, v in os.environ.items():
        if "kwarg:" in k:
            kwargs[k[6:]] = os.environ.pop(k)

def LoadEnv():
    LoadArgs()
    LoadKwargs()

LoadEnv()