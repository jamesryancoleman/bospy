from bospy import common_pb2_grpc, common_pb2
import grpc
import os

envVars:dict[str,str]
args:list[str] = []
kwargs:dict[str, str] = {}

SCHEDULER_ADDR = os.environ.get('SCHEDULER_ADDR')
if SCHEDULER_ADDR is None:
    # apply default
    SCHEDULER_ADDR = "localhost:2824"

# client calls
def Run(image:str, *args, envVars:dict[str, str]=None, **kwargs) -> common_pb2.RunResponse:
    print("image:", image)
    print("args:", args)
    print("envVars:", envVars)
    print("kwargs:", kwargs)
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