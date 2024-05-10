from typing import Any
from websocket import WebSocket
import json

id = 0
def send(ws: WebSocket, method: str, params: dict[str, Any] | None = None):
    global id
    id+=1
    h: dict[str,Any] = {
        "jsonrpc": "2.0",
        "method": method,
        "id": str(id)
    }
    if params is not None: h["params"] = params
    ws.send(json.dumps(params))
    return json.loads(ws.recv())["result"]
