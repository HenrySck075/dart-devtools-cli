from pathlib import PurePath
from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Type, Union
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container
from textual.driver import Driver
from textual.widget import Widget
from textual.widgets import TabbedContent, Static
from websocket import WebSocket, WebSocketApp, create_connection 
import json,sys,asyncio

if TYPE_CHECKING:
    from vm import Event
from e import WebSocket2
from pages.home import Home
from pages.inspector import Inspector


CSSPathType = Union[
    str,
    PurePath,
    List[Union[str, PurePath]],
]

_events: dict[str, list[Callable[["Event"],Coroutine[Any, Any, None]]]] = {}
async def n(name,event:"Event"):
    for i in _events.get(name,[]):
        await i(event)
def on_ws_message(idk: WebSocket):
    while idk.connected:
        j = json.loads(idk.recv())
        if j.get("method", '') == 'streamNotify':
            asyncio.ensure_future(n(j["params"]["streamId"],j["params"]["event"]))

def yield_patch(w:Widget):
    with Container():
        yield from w.compose()

class DartDevtoolsCLI(App):
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        meow = sys.argv[1].replace("http","ws")+"ws"
        print("Connecting to "+meow)
        self._ws: WebSocket2 = create_connection(meow,class_=WebSocket2,enable_multithread=True)#type: ignore
        "yes i did it like this"

        # Listen to event
        for i in []:#["Debug", "Service"]:
            self._ws.send_json("streamListen",{"streamId": i})

    def compose(self) -> ComposeResult:
        with TabbedContent("Home","Inspector","Timeline","Memory","Performance","Debugger","Network","Logging"):
            yield from yield_patch(Home(self._ws))
            yield from yield_patch(Inspector(self._ws))
            yield Static("jjejdn")
            yield Static("maymory")
            yield Static("speed")
            yield Static("i need it")
            yield Static("s")
            yield Static("word abuse")

        
        


if __name__ == "__main__":
    DartDevtoolsCLI().run()
