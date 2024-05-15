import asyncio
from threading import Thread
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal, TypedDict, overload
from warnings import warn
from aiohttp import ClientSession
from textual import log 

if TYPE_CHECKING:
    from s0 import FrameworkVersion
    from flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
    from vm import VM, Isolate, Event, ScriptList, ObjectReference, Script, ScriptReference, IsolateReference, Response 
    RequiresIsolateId = TypedDict("RequiresIsolateId", {"isolateId": str})
    getIsolate = RequiresIsolateId
    streamListen = TypedDict("streamListen", {"streamId": str})
    class getRootWidgetSummaryTreeWithPreviews(getIsolate):
        groupName: str

    class timeDilation(getIsolate):
        timeDilation: int

    class getObject(getIsolate):
        objectId: str
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})
else:
    Event = dict

class JsonRpc:
    def __init__(self) -> None:
        self.queued_recv = {}
        self.queued_event: dict[str,list[Callable[[Event],Coroutine[Any,Any,None]]]] = {}
        self.listened = []
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
        if listener in self.listened: raise ValueError("This function is already listened to an event.") # could be a bad idea, but meh just leave it like this
        if event not in self.queued_event:
            self.queued_event[event] = []
        self.queued_event[event].append(listener)
        self.listened.append(listener)

    if TYPE_CHECKING:
        @overload 
        def send_json(self, method: Literal["getObject"], params: getObject):...

        @overload 
        def send_json(self, method: Literal["getVM"], params = {}) -> Coroutine[Any,Any,VM]:...
        @overload 
        def send_json(self, method: Literal["getScripts"], params = {}) -> Coroutine[Any,Any,ScriptList]:...
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

        @overload
        def send_json(self, method: Literal["s0.flutterVersion"], params: RequiresIsolateId) -> Coroutine[Any,Any,FrameworkVersion]:...
 
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


class Devtools:
    "some info about the vm that needs to be passed around the codebase"
    def __init__(self, ws: JsonRpc) -> None:
        self.ws = ws
        self.isolate = {}
        self.vm = {}
        self.rootFileUri = ""

    async def create(self):
        self.vm = await self.getVM()
        self.isolate = await self.getIsolate(self.vm["isolates"][0]["id"])
        self.rootFileUri = self.isolate["rootLib"]["uri"]


    async def getVM(self) -> VM:
        return await self.ws.send_json("getVM")

    async def getIsolate(self, isolateId: str) -> Isolate:
        return await self.ws.send_json("getIsolate", {"isolateId": isolateId})

    if TYPE_CHECKING:
        @overload 
        async def getObject(self, obj: ScriptReference, isolateId: str) -> Script:...
        @overload 
        async def getObject(self, obj: IsolateReference, isolateId: str) -> Isolate:...
    async def getObject(self, obj: Response | str, isolateId: str):
        if type(obj) == str: 
            objId = obj 
        else: 
            assert obj is str, "this will never hit, but pyright is stupid so"
            if not obj["type"].startswith("@"): 
                warn("Unnecessary request prevented: Object passes is not a reference.")
                return obj
            objId = obj["id"] # type: ignore
        return await self.ws.send_json("getObject", {"isolateId": isolateId, "objectId": objId})


