from bospy.config import get_orchestrator_addr
from bospy import common_pb2_grpc, common_pb2
import grpc

def run(app:str, *args, envVars:dict[str, str]=None, timeout=0, **_kwargs) -> common_pb2.RunResponse:
    """
    Docstring for Run
    
    :param app: Description
    :type app: str
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
    args = [str(a) for a in args]
    if envVars is not None:
        envVars = {k: str(v) for k, v in envVars.items()}

    response: common_pb2.RunResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        response = stub.Run(common_pb2.RunRequest(
            Image=app,
            EnvVars=envVars,
            Args=args,
            Kwargs=_kwargs,
            Timeout=timeout,
        ))
        if response.ExitCode > 0:
            print("scheduler.Run error:", response.ErrorMsg)
    
    return response

def schedule(app:str, schedule_str:str, on_start:bool=False, *args, envVars:dict[str, str]=None, **_kwargs):
    """
    Docstring for schedule
    
    :param app: name of app to run (image)
    :type app: str
    :param schedule_str: the cron string or timestamp (ISO 8601) the job should be run at.
    :type schedule_str: str
    :param on_start: Description
    :type on_start: bool
    :param args: Description
    :param envVars: Description
    :type envVars: dict[str, str]
    :param _kwargs: Description
    """
    if len(_kwargs) > 0:
        for k, v in _kwargs:
            _kwargs[k] = str(v)
            print(f'{k} {type(k)} {v} {type(v)}')
    args = [str(a) for a in args]
    if envVars is not None:
        envVars = {k: str(v) for k, v in envVars.items()}

    resp: common_pb2.CronResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.RegisterCron(common_pb2.CronRequest(
            CronStr=schedule_str,
            OnStart=on_start,
            Requests=[common_pb2.RunRequest(
                Image=app,
                Args=args,
                Kwargs=_kwargs,
                EnvVars=envVars,
            )]
        ))
    return resp

def get_running_apps() -> list[common_pb2.JobData]:
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
    return resp.jobs

def get_scheduled_apps() -> list[common_pb2.JobData]:
    """
    Docstring for get_scheduled_apps
    
    :return: Description
    :rtype: list[JobData]
    """
    resp : common_pb2.RunningJobsResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.CronTable(common_pb2.RunningJobsRequest())
    return resp.jobs

def get_event_handlers() -> list[common_pb2.JobData]:
    return []

def get_apps() -> list[common_pb2.AppDesciption]:
    resp : common_pb2.LibraryResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.Library(common_pb2.LibraryRequest())
    return resp.apps

def stop_apps(ids:int|list[int]):
    if isinstance(ids, str):
        ids = [ids]
    print(f'stopping {ids}')
    resp: common_pb2.StopResponse
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.Stop(common_pb2.StopRequest(
            header=common_pb2.Header(),
            ids=ids,
        ))
    return resp

def unschedule_app(id:str):
    resp: common_pb2.StopResponse
    print(f'unregisterin {id}')
    with grpc.insecure_channel(get_orchestrator_addr()) as channel:
        stub = common_pb2_grpc.SchedulerStub(channel)
        resp = stub.UnregisterCron(common_pb2.UnregisterCronRequest(
            header=common_pb2.Header(),
            uuid=id,
        ))
    return resp