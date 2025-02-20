# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import comms_pb2 as comms__pb2

GRPC_GENERATED_VERSION = '1.66.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in comms_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GetSetRunStub(object):
    """the GetSetRun service provides the fundamental driver functionality for Setting 
    values, getting them, and running commands.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/bos.GetSetRun/Get',
                request_serializer=comms__pb2.GetRequest.SerializeToString,
                response_deserializer=comms__pb2.GetResponse.FromString,
                _registered_method=True)
        self.Set = channel.unary_unary(
                '/bos.GetSetRun/Set',
                request_serializer=comms__pb2.SetRequest.SerializeToString,
                response_deserializer=comms__pb2.SetResponse.FromString,
                _registered_method=True)


class GetSetRunServicer(object):
    """the GetSetRun service provides the fundamental driver functionality for Setting 
    values, getting them, and running commands.
    """

    def Get(self, request, context):
        """rpc for getting a value from a driver
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Set(self, request, context):
        """rpc for setting a value on a driver
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GetSetRunServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=comms__pb2.GetRequest.FromString,
                    response_serializer=comms__pb2.GetResponse.SerializeToString,
            ),
            'Set': grpc.unary_unary_rpc_method_handler(
                    servicer.Set,
                    request_deserializer=comms__pb2.SetRequest.FromString,
                    response_serializer=comms__pb2.SetResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bos.GetSetRun', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bos.GetSetRun', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class GetSetRun(object):
    """the GetSetRun service provides the fundamental driver functionality for Setting 
    values, getting them, and running commands.
    """

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.GetSetRun/Get',
            comms__pb2.GetRequest.SerializeToString,
            comms__pb2.GetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Set(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.GetSetRun/Set',
            comms__pb2.SetRequest.SerializeToString,
            comms__pb2.SetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class SysmodStub(object):
    """the PointId (pid) service takes classes, names, or regexes
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryDevices = channel.unary_unary(
                '/bos.Sysmod/QueryDevices',
                request_serializer=comms__pb2.DeviceQueryRequest.SerializeToString,
                response_deserializer=comms__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.QueryPoints = channel.unary_unary(
                '/bos.Sysmod/QueryPoints',
                request_serializer=comms__pb2.PointQueryRequest.SerializeToString,
                response_deserializer=comms__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.GetName = channel.unary_unary(
                '/bos.Sysmod/GetName',
                request_serializer=comms__pb2.GetRequest.SerializeToString,
                response_deserializer=comms__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.GetDriver = channel.unary_unary(
                '/bos.Sysmod/GetDriver',
                request_serializer=comms__pb2.GetRequest.SerializeToString,
                response_deserializer=comms__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.GetDriverXref = channel.unary_unary(
                '/bos.Sysmod/GetDriverXref',
                request_serializer=comms__pb2.GetRequest.SerializeToString,
                response_deserializer=comms__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.MakeDevice = channel.unary_unary(
                '/bos.Sysmod/MakeDevice',
                request_serializer=comms__pb2.MakeDeviceRequest.SerializeToString,
                response_deserializer=comms__pb2.MakeResponse.FromString,
                _registered_method=True)
        self.MakePoint = channel.unary_unary(
                '/bos.Sysmod/MakePoint',
                request_serializer=comms__pb2.MakePointRequest.SerializeToString,
                response_deserializer=comms__pb2.MakeResponse.FromString,
                _registered_method=True)
        self.MakeDriver = channel.unary_unary(
                '/bos.Sysmod/MakeDriver',
                request_serializer=comms__pb2.MakeDriverRequest.SerializeToString,
                response_deserializer=comms__pb2.MakeResponse.FromString,
                _registered_method=True)
        self.Delete = channel.unary_unary(
                '/bos.Sysmod/Delete',
                request_serializer=comms__pb2.DeleteRequest.SerializeToString,
                response_deserializer=comms__pb2.DeleteResponse.FromString,
                _registered_method=True)


class SysmodServicer(object):
    """the PointId (pid) service takes classes, names, or regexes
    """

    def QueryDevices(self, request, context):
        """sysmod querying rpcs
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPoints(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetName(self, request, context):
        """rpc NameToPoint(GetRequest) returns (QueryResponse);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDriver(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDriverXref(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MakeDevice(self, request, context):
        """sysmod populating rpcs
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MakePoint(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MakeDriver(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SysmodServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'QueryDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryDevices,
                    request_deserializer=comms__pb2.DeviceQueryRequest.FromString,
                    response_serializer=comms__pb2.QueryResponse.SerializeToString,
            ),
            'QueryPoints': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryPoints,
                    request_deserializer=comms__pb2.PointQueryRequest.FromString,
                    response_serializer=comms__pb2.QueryResponse.SerializeToString,
            ),
            'GetName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetName,
                    request_deserializer=comms__pb2.GetRequest.FromString,
                    response_serializer=comms__pb2.QueryResponse.SerializeToString,
            ),
            'GetDriver': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDriver,
                    request_deserializer=comms__pb2.GetRequest.FromString,
                    response_serializer=comms__pb2.QueryResponse.SerializeToString,
            ),
            'GetDriverXref': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDriverXref,
                    request_deserializer=comms__pb2.GetRequest.FromString,
                    response_serializer=comms__pb2.QueryResponse.SerializeToString,
            ),
            'MakeDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.MakeDevice,
                    request_deserializer=comms__pb2.MakeDeviceRequest.FromString,
                    response_serializer=comms__pb2.MakeResponse.SerializeToString,
            ),
            'MakePoint': grpc.unary_unary_rpc_method_handler(
                    servicer.MakePoint,
                    request_deserializer=comms__pb2.MakePointRequest.FromString,
                    response_serializer=comms__pb2.MakeResponse.SerializeToString,
            ),
            'MakeDriver': grpc.unary_unary_rpc_method_handler(
                    servicer.MakeDriver,
                    request_deserializer=comms__pb2.MakeDriverRequest.FromString,
                    response_serializer=comms__pb2.MakeResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=comms__pb2.DeleteRequest.FromString,
                    response_serializer=comms__pb2.DeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bos.Sysmod', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bos.Sysmod', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Sysmod(object):
    """the PointId (pid) service takes classes, names, or regexes
    """

    @staticmethod
    def QueryDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/QueryDevices',
            comms__pb2.DeviceQueryRequest.SerializeToString,
            comms__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def QueryPoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/QueryPoints',
            comms__pb2.PointQueryRequest.SerializeToString,
            comms__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/GetName',
            comms__pb2.GetRequest.SerializeToString,
            comms__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetDriver(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/GetDriver',
            comms__pb2.GetRequest.SerializeToString,
            comms__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetDriverXref(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/GetDriverXref',
            comms__pb2.GetRequest.SerializeToString,
            comms__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MakeDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/MakeDevice',
            comms__pb2.MakeDeviceRequest.SerializeToString,
            comms__pb2.MakeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MakePoint(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/MakePoint',
            comms__pb2.MakePointRequest.SerializeToString,
            comms__pb2.MakeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MakeDriver(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/MakeDriver',
            comms__pb2.MakeDriverRequest.SerializeToString,
            comms__pb2.MakeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.Sysmod/Delete',
            comms__pb2.DeleteRequest.SerializeToString,
            comms__pb2.DeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class HealthCheckStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/bos.HealthCheck/Ping',
                request_serializer=comms__pb2.Empty.SerializeToString,
                response_deserializer=comms__pb2.Empty.FromString,
                _registered_method=True)


class HealthCheckServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HealthCheckServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=comms__pb2.Empty.FromString,
                    response_serializer=comms__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bos.HealthCheck', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bos.HealthCheck', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class HealthCheck(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.HealthCheck/Ping',
            comms__pb2.Empty.SerializeToString,
            comms__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class HistoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetHistory = channel.unary_unary(
                '/bos.History/GetHistory',
                request_serializer=comms__pb2.HistoryRequest.SerializeToString,
                response_deserializer=comms__pb2.HistoryResponse.FromString,
                _registered_method=True)
        self.GetSampleRate = channel.unary_unary(
                '/bos.History/GetSampleRate',
                request_serializer=comms__pb2.SetRequest.SerializeToString,
                response_deserializer=comms__pb2.SetResponse.FromString,
                _registered_method=True)
        self.SetSampleRate = channel.unary_unary(
                '/bos.History/SetSampleRate',
                request_serializer=comms__pb2.SetRequest.SerializeToString,
                response_deserializer=comms__pb2.SetResponse.FromString,
                _registered_method=True)
        self.RefreshRates = channel.unary_unary(
                '/bos.History/RefreshRates',
                request_serializer=comms__pb2.RefreshRatesRequest.SerializeToString,
                response_deserializer=comms__pb2.RefreshRatesResponse.FromString,
                _registered_method=True)


class HistoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetHistory(self, request, context):
        """returns rows of history from the historian
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSampleRate(self, request, context):
        """set the sample rate of a given point
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetSampleRate(self, request, context):
        """set the sample rate of a given point
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RefreshRates(self, request, context):
        """remotely trigger an update of the rates used by the historian.
        this may be removed in future updates and its functionality triggered
        by SetSampleRate.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HistoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistory,
                    request_deserializer=comms__pb2.HistoryRequest.FromString,
                    response_serializer=comms__pb2.HistoryResponse.SerializeToString,
            ),
            'GetSampleRate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSampleRate,
                    request_deserializer=comms__pb2.SetRequest.FromString,
                    response_serializer=comms__pb2.SetResponse.SerializeToString,
            ),
            'SetSampleRate': grpc.unary_unary_rpc_method_handler(
                    servicer.SetSampleRate,
                    request_deserializer=comms__pb2.SetRequest.FromString,
                    response_serializer=comms__pb2.SetResponse.SerializeToString,
            ),
            'RefreshRates': grpc.unary_unary_rpc_method_handler(
                    servicer.RefreshRates,
                    request_deserializer=comms__pb2.RefreshRatesRequest.FromString,
                    response_serializer=comms__pb2.RefreshRatesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bos.History', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bos.History', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class History(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.History/GetHistory',
            comms__pb2.HistoryRequest.SerializeToString,
            comms__pb2.HistoryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSampleRate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.History/GetSampleRate',
            comms__pb2.SetRequest.SerializeToString,
            comms__pb2.SetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetSampleRate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.History/SetSampleRate',
            comms__pb2.SetRequest.SerializeToString,
            comms__pb2.SetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RefreshRates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bos.History/RefreshRates',
            comms__pb2.RefreshRatesRequest.SerializeToString,
            comms__pb2.RefreshRatesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
