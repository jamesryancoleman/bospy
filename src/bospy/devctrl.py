import grpc
import bospy.config as config
from bospy import common_pb2_grpc
from bospy import common_pb2


def clear_cache() -> bool:
    """Trigger the DeviceControl ClearCache RPC, flushing the devctrl value cache."""
    with grpc.insecure_channel(config.get_devctrl_addr()) as channel:
        stub = common_pb2_grpc.DeviceControlStub(channel)
        stub.ClearCache(common_pb2.ClearCacheRequest())
    return True