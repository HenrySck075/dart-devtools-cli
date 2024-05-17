import asyncio
from threading import Thread
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal, TypedDict, Union, overload
from warnings import warn
from aiohttp import ClientSession
from textual import log

L = Literal
if TYPE_CHECKING:
    from s0 import FrameworkVersion
    from flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
    from vm import VM, Isolate, Event, ScriptList, Breakpoint, Script, ScriptReference, IsolateReference, Response 
    RequiresIsolateId = TypedDict("RequiresIsolateId", {"isolateId": str})
    getIsolate = RequiresIsolateId
    streamListen = TypedDict("streamListen", {"streamId": str})
    class getRootWidgetSummaryTreeWithPreviews(getIsolate):
        groupName: str

    class timeDilation(getIsolate):
        timeDilation: int

    class getObject(getIsolate):
        objectId: str

    class addBreakpoint(RequiresIsolateId):
        line: int
        scriptId: str
    class removeBreakpoint(RequiresIsolateId):
        breakpointId: str
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})
else:
    Event = dict
    VM = dict
    Isolate = dict
    Response = dict
class IsolateExited(Exception):
    pass
class JsonRpc:
    def __init__(self) -> None:
        self.queued_recv = {}
        self.queued_event: dict[str,list[Callable[[Event],Coroutine[Any,Any,None]]]] = {}
        self.listened = []
        self.rpcid = 0
        self.session = ClientSession()

        self.isolate = {}
        self.vm = {}
        self.rootFileUri = ""
        
    async def create(self,*args,**kwargs):
        "real"
        self._ws = await self.session.ws_connect(*args,**kwargs)
        async def h():
            queued = {}
            "somehow these are still not catched"
            async for msg in self._ws:
                j = msg.json()
                if "result" in j.keys():
                    #if j["result"]["type"] == "Sentinel":
                    #    raise IsolateExited()
                    await self.queued_recv.pop(j["id"], lambda n: log("No response catcher found for id "+j["id"]))(j["result"])
                elif j.get("method","") == "streamNotify":
                    n = j["params"]["streamId"]+"/"+j["params"]["event"]["kind"]
                    log("Calling event "+n)
                    for i in self.queued_event.get(n,[]):
                        await i(j["params"]["event"])

        asyncio.ensure_future(h(),loop=asyncio.get_event_loop())
        self.vm = await self.send_json("getVM")
        self.isolate = await self.send_json("getIsolate",{"isolateId":self.vm["isolates"][0]["id"]})
        self.rootFileUri = self.isolate["rootLib"]["uri"]
        return self
    
    def addEventListener(
        self, 
        event:Literal[
            "VM/VMUpdate",

            "Debug/PauseStart", "Debug/PauseExit", "Debug/PauseBreakpoint", "Debug/PauseInterrupted", "Debug/PauseException", "Debug/PausePostRequest", "Debug/Resume", "Debug/BreakpointAdded", "Debug/BreakpointResolved", "Debug/BreakpointRemoved", "Debug/BreakpointUpdated", "Debug/Inspect", "Debug/None",

            "Logging/Logging"
        ], 
        listener: Callable[[Event],Coroutine[Any,Any,None]]
    ):
        if listener in self.listened: raise ValueError("This function is already listened to an event.") # could be a bad idea, but meh just leave it like this
        if event not in self.queued_event:
            self.queued_event[event] = []
        self.queued_event[event].append(listener)
        self.listened.append(listener)

    if TYPE_CHECKING:
        @overload 
        async def send_json(self, method: Literal["addBreakpoint"], params: addBreakpoint) -> Breakpoint:...
        @overload 
        async def send_json(self, method: Literal["removeBreakpoint"], params: removeBreakpoint):...
        @overload 
        def send_json(self, method: Literal["getObject"], params: getObject):...
        @overload 
        async def send_json(self, method: Literal["getVM"], params = {}) -> VM:...
        @overload 
        async def send_json(self, method: Literal["getScripts"], params = {}) -> ScriptList:...
        @overload 
        async def send_json(self, method: Literal["getIsolate"],params: getIsolate) -> Isolate:...
        @overload
        async def send_json(self, method: Literal["streamListen"],params: streamListen) -> Isolate:...

        @overload 
        async def send_json(self, method: Literal["ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews"], params: getRootWidgetSummaryTreeWithPreviews) -> ExtensionResult[Widget]:...
        @overload 
        async def send_json(self, method: Literal["ext.flutter.inspector.getLayoutExplorerNode"], params: getLayoutExplorerNode) -> ExtensionResult[LayoutNode]:...
        @overload 
        async def send_json(self, method: Literal["ext.flutter.timeDilation"], params: timeDilation) -> TimeDilationResponse:...
        @overload
        async def send_json(self, method: Literal["ext.flutter.debugPaint"], params: debugPaint) -> DebugPaintResponse:...

        @overload
        async def send_json(self, method: Literal["s0.flutterVersion"], params: RequiresIsolateId) -> FrameworkVersion:...
        @overload
        async def send_json(self, method: Literal["s0.reloadSources"], params: RequiresIsolateId) -> FrameworkVersion:...
        @overload
        async def send_json(self, method: Literal["s0.hotRestart"], params: RequiresIsolateId) -> FrameworkVersion:...
 
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
        
        await self._ws.send_json(h)
        self.rpcid+=1
        while j==None:
            await asyncio.sleep(0.1)
        return j
        #return (await self._ws.receive_json())["res


    if TYPE_CHECKING:
        @overload 
        async def getObject(self, obj: ScriptReference) -> Script:...
        @overload 
        async def getObject(self, obj: IsolateReference) -> Isolate:...
    async def getObject(self, obj: Response | str):
        if type(obj) == str: 
            objId = obj 
        elif type(obj) == Response: 
            if not obj["type"].startswith("@"): 
                warn("Unnecessary request prevented: Object passes is not a reference.")
                return obj
            objId = obj["id"] # type: ignore
        else:
            objId = "no"
        return await self.send_json("getObject", {"isolateId": self.isolate["id"], "objectId": objId})


