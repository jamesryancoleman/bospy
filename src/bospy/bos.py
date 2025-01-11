from . import comms_pb2_grpc
from . import comms_pb2
import grpc

import datetime as dt
import sys
import os

from typing import Any

""" Provides the wrapper functions used to access openBOS points in Python
"""

VERSION = "0.0.4"

SYSMOD_ADDR = os.environ.get('SYSMOD_ADDR')
DEVCTRL_ADDR = os.environ.get('DEVCTRL_ADDR')

# uri -> name cache
point_name_cache = {}

# apply defaults
if SYSMOD_ADDR is None:
    SYSMOD_ADDR = "localhost:2821"
if DEVCTRL_ADDR is None:
    DEVCTRL_ADDR = "localhost:2822"

# client calls for the sysmod rpc calls
def NameToPoint(names:str|list[str], multiple_matches:bool=False, addr:str=SYSMOD_ADDR) -> None | list[str]:
    if isinstance(names, str):
        names = [names]
    else:
        multiple_matches = True

    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.NameToPoint(comms_pb2.GetRequest(
            Keys=names
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    # cast as a more user-friendly type
    if multiple_matches:
        return response.Values
    elif len(response.Values) == 1:
        return response.Values[0]
    else:
        return None
    
def PointToName(pt:str, addr:str=SYSMOD_ADDR) -> None | str:
    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.PointToName(comms_pb2.GetRequest(
            Keys=[pt]
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    if len(response.Values) > 0:
        return response.Values[0]
    else:
        return None

def TypeToPoint(types:str|list[str], addr:str=SYSMOD_ADDR) -> None | str | list[str]:
    if isinstance(types, str):
        types = [types]
    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.TypeToPoint(comms_pb2.GetRequest(
            Keys=types))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    # cast as a more user-friendly type
    return response.Values

def LocationToPoint(locations:str|list[str], addr:str=SYSMOD_ADDR) -> None | str | list[str]:
    print(locations, type(locations))
    if isinstance(locations, str):
        locations = [locations]
    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.LocationToPoint(comms_pb2.GetRequest(
            Keys=locations))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    return response.Values

def QueryPoints(query:str=None, types:str|list[str]=None, locations:str|list[str]=None, inherit_device_loc:bool=True, addr:str=SYSMOD_ADDR):
    """ if query, types, and locations are all none. This returns all pts in sysmod.
    """
    print('The sysmod address is: {}'.format(addr))
    if isinstance(types, str):
        types = [types]
    if isinstance(locations, str):
        locations = [locations]

    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        if query is None:
            response = stub.QueryPoints(comms_pb2.PointQueryRequest(
                Types=types,
                Locations=locations,
                ConsiderDeviceLoc=inherit_device_loc,
            ))
        else:
            response = stub.QueryPoints(comms_pb2.PointQueryRequest(
                Query=query,
            ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    return response.Values

# devctrl rpc calls
class GetValue(object):
    def __init__(self):
        self.Key:str
        self.Value:str

class GetResponse(object):
    def __init__(self):
        self.Values:list[GetValue] = []


def NewGetValues(resp:comms_pb2.GetResponse) -> list[GetValue]:
    V:list[GetValue] = []
    for v in resp.Pairs:
        _v = GetValue()
        _v.Key = v.Key
        _v.Value = GetTypedValue(v)
        V.append(_v)
        
    return V


class SetResponse(object):
    def __init__(self):
        self.Key:str = None
        self.ValueStr:str = None
        self.Ok:bool = False


def NewSetResponse(responses:comms_pb2.SetResponse) -> list[SetResponse]:
    R:list[SetResponse] = []
    for p in responses.Pairs:
        r = SetResponse()
        if p.Key is not None:
            r.Key = p.Key
        if p.Value is not None:
            r.ValueStr = p.Value
        r.Ok = p.Ok
        R.append(r)
    return R


def Ping(addr:str) -> bool:
    response: comms_pb2.Empty
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.HealthCheckStub(channel)
        response = stub.Ping(comms_pb2.Empty())
    if response is not None:
        return True
    else:
        return False


def CheckLatency(addr:str, num_pings:int=5) -> dt.timedelta | None:
    running_total:dt.timedelta
    for i in range(num_pings):
        start = dt.datetime.now()
        ok = Ping(addr)
        end = dt.datetime.now()
        if not ok:
            return None
        diff = end-start
        if i == 0:
            running_total = diff
        else:
            running_total = running_total + diff
    return running_total / num_pings
        

def Get(keys:str|list[str], full_response=False, addr=DEVCTRL_ADDR) -> list[GetResponse] | dict[str, object]:
    if type(keys) == str:
        keys = [keys]

    response: comms_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        response = stub.Get(comms_pb2.GetRequest(Keys=keys))
    R = NewGetValues(response)
    if full_response:
        return R
    D = {}
    for r in R:
        D[r.Key] = r.Value
    return D

def Set(keys:str|list[str], values:str|list[str], full_response=False, addr=DEVCTRL_ADDR) -> SetResponse | dict[str, bool] | bool:
    if isinstance(keys, str):
        keys = [keys]
    if isinstance(values, (str, float, int, bool)):
        values = [values]

    # validate the number of keys and values
    if len(keys) != len(values) :
        if len(keys) >= 1 and len(values) == 1:
            values = [values[0]] * len(keys)
        else:
            print("error: unable to broadcast values to match number of keys")
            print("\thave {} keys and {} values".format(len(keys), len(values)))
            return False

    # by now now we must have an equal number of keys and values, format them
    pairs = [comms_pb2.SetPair(Key=k, Value=str(values[i])) for i, k in enumerate(keys)]

    response: comms_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        response = stub.Set(comms_pb2.SetRequest(Pairs=pairs))
        if response.Error > 0:
            print("SET_ERROR_{}: {}".format(response.Error, response.ErrorMsg))
            return False
    r = NewSetResponse(response)
    if full_response:
        return r
    return True


def GetTypedValue(v:comms_pb2.GetPair|comms_pb2.SetPair):
    """ a helper function that uses the appropriate fields from a comms_pb2.GetReponse
    to return a typed value.
    """
    return DecodeValue(v.Value, v.Dtype)


def DecodeValue(s:str, dtype:comms_pb2.Dtype=comms_pb2.UNSPECIFIED):
    if (dtype == comms_pb2.DOUBLE) or (dtype == comms_pb2.FLOAT):
        return float(s)
    if (dtype == comms_pb2.INT32) or (dtype == comms_pb2.INT64) or (dtype == comms_pb2.UINT32) or (dtype == comms_pb2.UINT64):
        return int(s)
    if (dtype == comms_pb2.BOOL):
        return bool(s)
    if (dtype == comms_pb2.STRING):
        return s
    else:
        return UntypedString(s)
    

class UntypedString(str):
    """ Used to show that a value received by Get or GetMultiple was cast to a 
    native python type but that the function did not receive dtype information 
    (i.e., the Dtype=UNSPECIFIED)
    """

class PointUri(str):
    """ Used to indicate that a value is not just a str but specifically a point uri.
    """


if __name__ == "__main__":
    """ running this file will do a health check on the devctrl and sysmod services.
    """
    devctrl_addr = os.environ.get('DEVCTRL_ADDR')
    if devctrl_addr is None:
        print("environment variable DEVCTRL_ADDR not set. Try running:")
        print("\t$ source serivces/config-env")
        sys.exit(1)

    # make sure devCtrl is running
    try:
        resp = CheckLatency(devctrl_addr)
    except Exception as e:
        print("devctrl did not respond at {}\n\tis it running?".format(devctrl_addr))
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        sys.exit(1)
    else:
        print("devctrl running. RTT = {:.2f} ms".format(resp.total_seconds()*1000))

    sysmod_addr = os.environ.get('SYSMOD_ADDR')
    if sysmod_addr is None:
        print("environment variable DEVCTRL_ADDR not set. Try running:")
        print("\t$ source serivces/config-env")
        sys.exit(1)

    # make sure devCtrl is running
    try:
        resp = CheckLatency(sysmod_addr)
    except Exception as e:
        print("devCtrl did not respond at {}\n\tis it running?".format(sysmod_addr))
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        sys.exit(1)
    else:
        print("sysmod running. RTT = {:.2f} ms".format(resp.total_seconds()*1000))
