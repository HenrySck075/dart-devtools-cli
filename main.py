from pathlib import PurePath
from typing import List, Type, Union
from textual.app import App, ComposeResult
from textual.driver import Driver
from textual.widgets import TabbedContent, Static
from websocket import WebSocket, WebSocketApp, create_connection 
import json,sys

from pages.home import Home


CSSPathType = Union[
    str,
    PurePath,
    List[Union[str, PurePath]],
]

class DartDevtoolsCLI(App):
    @staticmethod
    def on_ws_message(n: WebSocket, data: str):
        j = json.loads(data)
        if j.get("method", '') == 'streamNotify':...
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        self._ws = create_connection(sys.argv[1].replace("http","ws")+"/ws")
        self._event = WebSocketApp(sys.argv[1].replace("http","ws")+"/ws", on_message=DartDevtoolsCLI.on_ws_message)
        "yes i did it like this"

        # Listen to event
        for i in ["Debug", "Service"]:
            self._event.send(json.dumps({
                "jsonrpc": "2.0",
                "method": "streamListen",
                "params": {"streamId": i}
            }))
    def compose(self) -> ComposeResult:
        with TabbedContent("Home","Inspector","Timeline","Memory","Performance","Debugger","Network","Logging"):
            yield Home(self._ws) 
            yield Static("s")
            yield Static("jjejdn")
            yield Static("maymory")
            yield Static("speed")
            yield Static("i need it")
            yield Static("s")
            yield Static("word abuse")

        
        


if __name__ == "__main__":
    DartDevtoolsCLI().run()
