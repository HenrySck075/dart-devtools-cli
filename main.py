from pathlib import PurePath
from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Type, Union
from textual.app import App, ComposeResult, RenderResult, log
from textual.containers import Container
from textual.driver import Driver
from textual.reactive import reactive
from textual.widgets import Label, TabbedContent, Static
import time,sys,asyncio,aiohttp

if TYPE_CHECKING:
    from vm import Event, VM
else:
    VM = dict
from e import JsonRpc
from pages.home import Home
from pages.inspector import Inspector
#enableTrace(True)

CSSPathType = Union[
    str,
    PurePath,
    List[Union[str, PurePath]],
]

_events: dict[str, list[Callable[["Event"],Coroutine[Any, Any, None]]]] = {}
async def n(name,event:"Event"):
    for i in _events.get(name,[]):
        await i(event)

class DartDevtoolsCLI(App):
    CSS = """.borderless {
    border: none;
    padding: 0 
}"""
    _vm = reactive({})
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, "j.tcss", watch_css)
        self.styles.layers = ("below", "above") # type: ignore      

        self.meow = sys.argv[1].replace("http","ws")+"ws"
        print("Connecting to "+self.meow)
        self._ws = None
        self._isolate = ""


    def compose(self) -> ComposeResult:
        if self._vm == {}:
            yield Static(str(self._vm))
            return
        with TabbedContent("Home","Inspector","Timeline","Memory","Performance","Debugger","Network","Logging"):
            yield Home(self._ws, self._vm) # type: ignore
            yield Inspector(self._ws,self._isolate)
            yield Static("jjejdn")
            yield Static("maymory")
            yield Static("speed")
            yield Static("i need it")
            yield Static("s")
            yield Static("word abuse")

        
    async def on_ready(self, e):

        log("ujejejebegebyeybwbywbgwg w")
        ws = await JsonRpc().create(self.meow)
        self._ws: JsonRpc = ws #type: ignore
        data:VM = await ws.send_json("getVM")
        self._isolate = data["isolates"][0]["id"]
        self._vm = data
        await self.recompose()

        # Listen to event
        for i in []:#["Debug", "Service"]:
            await ws.send_json("streamListen",{"streamId": i})


if __name__ == "__main__":
    asyncio.run(DartDevtoolsCLI().run_async())
