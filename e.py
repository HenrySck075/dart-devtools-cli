import asyncio
from threading import Thread
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal, TypedDict, overload
from aiohttp import ClientSession
from textual import log


if TYPE_CHECKING:
    from flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
    from vm import VM, Isolate, Event
    getIsolate = TypedDict("getIsolate", {"isolateId": str})
    streamListen = TypedDict("streamListen", {"streamId": str})
    getRootWidgetSummaryTreeWithPreviews = TypedDict("getRootWidgetSummaryTreeWithPreviews", {"groupName":str, "isolateId": str})
    timeDilation = TypedDict("timeDilation", {"timeDilation":int, "isolateId": str})
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})
else:
    Event = dict

class JsonRpc:
    def __init__(self) -> None:
        self.queued_recv = {}
        self.queued_event: dict[str,list[Callable[[Event],Coroutine[Any,Any,None]]]] = {}
        self.rpcid = 0
        self.session = ClientSession()
        
    async def create(self,*args,**kwargs):
        "real"
        self._ws = await self.session.ws_connect(*args,**kwargs)
        async def h():
            async for msg in self._ws:
                print(msg)
                j = msg.json()
                if "result" in j.keys():
                    log(j["id"] in self.queued_recv)
                    await self.queued_recv.pop(j["id"], lambda n: None)(j["result"])
                elif j.get("method","") == "streamNotify":
                    for i in self.queued_event.get(j["params"]["streamId"]+"/"+j["params"]["event"]["kind"],[]):
                        await i(j["params"]["event"])

        asyncio.ensure_future(h(),loop=asyncio.get_event_loop())
        return self
    
    def addEventListener(self, event:str, listener: Callable[[Event],Coroutine[Any,Any,None]]):
        if event not in self.queued_event:
            self.queued_event[event] = []
        self.queued_event[event].append(listener)

    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getVM"], params = {}) -> Coroutine[Any,Any,VM]:...
        @overload 
        def send_json(self, method: Literal["getIsolate"],params: getIsolate) -> Coroutine[Any,Any,Isolate]:...
        @overload
        def send_json(self, method: Literal["streamListen"],params: streamListen) -> Coroutine[Any,Any,Isolate]:...

        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews"], params: getRootWidgetSummaryTreeWithPreviews) -> Coroutine[Any,Any,ExtensionResult[Widget]]:...
        @overload 
        def send_json(self, method: Literal["ext.flutter.inspector.getLayoutExplorerNode"], params: getLayoutExplorerNode) -> Coroutine[Any,Any,ExtensionResult[LayoutNode]]:...
        @overload 
        def send_json(self, method: Literal["ext.flutter.timeDilation"], params: timeDilation) -> Coroutine[Any,Any,TimeDilationResponse]:...
        @overload
        def send_json(self, method: Literal["ext.flutter.debugPaint"], params: debugPaint) -> Coroutine[Any,Any,DebugPaintResponse]:...
 
    async def send_json(self, method: str, params: dict = {}) -> dict: # type: ignore
        global rpcid
        h: dict[str,Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(self.rpcid)
        }
        
        j = None 
        async def get(data):
            nonlocal j
            j =data 
        self.queued_recv[str(self.rpcid)] = get
        
        log(h)
        log(self.queued_recv)
        await self._ws.send_json(h)
        self.rpcid+=1
        while j==None:
            await asyncio.sleep(0.2)
        return j
        #return (await self._ws.receive_json())["result"]
