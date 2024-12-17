import comms_pb2_grpc
import comms_pb2 
import grpc

import datetime as dt
import sys
import os

""" Provides the wrapper functions used to access openBOS points in Python
"""

SYSMOD_ADDR = os.environ.get('SYSMOD_ADDR')
DEVCTRL_ADDR = os.environ.get('DEVCTRL_ADDR')

if SYSMOD_ADDR is None:
    SYSMOD_ADDR = "localhost:2821"
if DEVCTRL_ADDR is None:
    DEVCTRL_ADDR = "localhost:2822"

def NameToPoint(name:str, multiple_matches:bool=False, addr:str=SYSMOD_ADDR) -> None | str | list[str]:
    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.NameToPoints(comms_pb2.GetRequest(
            Key=name
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Response.Key,
                                              response.Response.Error))
    # cast as a more user-friendly type
    matches = response.Value.split()
    if multiple_matches:
        return matches
    elif len(matches) > 0:
        return matches[0]
    else:
        return None
    

def TypeToPoint(_type:str, addr:str=SYSMOD_ADDR) -> None | str | list[str]:
    response: comms_pb2.QueryResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.SysmodStub(channel)
        response = stub.TypeToPoints(comms_pb2.GetRequest(
            Key=_type
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Response.Key,
                                              response.Response.Error))
    # cast as a more user-friendly type
    matches = response.Value.split()
    return matches



class GetResponse(object):
    def __init__(self):
        self.Key:str
        self.ValueStr:str
        self.Value = None 


def NewGetResponse(resp:comms_pb2.GetResponse) -> GetResponse:
    r = GetResponse()
    if resp.Key is not None:
            r.Key = resp.Key
    
    r.ValueStr = resp.Value
    r.Value = GetTypedValue(resp)
    return r


def NewGetMultipleResponse(responses:comms_pb2.GetMultipleResponse) -> list[GetResponse]:
    R:list[GetResponse] = []
    for resp in responses.Responses:
        r = GetResponse()
        if resp.Key is not None:
            r.Key = resp.Key
        r.ValueStr = resp.Value
        r.Value = GetTypedValue(resp)
        R.append(r)
    return R


class SetResponse(object):
    def __init__(self):
        self.Key:str = None
        self.ValueStr:str = None
        self.Ok:bool = False


def NewSetResponse(resp:comms_pb2.SetResponse) -> SetResponse:
    r = SetResponse()
    print(resp.Key)
    if resp.Key is not None:
        r.Key = resp.Key
    if resp.Value is not None:
        r.ValueStr = resp.Value
    r.Ok = resp.Ok
    return r


def NewSetMultipleResponse(responses:comms_pb2.SetMultipleResponse) -> list[SetResponse]:
    R:list[SetResponse] = []
    for resp in responses.Responses:
        r = SetResponse()
        if resp.Key is not None:
            r.Key = resp.Key
        if resp.Value is not None:
            r.ValueStr = resp.Value
        r.Ok = resp.Ok
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
        

def Get(key:str, full_response=False, addr:str=DEVCTRL_ADDR) -> GetResponse | bool:
    response: comms_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        response = stub.Get(comms_pb2.GetRequest(
            Key=key
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Key, 
                                              response.Error))
    # cast as a more user-friendly type
    r = NewGetResponse(response)
    if full_response:
        return r
    return r.Value

def Set(key:str, value:str, full_response=False, addr=DEVCTRL_ADDR) -> SetResponse | bool:
    response: comms_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        response = stub.Set(comms_pb2.SetRequest(
            Key=key, 
            Value=str(value),
        ))
        if not response.Ok:
            print("set '{}' error: {}".format(response.Response.Key,
                                              response.Response.Error))
    r = NewSetResponse(response)
    if full_response:
        return r
    return r.Ok


def GetMutiple(keys:list[str], full_response=False, addr=DEVCTRL_ADDR) -> list[GetResponse] | dict[str, object]:
    responses: comms_pb2.GetMultipleResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        responses = stub.GetMultiple(
            comms_pb2.GetMultipleRequest(
                Keys=keys
            )
        )
    R = NewGetMultipleResponse(responses)
    if full_response:
        return R
    resp_dict = {}
    for r in R:
        resp_dict[r.Key] = r.Value
    return resp_dict
    


def SetMultiple(key_value_pairs:tuple[str,str], addr=DEVCTRL_ADDR) -> list[SetResponse]:
    responses : comms_pb2.SetMultipleResponse
    # convert all values to strings
    for i, pair in enumerate(key_value_pairs):
        key_value_pairs[i] = (pair[0], str(pair[1]))
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        responses = stub.SetMultiple(
            comms_pb2.SetMultipleRequest(
                Requests=[comms_pb2.SetRequest(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return NewSetMultipleResponse(responses)


def GetTypedValue(resp:comms_pb2.GetResponse):
    """ a helper function that uses the appropriate fields from a comms_pb2.GetReponse
    to return a typed value.
    """
    return DecodeValue(resp.Value, resp.Dtype)


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
