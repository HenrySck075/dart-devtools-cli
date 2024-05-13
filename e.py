from typing import TYPE_CHECKING, Any, Literal, TypedDict, overload
from websocket import WebSocket
import json


def send_json(ws, method: str, params: dict = {}): # type: ignore
    h: dict[str,Any] = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": str(ws.id)
    }
    print(h)
    ws.send(json.dumps(h))
    try:
        while True:
            j = json.loads(ws.recv())
            print(j)
            if j["id"] != str(ws.id): continue
            ws.id+=1
            return j["result"]        
    except: ws.close()


if TYPE_CHECKING:
    from flutter import ExtensionResponse, Widget, LayoutNode
    from vm import VM, Isolate
    getIsolate = TypedDict("getIsolate", {"isolateId": str})
    streamListen = TypedDict("streamListen", {"streamId": str})
    getRootWidgetSummaryTreeWithPreviews = TypedDict("getRootWidgetSummaryTreeWithPreviews", {"groupName":str, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})

class WebSocket2(WebSocket):
    def __init__(self, get_mask_key=None, sockopt=None, sslopt=None, fire_cont_frame: bool = False, enable_multithread: bool = True, skip_utf8_validation: bool = False, **_):
        super().__init__(get_mask_key, sockopt, sslopt, fire_cont_frame, enable_multithread, skip_utf8_validation, **_)
        self.id = 0
    
    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getVM"]) -> VM:...
        @overload 
        def send_json(self, method: Literal["getIsolate"],params: getIsolate) -> Isolate:...
        @overload
        def send_json(self, method: Literal["streamListen"],params: streamListen) -> Isolate:...

        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews"], params: getRootWidgetSummaryTreeWithPreviews) -> ExtensionResponse[Widget]:...
        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getLayoutExplorerNode"], params: getLayoutExplorerNode) -> ExtensionResponse[LayoutNode]:...


    def send_json(self, method: str, params: dict = {}): # type: ignore
        return send_json(self,method,params)
