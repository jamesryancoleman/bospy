from google.protobuf.timestamp_pb2 import Timestamp
import bospy.config as config
from bospy import common_pb2_grpc
from bospy import common_pb2
import grpc

from rdflib import Graph, URIRef, parser

from typing import cast
import datetime as dt
import pandas as pd
import sys
import os

from typing import Any, Optional

""" Provides the wrapper functions used to access openBOS points in Python
"""

VERSION = "0.0.10"

_TXN_ID = int(os.environ.get('TXN_ID', 0))

# uri -> name cache
point_name_cache = {}

# config.get_sysmod_addr() = "localhost:2821"
# DEVCTRL_ADDR = "localhost:2822"
# HISTORY_ADDR = "localhost:2823"
# # SCHEDULER_ADDR = "localhost:2824"
# FORECAST_ADDR = "localhost:2825"

# # apply defaults
# def LoadEnv():
#     """ Called to load/reload the env vars. Does nothing if env vars not set
#     """
#     global config.get_sysmod_addr(), DEVCTRL_ADDR, HISTORY_ADDR, FORECAST_ADDR
#     config.get_sysmod_addr() = os.environ.get('config.get_sysmod_addr()', config.get_sysmod_addr())
#     DEVCTRL_ADDR = os.environ.get('DEVCTRL_ADDR', DEVCTRL_ADDR)
#     HISTORY_ADDR = os.environ.get('HISTORY_ADDR', HISTORY_ADDR)
#     FORECAST_ADDR = os.environ.get('FORECAST_ADDR', FORECAST_ADDR)

# LoadEnv()

# client calls for the sysmod rpc calls
def name_to_point(names:str|list[str], multiple_matches:bool=False) -> None | list[str]:
    if isinstance(names, str):
        names = [names]
    else:
        multiple_matches = True

    response: common_pb2.QueryResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.QueryPoints(common_pb2.PointQueryRequest(
            Names=names
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
    
def get_name(pt:str) -> None | str:
    response: common_pb2.QueryResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.GetName(common_pb2.GetRequest(
            Keys=[pt]
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))
    if len(response.Values) > 0:
        return response.Values[0]
    else:
        return None

# def type_to_point(types:str|list[str]) -> None | str | list[str]:
#     if isinstance(types, str):
#         types = [types]
#     response: common_pb2.QueryResponse
#     with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
#         stub = common_pb2_grpc.SysmodStub(channel)
#         response = stub.TypeToPoint(common_pb2.GetRequest(
#             Keys=types))
#         if response.Error > 0:
#             print("get '{}' error: {}".format(response.Query,
#                                               response.Error))
#     # cast as a more user-friendly type
#     return response.Values

# def location_to_point(locations:str|list[str]) -> None | str | list[str]:
#     print(locations, type(locations))
#     if isinstance(locations, str):
#         locations = [locations]
#     response: common_pb2.QueryResponse
#     with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
#         stub = common_pb2_grpc.SysmodStub(channel)
#         response = stub.LocationToPoint(common_pb2.GetRequest(
#             Keys=locations))
#         if response.Error > 0:
#             print("get '{}' error: {}".format(response.Query,
#                                               response.Error))
#     return response.Values

def query_points(query:str=None, names:str|list[str]=None, types:str|list[str]=None,
                locations:str|list[str]=None, inherit_device_loc:bool=True,
                parent_types:str|list[str]=None, device:str=None):
    """ if query, types, and locations are all none. This returns all pts in sysmod.
    """

    if isinstance(names, str):
        names = [names]
    if isinstance(types, str):
        types = [types]
    if isinstance(locations, str):
        locations = [locations]
    if isinstance(parent_types, str):
        parent_types = [parent_types]

    response: common_pb2.QueryResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        if query is None:
            response = stub.QueryPoints(common_pb2.PointQueryRequest(
                Names=names,
                Types=types,
                Locations=locations,
                ConsiderDeviceLoc=inherit_device_loc,
                ParentTypes=parent_types,
                Device=device,
            ))
        else:
            response = stub.QueryPoints(common_pb2.PointQueryRequest(
                Query=query,
            ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query,
                                              response.Error))                              
    return sorted(response.Values)

def query_devices(query:str=None, names:str|list[str]=None, types:str|list[str]=None, 
                locations:str|list[str]=None, child_types:str|list[str]=None) -> list[str]:
    
    if isinstance(names, str):
        names = [names]
    if isinstance(types, str):
        types = [types]
    if isinstance(locations, str):
        locations = [locations]
    if isinstance(child_types, str):
        child_types = [child_types]

    response:common_pb2.QueryResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        if query is None:
            response = stub.QueryDevices(common_pb2.DeviceQueryRequest(
                Names=names,
                Types=types,
                Locations=locations,
                ChildTypes=child_types,
            ))
        else:
            response = stub.QueryDevices(common_pb2.PointQueryRequest(
                Query=query,
            ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Query, response.Error))
    return sorted(response.Values)

def make_device(name:str, types:str|list[str]=None, locations:str|list[str]=None, 
               driver:str=None, properties:list[tuple]=None) -> str:
    """ takes the name, types, locations, driver, and any other properties you 
        wish to associate with the device.
        driver is of the format "bos://localhost/drives/[0-9]+".
        otherProperties is a list of 3-tuples of the format (subject:str, predicate:str, object:str)
    """
    if isinstance(types, str):
        types = [types]
    if isinstance(locations, str):
        locations = [locations]
    if properties:
        properties = [common_pb2.Triple(s=p[0], p=p[1], o=p[2]) for p in properties]

    response:common_pb2.MakeResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.MakeDevice(common_pb2.MakeDeviceRequest(
            Name=name,
            Types=types,
            Locations=locations,
            Driver=driver,
            other_properties=properties,
        ))
    if response.ErrorMsg != "":
        return f"error: { response.ErrorMsg}"
    return response.Url

def make_point(name:str, device:str, types:str|list[str]=None, locations:str|list[str]=None, 
              xref:str=None, properties:list[tuple]=None, ) -> str:
    """ takes the name, types, locations, and any other properties you 
        wish to associate with the device.
        otherProperties is a list of 3-tuples of the format (subject:str, predicate:str, object:str)
    """
    if isinstance(types, str):
        types = [types]
    if isinstance(locations, str):
        locations = [locations]
    if properties:
        properties = [common_pb2.Triple(s=p[0], p=p[1], o=p[2]) for p in properties]

    response:common_pb2.MakeResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.MakePoint(common_pb2.MakePointRequest(
            Device=device,
            Name=name,
            Types=types,
            Locations=locations,
            Xref=xref,
            other_properties=properties,
        ))
    if response.ErrorMsg != "":
        return f"error: {response.ErrorMsg}"
    return response.Url

def query_drivers() -> list[dict]:
    """Return all registered drivers as [{"uri": ..., "name": ...}], sorted by name."""
    query = """
        SELECT DISTINCT ?uri ?pred ?name WHERE {
            ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
                 <https://openbos.org/schema/bos#Driver> .
            ?uri <https://openbos.org/schema/bos#Name> ?name .
            BIND(<https://openbos.org/schema/bos#Name> AS ?pred)
        } ORDER BY ?name
    """
    g = BasicQuery(query)
    seen = set()
    results = []
    for s, p, o in g:
        uri = str(s)
        if uri not in seen:
            seen.add(uri)
            results.append({"uri": uri, "name": str(o)})
    return results

def make_driver(name:str, host:str, port:int, image:str=None, container:str=None) -> str:
    """ name    of the driver
        host    the hostname (preferred) or IP that the service can be found at
        port    starts at 50061 by convention
        
        [optional]
        image       name of the image to pull if not on system
        container   name of the container if it doesn't match the hostname
    """
    response: common_pb2.MakeResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.MakeDriver(common_pb2.MakeDriverRequest(
            Name=name,
            Host=host,
            Port=str(port),
            Image=image,
            Container=container,
        ))
    if response.ErrorMsg != "":
        return "error: {response.ErrorMsg}"
    return response.Url

def Delete(sub:str="", pred:str="", obj:str="") -> common_pb2.DeleteResponse:
    if sub == "" and pred == "" and obj == "":
        print("must provide at least one of subject, predicate, or object")
        return common_pb2.DeleteResponse()
    response:common_pb2.DeleteResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.Delete(common_pb2.DeleteRequest(
            Triple=common_pb2.Triple(
                s=sub,
                p=pred,
                o=obj,
            )
        ))
    return response

def make_space(name: str, kind: str, parents: list[str] = None, children: list[str] = None) -> str:
    """Create a new location/space node in the system model.

    name     — human-readable label (e.g. "CHAOS Lab")
    kind     — REC class URI (e.g. "https://w3id.org/rec#Room")
    parents  — list of parent space URIs (the parent gains a rec:hasPart edge to this node)
    children — list of child space URIs (this node gains rec:hasPart edges to them)
    Returns the URI of the new node, or a string starting with "error:" on failure.
    """
    if parents is None:
        parents = []
    if children is None:
        children = []
    response: common_pb2.MakeResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.MakeSpace(common_pb2.MakeSpaceRequest(
            name=name,
            kind=kind,
            parent_uuids=parents,
            child_uuids=children,
        ))
    if response.ErrorMsg:
        return "error: {}".format(response.ErrorMsg)
    return response.Url

def delete_node(uri: str) -> bool:
    """Delete all triples where uri is the subject or the object."""
    response: common_pb2.DeleteResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.Delete(common_pb2.DeleteRequest(
            root_node=uri,
        ))
    return True

_KIND_TO_ENTITY_TYPE = {
    'bos:Device':   common_pb2.ENTITY_TYPE_DEVICE,
    'bos:Point':    common_pb2.ENTITY_TYPE_POINT,
    'bos:Location': common_pb2.ENTITY_TYPE_SPACE,
    'bos:Driver':   common_pb2.ENTITY_TYPE_DRIVER,
}

def update_entity(uri: str, kind: str = None, updates: list[dict] = None,
                  deletions: list[dict] = None,
                  additions: list[dict] = None) -> dict:
    """Call the sysmod Update RPC.

    Each triple dict has keys 's', 'p', 'o'.
    - kind:      compact bos: type string (e.g. 'bos:Device'); passed as EntityType to skip
                 the server-side graph query for type detection
    - updates:   functional upserts — atomically replaces any existing value for (s, p)
    - deletions: exact (s, p, o) removals
    - additions: new triples appended without removing existing values

    Returns {'deleted': [...], 'inserted': [...]} or raises on error.
    """
    def _triple(d: dict) -> common_pb2.Triple:
        return common_pb2.Triple(s=d.get('s', ''), p=d.get('p', ''), o=d.get('o', ''))

    entity_type = _KIND_TO_ENTITY_TYPE.get(kind or '', common_pb2.ENTITY_TYPE_UNSPECIFIED)

    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        response = stub.Update(common_pb2.UpdateRequest(
            root_uri=uri,
            kind=entity_type,
            updates=[_triple(t) for t in (updates or [])],
            deletions=[_triple(t) for t in (deletions or [])],
            additions=[_triple(t) for t in (additions or [])],
        ))
    return {
        'deleted':  [{'s': t.s, 'p': t.p, 'o': t.o} for t in response.deleted],
        'inserted': [{'s': t.s, 'p': t.p, 'o': t.o} for t in response.inserted],
    }

# History rpc calls
def set_sample_rate(pts:str|list[str], rates:str|list[str]) -> bool:
    if isinstance(pts, str):
        pts = [pts]
    if isinstance(rates, str):
        rates = [rates]

    pairs = []
    if len(pts) == len(rates):
        pairs = [common_pb2.SetPair(Key=k, Value=rates[i]) for i, k in enumerate(pts)]
    elif len(rates) == 1:
        pairs = [common_pb2.SetPair(Key=k, Value=rates[0]) for k in pts]
    else:
        print("unable invalid combination of pts ({}) and rates {}".format(len(pts), len(rates)))
        return False
    
    response: common_pb2.SetResponse
    with grpc.insecure_channel(config.get_history_addr()) as channel:
        stub = common_pb2_grpc.HistoryStub(channel)
        response = stub.SetSampleRate(common_pb2.SetRequest(
            Pairs=pairs
        ))
        if response.Error > 0:
            print("SetSampleRates: error code {}".format(response.Error))
            return False
    #  trigger a refresh
    refresh_rates()
    return True

def refresh_rates():
    response: common_pb2.RefreshRatesResponse
    with grpc.insecure_channel(config.get_history_addr()) as channel:
        stub = common_pb2_grpc.HistoryStub(channel)
        response = stub.RefreshRates(common_pb2.RefreshRatesRequest())
        if response.Error > 0:
            print("RefreshRates: error code {}".format(response.Error))
            return False
    return True

def get_history(pts:str|list[str], start:str=None, end:str=None, limit:int=14400, 
               pandas:bool=False, tz:str=None, group_by_id:bool=True, 
               get_names:bool=False, resample_to:str=None) -> list[common_pb2.HisRow] | None:
    if isinstance(pts, str):
        pts = [pts]
    if start is None:
        start = ""
    if end is None:
        end = ""
    response: common_pb2.HistoryResponse
    with grpc.insecure_channel(config.get_history_addr()) as channel:
        stub = common_pb2_grpc.HistoryStub(channel)
        response = stub.GetHistory(common_pb2.HistoryRequest(
            Start=start, 
            End=end,
            Keys=pts,
            Limit=limit,
        ))
        if response.Error > 0:
            print("GetHistory: error code {}".format(response.Error))
            return None
    R = [[r.Timestamp, r.Value, r.Id] for r in response.Rows]
    if pandas:
        import pandas as pd
        df = pd.DataFrame(R, columns=['time', 'value', 'id'])
        df['time'] = pd.to_datetime(df['time'], utc=True)
        if tz:
            from pytz import timezone
            _tz = timezone(tz)
            df['time'] = df['time'].dt.tz_convert(_tz)
        if group_by_id:
            xf = pd.DataFrame()
            G = df.groupby('id')
            columns = ['time']
            count = 0 
            for _id, g in G:
                if len(xf) == 0:
                    xf = g[['time', 'value']]
                else:
                    xf = pd.merge_ordered(xf, g[['time', 'value']], 
                                        on='time', fill_method='ffill', suffixes=('', f'_df{count+1}'))
                columns.append(_id)
                count+=1
            xf.columns = columns
            df = xf
        df.set_index('time', inplace=True)
        if resample_to:
            df = df.resample(resample_to).mean()
        if get_names:
            df.columns = [get_name(pt) for pt in df.columns]
        return df.sort_index()
    return R

# devctrl rpc calls
class GetValue(object):
    def __init__(self, key, value):
        self.Key:str = key
        self.Value = value

class GetResponse(object):
    def __init__(self):
        self.Values:list[GetValue] = []


def NewGetValues(resp:common_pb2.GetResponse) -> list[GetValue]:
    V:list[GetValue] = []
    for pair in resp.Pairs:
        p = GetValue(
            key=pair.Key,
            value=GetTypedValue(pair),
        )
        V.append(p)
    return V


class SetResponse(object):
    def __init__(self):
        self.Key:str = None
        self.ValueStr:str = None
        self.Ok:bool = False


def NewSetResponse(responses:common_pb2.SetResponse) -> list[SetResponse]:
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
    response: common_pb2.Empty
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.HealthCheckStub(channel)
        response = stub.Ping(common_pb2.Empty())
    if response is not None:
        return True
    else:
        return False


# def CheckLatency(addr:str, num_pings:int=5) -> dt.timedelta | None:
#     running_total:dt.timedelta
#     for i in range(num_pings):
#         start = dt.datetime.now()
#         ok = Ping(addr)
#         end = dt.datetime.now()
#         if not ok:
#             return None
#         diff = end-start
#         if i == 0:
#             running_total = diff
#         else:
#             running_total = running_total + diff
#     return running_total / num_pings
        

def _get_pt_values(*keys:str):
    """Like _get_pt but returns a single value for one key, or an ordered tuple for multiple."""
    result = cast(dict, _get_pt(list(keys)))
    values = tuple(result.get(k) for k in keys)
    return values[0] if len(keys) == 1 else values

def _get_pt(keys:str|list[str], full_response=False) -> list[GetResponse] | dict[str, object]:
    if type(keys) == str:
        keys = [keys]

    response: common_pb2.GetResponse
    with grpc.insecure_channel(config.get_devctrl_addr()) as channel:
        stub = common_pb2_grpc.DeviceControlStub(channel)
        response = stub.Get(common_pb2.GetRequest(
            Header=common_pb2.Header(TxnId=_TXN_ID),
            Keys=keys,
        ))
    R = NewGetValues(response)
    if full_response:
        return R
    D = {}
    for r in R:
        D[r.Key] = r.Value

    # guarantee every requested key is present; None means not found/unavailable
    for k in keys:
        D.setdefault(k, None)

    return D

def _set_pt(keys:str|list[str], values:str|list[str], full_response=False) -> SetResponse | dict[str, bool] | bool:
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
    pairs = [common_pb2.SetPair(Key=k, Value=str(values[i])) for i, k in enumerate(keys)]

    response: common_pb2.SetResponse
    with grpc.insecure_channel(config.get_devctrl_addr()) as channel:
        stub = common_pb2_grpc.DeviceControlStub(channel)
        response = stub.Set(common_pb2.SetRequest(
            Header=common_pb2.Header(TxnId=_TXN_ID),
            Pairs=pairs,
        ))
        if response.Error > 0:
            print("SET_ERROR_{}: {}".format(response.Error, response.ErrorMsg))
            return False
    r = NewSetResponse(response)
    if full_response:
        return r
    return True

def GetTypedValue(v:common_pb2.GetPair|common_pb2.SetPair):
    """ a helper function that uses the appropriate fields from a common_pb2.GetReponse
    to return a typed value.
    """
    return DecodeValue(v.Value, v.Dtype)


def DecodeValue(s:str, dtype:common_pb2.Dtype=common_pb2.UNSPECIFIED):
    if (dtype == common_pb2.DOUBLE) or (dtype == common_pb2.FLOAT):
        return float(s)
    if (dtype == common_pb2.INT32) or (dtype == common_pb2.INT64) or (dtype == common_pb2.UINT32) or (dtype == common_pb2.UINT64):
        return int(s)
    if (dtype == common_pb2.BOOL):
        if s.lower() == "true":
            return True
        return False
    if (dtype == common_pb2.STRING):
        return s
    else:
        return UntypedString(s)

def BasicQuery(query:str) -> Graph:
    # call the BasicQuery endpoint
    resp: common_pb2.BasicQueryResponse
    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        resp = stub.BasicQuery(common_pb2.BasicQueryRequest(
            Query=query
        ))
        if resp.Error > 0:
            print("QUERY_ERROR_{}: {}".format(resp.Error, resp.ErrorMsg))
            return False
    
    # translate the results 
    g = Graph()
    for t in resp.Results:
        g.parse(data=f"{t.s} {t.p} {t.o} .", format="turtle")
    return g

def get_spaces() -> list[dict]:
    """Return all space/location nodes (rdf:type bos:Location) with their rdfs:label, kind, and hasPart children."""
    query = """
        SELECT DISTINCT ?sub ?pred ?obj WHERE {
            ?sub <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://openbos.org/schema/bos#Location> .
            ?sub ?pred ?obj .
            FILTER(?pred IN (
                <http://www.w3.org/2000/01/rdf-schema#label>,
                <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,
                <https://w3id.org/rec#hasPart>
            ))
        }
    """
    g = BasicQuery(query)
    if not g:
        return []

    TYPE_P = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    LABEL_P = "http://www.w3.org/2000/01/rdf-schema#label"
    LOCATION_T = "https://openbos.org/schema/bos#Location"
    HASPART_P = "https://w3id.org/rec#hasPart"

    spaces = {}
    for s, p, o in g:
        uri = str(s)
        pred = str(p)
        obj = str(o)
        if uri not in spaces:
            spaces[uri] = {"uri": uri, "label": "", "kind": "", "parts": []}
        if pred == LABEL_P:
            spaces[uri]["label"] = obj
        elif pred == TYPE_P and obj != LOCATION_T:
            kind = obj.rsplit("#", 1)[-1] if "#" in obj else obj.rsplit("/", 1)[-1]
            spaces[uri]["kind"] = kind
        elif pred == HASPART_P:
            spaces[uri]["parts"].append(obj)

    return list(spaces.values())


def get_ontology_subclasses(root_uri: str, graph_uri: str, transitive: bool = True) -> list[dict]:
    """Return subclasses of root_uri within a named graph in Oxigraph.

    Uses a 3-column SELECT (?class ?pred ?label) so results map cleanly to
    the (Subject, Predicate, Object) triple format that BasicQuery returns.
    Requires the ontology to already be loaded as the named graph graph_uri.
    Set transitive=False to return only direct subclasses.
    """
    path = "+" if transitive else ""
    query = f"""
        SELECT DISTINCT ?class ?pred ?label WHERE {{
            GRAPH <{graph_uri}> {{
                ?class <http://www.w3.org/2000/01/rdf-schema#subClassOf>{path} <{root_uri}> .
                ?class <http://www.w3.org/2000/01/rdf-schema#label> ?label .
                BIND(<http://www.w3.org/2000/01/rdf-schema#label> AS ?pred)
            }}
        }} ORDER BY ?label
    """
    g = BasicQuery(query)
    if not g:
        return []
    seen = set()
    results = []
    for s, p, o in g:
        uri = str(s)
        if uri not in seen:
            seen.add(uri)
            results.append({"uri": uri, "label": str(o)})
    return results


def GetAllLocation() -> set[str]:
    query = """
        SELECT DISTINCT ?sub ?pred ?obj WHERE {
                ?sub ?pred ?obj .
                VALUES ?pred { <https://openbos.org/schema/bos#Location> }
        } ORDER BY (?obj)
        """
    results = set()
    g = BasicQuery(query)
    for s, p, o in g:
        results.add(str(o))
    return results

def GetForecast(point: str="", forecast_id: str="", 
                start: str|dt.datetime=None, 
                end: str|dt.datetime=None,
                pandas=True, tz="") -> None | common_pb2.GetForecastResponse | list[pd.DataFrame]:
    """
    GetForecast returns a forecast if the id is known. If the point is provided 
    newest forecast is returned. For now, this only accepts 1 point. TODO add 
    support for N points.
    
    :param point: Description
    :type point: str
    :param forecast_id: Description
    :type forecast_id: str
    :return: Description
    :rtype: GetForecastResponse | None
    """
    if not (point or forecast_id):
        print("error, must provide point or forecast_id")
        return None
    if isinstance(start, str):
        start = dt.datetime.fromisoformat(start)
    if isinstance(end, str):
        end = dt.datetime.fromisoformat(end)

    resp: common_pb2.GetForecastResponse
    with grpc.insecure_channel(config.get_forecast_addr()) as channel:
        stub = common_pb2_grpc.ForecastStub(channel)
        resp = stub.Get(common_pb2.GetForecastRequest(
            header=common_pb2.Header(
                Src="python-client",
                Dst=config.get_forecast_addr()),
            forecast_id=forecast_id,
            point_uri=point,
            start=start,
            end=end,
            ))
        
    if pandas:
        frames = []
        for f in resp.forecasts:
            _df = pd.DataFrame({
                    'time': [pair.target_time.ToDatetime() for pair in f.values],
                    'value': [pair.value for pair in f.values],
                })
            _df.time = _df.time.dt.tz_localize('UTC')
            if tz != "":
                _df.time = _df.time.dt.tz_convert(tz)
            _df.set_index('time', inplace=True)
            frames.append(_df)
        return frames

    return resp

def SetForecast(point:str, values:list[tuple[dt.datetime, float]], model:str="", 
                model_version:str="") -> Optional[str]:
    """
    Docstring for SetForecast
    
    :param point: Description
    :type point: str
    :param values: Description
    :type values: list[tuple[dt.datetime, float]]
    :param model: Conventionally, container/app that was used to make this forecast.
    :type model: str
    :param model_version: Conventially, the git commit for this container/model.
    :type model_version: str
    :return: The uuid assigned to this forecast.
    :rtype: str
    """
    if len(values) < 1:
        # TODO: add exception
        return None
    
    V: list[common_pb2.ForecastValue] = []
    for pair in values:
        target_time = Timestamp()
        target_time.FromDatetime(pair[0])
        V.append(common_pb2.ForecastValue(
            target_time=target_time,
            value=pair[1]))
    req = common_pb2.SetForecastRequest(
        header=common_pb2.Header(
            Src="bospy.client",
            Dst="forecast.local"),
        forecast=common_pb2.ForecastEntry(
            point_uri=point,
            model=model,
            model_version=model_version,
            values=V))
    resp: common_pb2.SetForecastResponse
    with grpc.insecure_channel(config.get_forecast_addr()) as channel:
        stub = common_pb2_grpc.ForecastStub(channel)
        resp = stub.Set(req)

    return resp.id


class UntypedString(str):
    """ Used to show that a value received by Get or GetMultiple was cast to a 
    native python type but that the function did not receive dtype information 
    (i.e., the Dtype=UNSPECIFIED)
    """

class PointUri(str):
    """ Used to indicate that a value is not just a str but specifically a point uri.
    """

def suggest_points(preferred_class: str, accept_class: str,
                   device: str = None, limit: int = 0) -> list[dict]:
    """Return ranked point suggestions matching accept_class (or subclasses),
    with points that also match preferred_class sorted first.

    preferred_class  — ideal class as a CURIE or full URI
                       (e.g. "brick:Zone_Air_Temperature_Sensor" or
                        "https://brickschema.org/schema/Brick#Zone_Air_Temperature_Sensor")
    accept_class     — minimum acceptable superclass as a CURIE or full URI
    device           — optional device URI to filter results
    limit            — max number of results (0 = unlimited)

    Returns a list of dicts with keys: point, point_class, name, preferred.
    """
    req = common_pb2.SuggestPointsRequest(
        preferred_class=preferred_class,
        accept_class=accept_class,
        limit=limit if limit > 0 else None,
    )
    if device:
        req.device = device

    with grpc.insecure_channel(config.get_sysmod_addr()) as channel:
        stub = common_pb2_grpc.SysmodStub(channel)
        resp = stub.SuggestPoints(req)

    return [
        {
            "point":       s.point,
            "point_class": s.point_class,
            "name":        s.name,
            "preferred":   s.preferred,
        }
        for s in resp.suggestions
    ]


_BOS_NS = "https://openbos.org/schema/bos#"

def set_point_range(
    pts: str | list[str],
    *,
    off_value: str | int | float | bool = None,
    on_value: str | int | float | bool = None,
    min_value: str | int | float = None,
    max_value: str | int | float = None,
) -> list[dict]:
    """Assign on/off/min/max metadata to one or more points in the system model.

    All values are stored as strings.  Pass only the fields you want to set;
    omitted fields are left unchanged.  Existing values are atomically replaced
    (upsert semantics via update_entity's `updates` list).

    Example — analog 0-10V device with dead zone:
        set_point_range(pts, off_value="0", on_value="2.0", min_value="2.0", max_value="10.0")

    Example — binary device:
        set_point_range(pts, off_value="false", on_value="true")
    """
    if isinstance(pts, str):
        pts = [pts]

    field_map = {
        f"{_BOS_NS}offValue": str(off_value).lower() if isinstance(off_value, bool) else (str(off_value) if off_value is not None else None),
        f"{_BOS_NS}onValue":  str(on_value).lower()  if isinstance(on_value,  bool) else (str(on_value)  if on_value  is not None else None),
        f"{_BOS_NS}minValue": str(min_value) if min_value is not None else None,
        f"{_BOS_NS}maxValue": str(max_value) if max_value is not None else None,
    }
    updates = [{"s": "", "p": pred, "o": val}
               for pred, val in field_map.items() if val is not None]

    if not updates:
        return []

    results = []
    for pt in pts:
        if not isinstance(pt, str):
            raise TypeError(f"set_point_range: expected a point URI string, got {type(pt).__name__}: {pt!r}. "
                            "If passing a dict, use .keys() instead of .items().")
        triples = [{"s": pt, "p": t["p"], "o": t["o"]} for t in updates]
        result = update_entity(pt, kind="bos:Point", updates=triples)
        results.append({"point": pt, **result})
    return results


def RefreshNameTable():
    """ Calls the RefreshNames rpc of the History service. Used primarily to have
    user friendly names in Grafana.
    """
    with grpc.insecure_channel(config.get_history_addr()) as channel:
        stub = common_pb2_grpc.HistoryStub(channel)
        stub.RefreshNames(common_pb2.RefreshNamesRequest())
    return True