from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GET_ERROR_NONE: _ClassVar[GetError]
    GET_ERROR_UNSPECIFIED: _ClassVar[GetError]
    GET_ERROR_KEY_DOES_NOT_EXIST: _ClassVar[GetError]
    GET_ERROR_TIMEOUT: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_DRIVER: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_ADDR: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_XREF: _ClassVar[GetError]
    GET_ERROR_ACCESS_DENIED: _ClassVar[GetError]

class SetError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SET_ERROR_NONE: _ClassVar[SetError]
    SET_ERROR_UNSPECIFIED: _ClassVar[SetError]
    SET_ERROR_KEY_DOES_NOT_EXIST: _ClassVar[SetError]
    SET_ERROR_TIMEOUT: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_DRIVER: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_ADDR: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_XREF: _ClassVar[SetError]
    SET_ERROR_ACCESS_DENIED: _ClassVar[SetError]
    SET_ERROR_READ_ONLY: _ClassVar[SetError]
    SET_ERROR_INVALID_VALUE_TYPE: _ClassVar[SetError]

class QueryError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_ERROR_NONE: _ClassVar[QueryError]
    QUERY_ERROR_UNSPECIFIED: _ClassVar[QueryError]
    QUERY_ERROR_TIMEOUT: _ClassVar[QueryError]
    QUERY_ERROR_UNKNOWN_PREFIX: _ClassVar[QueryError]
    QUERY_ERROR_ACCESS_DENIED: _ClassVar[QueryError]

class Dtype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[Dtype]
    NULL: _ClassVar[Dtype]
    DOUBLE: _ClassVar[Dtype]
    FLOAT: _ClassVar[Dtype]
    INT32: _ClassVar[Dtype]
    INT64: _ClassVar[Dtype]
    UINT32: _ClassVar[Dtype]
    UINT64: _ClassVar[Dtype]
    SINT32: _ClassVar[Dtype]
    SINT64: _ClassVar[Dtype]
    FIXED32: _ClassVar[Dtype]
    FIXED64: _ClassVar[Dtype]
    SFIXED32: _ClassVar[Dtype]
    SFIXED64: _ClassVar[Dtype]
    BOOL: _ClassVar[Dtype]
    STRING: _ClassVar[Dtype]
    BYTES: _ClassVar[Dtype]
    POINT_ID: _ClassVar[Dtype]
    POINT_ID_LIST: _ClassVar[Dtype]
    DEVICE_ID: _ClassVar[Dtype]
    DEVICE_ID_LIST: _ClassVar[Dtype]
    DRIVER_ID: _ClassVar[Dtype]
    DRIVER_XREF: _ClassVar[Dtype]
GET_ERROR_NONE: GetError
GET_ERROR_UNSPECIFIED: GetError
GET_ERROR_KEY_DOES_NOT_EXIST: GetError
GET_ERROR_TIMEOUT: GetError
GET_ERROR_COULD_NOT_RESOLVE_DRIVER: GetError
GET_ERROR_COULD_NOT_RESOLVE_ADDR: GetError
GET_ERROR_COULD_NOT_RESOLVE_XREF: GetError
GET_ERROR_ACCESS_DENIED: GetError
SET_ERROR_NONE: SetError
SET_ERROR_UNSPECIFIED: SetError
SET_ERROR_KEY_DOES_NOT_EXIST: SetError
SET_ERROR_TIMEOUT: SetError
SET_ERROR_COULD_NOT_RESOLVE_DRIVER: SetError
SET_ERROR_COULD_NOT_RESOLVE_ADDR: SetError
SET_ERROR_COULD_NOT_RESOLVE_XREF: SetError
SET_ERROR_ACCESS_DENIED: SetError
SET_ERROR_READ_ONLY: SetError
SET_ERROR_INVALID_VALUE_TYPE: SetError
QUERY_ERROR_NONE: QueryError
QUERY_ERROR_UNSPECIFIED: QueryError
QUERY_ERROR_TIMEOUT: QueryError
QUERY_ERROR_UNKNOWN_PREFIX: QueryError
QUERY_ERROR_ACCESS_DENIED: QueryError
UNSPECIFIED: Dtype
NULL: Dtype
DOUBLE: Dtype
FLOAT: Dtype
INT32: Dtype
INT64: Dtype
UINT32: Dtype
UINT64: Dtype
SINT32: Dtype
SINT64: Dtype
FIXED32: Dtype
FIXED64: Dtype
SFIXED32: Dtype
SFIXED64: Dtype
BOOL: Dtype
STRING: Dtype
BYTES: Dtype
POINT_ID: Dtype
POINT_ID_LIST: Dtype
DEVICE_ID: Dtype
DEVICE_ID_LIST: Dtype
DRIVER_ID: Dtype
DRIVER_XREF: Dtype

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Header(_message.Message):
    __slots__ = ("Src", "Dst")
    SRC_FIELD_NUMBER: _ClassVar[int]
    DST_FIELD_NUMBER: _ClassVar[int]
    Src: str
    Dst: str
    def __init__(self, Src: _Optional[str] = ..., Dst: _Optional[str] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("Header", "Key")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Key: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Key: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("Header", "Key", "Value", "Dtype", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Key: str
    Value: str
    Dtype: Dtype
    Error: GetError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Key: _Optional[str] = ..., Value: _Optional[str] = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., Error: _Optional[_Union[GetError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class GetMultipleRequest(_message.Message):
    __slots__ = ("Header", "Keys")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GetMultipleResponse(_message.Message):
    __slots__ = ("Header", "Responses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Responses: _containers.RepeatedCompositeFieldContainer[GetResponse]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Responses: _Optional[_Iterable[_Union[GetResponse, _Mapping]]] = ...) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ("Header", "Key", "Value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Key: str
    Value: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Key: _Optional[str] = ..., Value: _Optional[str] = ...) -> None: ...

class SetResponse(_message.Message):
    __slots__ = ("Header", "Ok", "Key", "Value", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Ok: bool
    Key: str
    Value: str
    Error: SetError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Ok: bool = ..., Key: _Optional[str] = ..., Value: _Optional[str] = ..., Error: _Optional[_Union[SetError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class SetMultipleRequest(_message.Message):
    __slots__ = ("Header", "Requests")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Requests: _containers.RepeatedCompositeFieldContainer[SetRequest]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Requests: _Optional[_Iterable[_Union[SetRequest, _Mapping]]] = ...) -> None: ...

class SetMultipleResponse(_message.Message):
    __slots__ = ("Header", "Responses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Responses: _containers.RepeatedCompositeFieldContainer[SetResponse]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Responses: _Optional[_Iterable[_Union[SetResponse, _Mapping]]] = ...) -> None: ...

class PointQueryRequest(_message.Message):
    __slots__ = ("Header", "Device", "Types", "Names", "Locations", "ConsiderDeviceLoc", "Dtype", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    CONSIDERDEVICELOC_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Device: str
    Types: _containers.RepeatedScalarFieldContainer[str]
    Names: _containers.RepeatedScalarFieldContainer[str]
    Locations: _containers.RepeatedScalarFieldContainer[str]
    ConsiderDeviceLoc: bool
    Dtype: Dtype
    Error: QueryError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Device: _Optional[str] = ..., Types: _Optional[_Iterable[str]] = ..., Names: _Optional[_Iterable[str]] = ..., Locations: _Optional[_Iterable[str]] = ..., ConsiderDeviceLoc: bool = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., Error: _Optional[_Union[QueryError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("Header", "Key", "Value", "Dtype", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Key: str
    Value: str
    Dtype: Dtype
    Error: QueryError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Key: _Optional[str] = ..., Value: _Optional[str] = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., Error: _Optional[_Union[QueryError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...
