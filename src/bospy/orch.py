from bospy.config import get_orchestrator_addr
from bospy import common_pb2_grpc, common_pb2
import grpc

def run(image:str, *args, envVars:dict[str, str]=None, timeout=0, **_kwargs) -> common_pb2.RunResponse:
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
    if len(_kwargs) > 0:
        for k, v in _kwargs:
            _kwargs[k] = str(v)
            print(f'{k} {type(k)} {v} {type(v)}')
    
    envVars = {k: str(v) for k, v in envVars.items()}

    response: common_pb2.RunResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
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

def get_running_apps() -> dict[int, str]:
    """
    Docstring for get_running_apps
    
    :return: returns a dictionary of running jobs. Keys are txn ids and values
    are the container uuids.
    :rtype: dict[int, str]
    """
    resp: common_pb2.RunningJobsResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.RunningJobs(common_pb2.RunningJobsRequest(
            Header=common_pb2.Header(),
        ))
    return {k: v for k, v in resp.jobs.items()}

def stop_apps(txns:list[int]):
    resp: common_pb2.StopResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.Stop(common_pb2.StopRequest(
            header=common_pb2.Header(),
            txns=txns,
        ))
    return resp
