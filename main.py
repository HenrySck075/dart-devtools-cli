from pathlib import PurePath
from typing import List, Type, Union
from textual.app import App, ComposeResult
from textual.driver import Driver
from textual.widgets import Tabs, Tab, TabbedContent, Static
from websocket import WebSocket
import json


CSSPathType = Union[
    str,
    PurePath,
    List[Union[str, PurePath]],
]

class DartDevtoolsCLI(App):
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        self._ws = WebSocket()
    def compose(self) -> ComposeResult:
        with TabbedContent("Home","Inspector","Timeline","Memory","Performance","Debugger","Network","Logging"):
            yield Static("uhm no")
            yield Static("s")
            yield Static("jjejdn")
            yield Static("maymory")
            yield Static("speed")
            yield Static("i need it")
            yield Static("s")
            yield Static("word abuse")
        


if __name__ == "__main__":
    DartDevtoolsCLI().run()
