from typing import TYPE_CHECKING, Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, Static, TextArea

from e import Devtools
if TYPE_CHECKING:
    from vm import ScriptReference

class MarkableTextArea(TextArea):
    def render_line(self, y: int):
        out = super().render_line(y)
        # TODO: impl
        return out

class Source(Widget):
    def __init__(self, ws:Devtools):
        super().__init__(name="k")
        self._ws = ws 
        self.scripts: dict[str, ScriptReference] = {}
        self.source = ""
        self.uri = ""

    async def on_ready(self, e):
        for s in (await self._ws.ws.send_json("getScripts"))["scripts"]:
            self.scripts[s["uri"]] = s
        
    async def load(self,uri:str):
        s = self.scripts[uri]
        self.uri = uri
    
    def compose(self) -> ComposeResult:
        if self.source == "":
            return
        yield Input(self.uri)
        yield MarkableTextArea(self.source,language="dart",read_only=True,soft_wrap=False)

        

class Debugger(Widget):
    def __init__(self, ws:Devtools):
        super().__init__(name="DevtoolsDebugger")
        self._ws = ws 
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical() as v:
                v.styles.width = 20
                with Container() as callStack:
                    callStack.border_title = "Call Stack"
                with Container() as variables:
                    variables.border_title = "Variables"
                with Container() as breakpoints:
                    breakpoints.border_title = "Breakpoints"
        yield Static("gay")
