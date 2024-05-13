from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict, overload
from websocket import WebSocket, WebSocketApp
import json

rpcid = 0



if TYPE_CHECKING:
    from flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
    from vm import VM, Isolate
    getIsolate = TypedDict("getIsolate", {"isolateId": str})
    streamListen = TypedDict("streamListen", {"streamId": str})
    getRootWidgetSummaryTreeWithPreviews = TypedDict("getRootWidgetSummaryTreeWithPreviews", {"groupName":str, "isolateId": str})
    timeDilation = TypedDict("timeDilation", {"timeDilation":int, "isolateId": str})
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})

class WebSocket2(WebSocketApp):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.pop("on_message","")
        super().__init__(*args, **kwargs, on_message=lambda j,v:self.on_genuinely_send_help_please(v))
        self.queued_recv = {}
        self.queued_events = {}
    
    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getVM"], params = {}, on_message: Callable[[VM],None]|None = None):...
        @overload 
        def send_json(self, method: Literal["getIsolate"],params: getIsolate, on_message: Callable[[Isolate],None]|None = None):...
        @overload
        def send_json(self, method: Literal["streamListen"],params: streamListen, on_message: Callable[[Isolate],None]|None = None):...

        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews"], params: getRootWidgetSummaryTreeWithPreviews, on_message: Callable[[ExtensionResult[Widget]],None]|None = None):...
        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getLayoutExplorerNode"], params: getLayoutExplorerNode, on_message: Callable[[ExtensionResult[LayoutNode]],None]|None = None):...
        @overload 
        def send_json(self, method: Literal["ext.flutter.timeDilation"], params: timeDilation, on_message: Callable[[TimeDilationResponse],None]|None = None):...
        @overload
        def send_json(self, method: Literal["ext.flutter.debugPaint"], params: debugPaint, on_message: Callable[[DebugPaintResponse],None]|None = None):...
    
    def on_genuinely_send_help_please(self, data: str):
        print(data)
        try:
            j = json.loads(data)

            if "result" in j.keys(): 
                self.queued_recv.pop(j["id"])(j["result"])
            else:
                for i in self.queued_events.get(j["params"]["streamId"]+"/"+j["params"]["event"]["kind"],[]): i(j["params"]["event"])

        except: self.close()
    @staticmethod
    def j(d):
        pass

    def send_json(self, method: str, params: dict = {}, on_message: Callable[[dict],None]|None = None): # type: ignore
        global rpcid
        h: dict[str,Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(rpcid)
        }
        print(h)
        self.queued_recv[str(rpcid)] = on_message if on_message!=None else WebSocket2.j
        self.send(json.dumps(h))
        rpcid+=1
