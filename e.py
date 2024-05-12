from typing import TYPE_CHECKING, Any, Literal, TypedDict, overload
from websocket import WebSocket
import json

if TYPE_CHECKING:
    from vm import VM, Isolate
getIsolate = TypedDict("getIsolate", {"isolateId": str})
class WebSocket2(WebSocket):
    def __init__(self, get_mask_key=None, sockopt=None, sslopt=None, fire_cont_frame: bool = False, enable_multithread: bool = True, skip_utf8_validation: bool = False, **_):
        super().__init__(get_mask_key, sockopt, sslopt, fire_cont_frame, enable_multithread, skip_utf8_validation, **_)
        self.id = 0
    
    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getVM"]) -> VM:...
        @overload 
        def send_json(self, method: Literal["getIsolate"],params: getIsolate) -> Isolate:...


    def send_json(self, method: str, params: dict = {}): # type: ignore
        h: dict[str,Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(self.id)
        }
        print(h)
        self.send(json.dumps(h))
        try:
            while True:
                j = json.loads(self.recv())
                print(j)
                if j["id"] != str(self.id): continue
                self.id+=1
                return j["result"]        
        except: self.close()

