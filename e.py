import asyncio
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal, TypedDict, Union, overload
from warnings import warn
from aiohttp import ClientSession
from textual import log


from neko.ddstypes.s0 import FrameworkVersion
from neko.ddstypes.flutter import Widget, LayoutNode, TimeDilationResponse, ExtensionResult, DebugPaintResponse
from neko.ddstypes.vm import VM, Isolate, Event, ScriptList, Breakpoint, Script, ScriptReference, IsolateReference, Response, Stack, TimelineEvent
from neko.ddstypes.services import HttpProfile  
L = Literal
if TYPE_CHECKING:
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
    class getHttpProfile(RequiresIsolateId, total=True):
        updatedSince: int
    debugPaint = TypedDict("debugPaint", {"enabled":bool, "isolateId": str})
    getLayoutExplorerNode = TypedDict("getLayoutExplorerNode", {"groupName":str, "isolateId": str, "id": str, "subtreeDepth": str})

class IsolateExited(Exception):
    pass
class JsonRpc:
    def __init__(self) -> None:
        self.queued_recv = {}
        self.event_listeners: dict[str,list[Callable[[Event],Coroutine[Any,Any,None]]]] = {}
        self.timeline_listeners: dict[str,list[Callable[[TimelineEvent],Coroutine[Any,Any,None]]]] = {}
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
            def a(k, v):
                queued[k] = v
            "somehow these are still not catched"
            async for msg in self._ws:
                j = msg.json()
                if "result" in j.keys():
                    #if j["result"]["type"] == "Sentinel":
                    #    raise IsolateExited()
                    await self.queued_recv.pop(j["id"], lambda n: a(j["id"],j))(j["result"])
                elif j.get("method","") == "streamNotify":
                    n = j["params"]["streamId"]+"/"+j["params"]["event"]["kind"]
                    log("Calling event "+n)
                    if n != "Timeline/TimelineEvents":
                        for i in self.event_listeners.get(n,[]):
                            await i(j["params"]["event"])
                    else:
                        for e in j["params"]["event"]["timelineEvents"]:
                            for i in self.timeline_listeners.get(e["name"],[]):
                                await i(e)

                for k,v in queued:
                    await self.queued_recv.pop(k, lambda n: log("No catcher found for id "+k))(v)


        asyncio.ensure_future(h(),loop=asyncio.get_event_loop())
        self.vm = await self.send_json("getVM")
        self.isolate = await self.send_json("getIsolate",{"isolateId":self.vm["isolates"][0]["id"]})
        self.rootFileUri = self.isolate["rootLib"]["uri"] # type: ignore
        return self

    def addTimelineEventListener(self, eventName: str,listener: Callable[[TimelineEvent],Coroutine[Any,Any,None]] ):
        "j"
        #if listener in self.listened: raise ValueError("This function is already listened to an event.") # could be a bad idea, but meh just leave it like this
        if eventName not in self.timeline_listeners:
            self.timeline_listeners[eventName] = []
        self.timeline_listeners[eventName].append(listener)
        #self.listened.append(listener)
    
    def addEventListener(
        self, 
        event:Literal[
            "VM/VMUpdate",

            "Debug/PauseStart", "Debug/PauseExit", "Debug/PauseBreakpoint", "Debug/PauseInterrupted", "Debug/PauseException", "Debug/PausePostRequest", "Debug/Resume", "Debug/BreakpointAdded", "Debug/BreakpointResolved", "Debug/BreakpointRemoved", "Debug/BreakpointUpdated", "Debug/Inspect", "Debug/None",

            "Logging/Logging",

            "Timeline/TimelineEvents"
        ], 
        listener: Callable[[Event],Coroutine[Any,Any,None]]
    ):
        if listener in self.listened: raise ValueError("This function is already listened to an event.") # could be a bad idea, but meh just leave it like this
        if event not in self.event_listeners:
            self.event_listeners[event] = []
        self.event_listeners[event].append(listener)
        self.listened.append(listener)

    if TYPE_CHECKING:
        @overload 
        async def send_json(self, method: Literal["addBreakpoint"], params: addBreakpoint) -> Breakpoint:...
        @overload 
        async def send_json(self, method: Literal["removeBreakpoint"], params: removeBreakpoint):...
        @overload 
        def send_json(self, method: Literal["getObject"], params: getObject):...
        @overload 
        async def send_json(self, method: Literal["getStack"], params: RequiresIsolateId) -> Stack:...
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
        async def send_json(self, method: Literal["ext.dart.io.getHttpProfile"], params: getHttpProfile) -> HttpProfile:...

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
            await asyncio.sleep(0.05) # comedy
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


