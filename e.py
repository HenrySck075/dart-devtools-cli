from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict, overload
from websocket import WebSocket, WebSocketApp
import json

from websockets import WebSocketClientProtocol




if TYPE_CHECKING:
    from flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
    from vm import VM, Isolate
    getIsolate = TypedDict("getIsolate", {"isolateId": str})
    streamListen = TypedDict("streamListen", {"streamId": str})
    getRootWidgetSummaryTreeWithPreviews = TypedDict("getRootWidgetSummaryTreeWithPreviews", {"groupName":str, "isolateId": str})
    timeDilation = TypedDict("timeDilation", {"timeDilation":int, "isolateId": str})
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})

class WebSocketJsonProtocol(WebSocketClientProtocol):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.rpcid = 0
    
    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getVM"], params = {}) -> VM:...
        @overload 
        def send_json(self, method: Literal["getIsolate"],params: getIsolate) -> Isolate:...
        @overload
        def send_json(self, method: Literal["streamListen"],params: streamListen) -> Isolate:...

        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews"], params: getRootWidgetSummaryTreeWithPreviews) -> ExtensionResult[Widget]:...
        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getLayoutExplorerNode"], params: getLayoutExplorerNode) -> ExtensionResult[LayoutNode]:...
        @overload 
        def send_json(self, method: Literal["ext.flutter.timeDilation"], params: timeDilation) -> TimeDilationResponse:...
        @overload
        def send_json(self, method: Literal["ext.flutter.debugPaint"], params: debugPaint) -> DebugPaintResponse:...
    
    async def send_json(self, method: str, params: dict = {}): # type: ignore
        global rpcid
        h: dict[str,Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(self.rpcid)
        }
        print(h)
        await self.send(json.dumps(h))
        self.rpcid+=1
