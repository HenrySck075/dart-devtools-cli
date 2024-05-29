from typing import TypedDict
from vm import Response

class HttpProfile(Response):
    timestamp: int
    requests: list[HttpProfileRequestReference]

class _HttpProfileRequestReferenceRequired(Response):
    id: str
    isolateId: str
    method: str
    uri: str
    events: list[HttpProfileRequestEvent]
    startTime: int
class HttpProfileRequestReference(_HttpProfileRequestReferenceRequired,total=False):
    endTime: int
    request: HttpProfileRequestData
    response: HttpProfileResponseData

class HttpProfileRequest(HttpProfileRequestReference,total=False):
    requestBody: list[int]
    responseBody: list[int]

class HttpProfileRequestData(TypedDict,total=False):
    contentLength: int
    cookies: list[str]
    error: str
    followRedirects: bool
    maxRedirects: int
    persistentConnection: bool
    proxyDetails: HttpProfileProxyData

class HttpProfileResponseData(TypedDict,total=False):
    cookies: list[str]
    compressionState: str
    reasonPhrase: str
    isRedirect: bool
    persistentConnection: bool
    contentLength: int
    statusCode: int
    startTime: int
    endTime: int
    error: str

class HttpProfileProxyData(TypedDict,total=False):
    host: str
    username: str
    isDirect: bool
    port: int

class HttpProfileRequestEvent(TypedDict):
    event: str
    timestamp: int
