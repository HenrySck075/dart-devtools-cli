from pathlib import PurePath
from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Type, Union
from textual.app import App, ComposeResult, log
from textual.containers import Horizontal, VerticalScroll
from textual.driver import Driver
from textual.reactive import reactive
from textual.widgets import Button, TabbedContent, Static
import sys,asyncio

if TYPE_CHECKING:
    from vm import Event, VM
else:
    VM = dict
from e import JsonRpc
from pages.home import Home
from pages.inspector import Inspector
from pages.debugger import Debugger
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
        self._ws = None
        self._isolate = ""

    def compose(self) -> ComposeResult:
        if self._vm == {}:
            yield Static("")
            self.notify("Connecting to "+self.meow)
            return
        with Horizontal():
            yield Button("Reload",id="r")
            yield Button("Restart",id="R")
        with VerticalScroll():
            with TabbedContent("Home","Inspector","Timeline","Memory","Performance","Debugger","Network","Logging"):
                yield Home(self._ws, self._vm) # type: ignore
                yield Inspector(self._ws)
                yield Static("jjejdn")
                yield Static("maymory")
                yield Static("speed")
                yield Debugger(self._ws)
                yield Static("s")
                yield Static("word abuse")

        
    async def on_ready(self, e):

        log("ujejejebegebyeybwbywbgwg w")
        ws = await JsonRpc().create(self.meow)
        self.notify("Connected :)")
        self._ws: Devtools = ws #type: ignore
        data:VM = await ws.send_json("getVM")
        self._isolate = data["isolates"][0]["id"]
        self._vm = data
        await self.recompose()

        # Listen to event
        for i in ["Debug"]:#["Debug", "Service"]:
            await ws.send_json("streamListen",{"streamId": i})
    async def on_button_pressed(self, e: Button.Pressed):
        if e.button.id == "r":
            await self._ws.send_json("s0.reloadSources",{"isolateId": self._isolate})
            self.notify("Hot reload completed")
        if e.button.id == "R":
            await self._ws.send_json("s0.hotRestart",{"isolateId": self._isolate})
            self.notify("Hot restart completed")

if __name__ == "__main__":
    asyncio.run(DartDevtoolsCLI().run_async())
