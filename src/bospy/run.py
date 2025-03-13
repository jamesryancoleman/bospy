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