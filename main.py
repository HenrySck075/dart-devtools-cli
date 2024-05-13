from pathlib import PurePath
from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Type, Union
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container
from textual.driver import Driver
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, TabbedContent, Static
from websocket import enableTrace 
import time,sys,asyncio,threading

if TYPE_CHECKING:
    from vm import Event, VM
else:
    VM = dict
from e import WebSocket2
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
    _vm = reactive({},recompose=True)
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, "j.tcss", watch_css)
        self.styles.layers = ("below", "above") # type: ignore      

        meow = sys.argv[1].replace("http","ws")+"ws"
        print("Connecting to "+meow)
        ws: WebSocket2 = WebSocket2(meow,on_reconnect=lambda b,v: print("whar"))#type: ignore
        self._ws = ws 
        #self._e = WebSocketApp(meow,on_message=on_ws_message)
        self._isolate = ""
        def j(data: VM):
            self._isolate = data["isolates"][0]["id"]
            time.sleep(0.5)
            self._vm = data
        threading.Thread(target=ws.run_forever,daemon=True).start()
        time.sleep(1)
        ws.send_json("getVM",on_message=j)

        # Listen to event
        for i in []:#["Debug", "Service"]:
            ws.send_json(self._e,"streamListen",{"streamId": i})

    def compose(self) -> ComposeResult:
        if self._vm == {}:
            yield Static("Please wait")
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
        
        
        


if __name__ == "__main__":
    DartDevtoolsCLI().run()
