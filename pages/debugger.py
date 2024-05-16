from typing import TYPE_CHECKING, Literal, Text
from rich.segment import Segment
from rich.style import Style
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Input, Static, TextArea

from e import Devtools
if TYPE_CHECKING:
    from vm import ScriptReference

class MarkableTextArea(TextArea):
    def __init__(self, text: str = "", *, language: str | None = None, theme: str = "css", soft_wrap: bool = True, tab_behavior: Literal["focus", "indent"] = "focus", read_only: bool = False, show_line_numbers: bool = False, max_checkpoints: int = 50, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled)
        self.marks: dict[int, list[int]] = {}
        "Marker locations. Format: {y1: [x1,x2,...],...}"

    def render_line(self, y: int):
        s = "  "
        color = "black"
        if y == self.cursor_location[0]-self.scroll_y or y in self.marks:
            s = "● "
            if y in self.marks: color="#F00"
        
        out = Strip.join([Strip([Segment(s, style=Style(color=color))]),super().render_line(y)])
        # TODO: impl
        return out

class Source(Widget):
    def __init__(self, ws:Devtools):
        super().__init__(name="k")
        self._ws = ws 
        self.scripts: dict[str, ScriptReference] = {}
        self.source = ""
        self.uri = ""

    async def on_show(self, e):
        for s in (await self._ws.ws.send_json("getScripts",{"isolateId": self._ws.isolate["id"]}))["scripts"]:
            self.scripts[s["uri"]] = s
        await self.load(self._ws.rootFileUri)
        
    async def load(self,uri:str):
        self.source = (await self._ws.getObject(self.scripts[uri])).get("source","")
        self.uri = uri
        self.log("j")
        await self.recompose()
    
    def compose(self) -> ComposeResult:
        if self.uri == "":
            return
        yield Input(self.uri)
        yield MarkableTextArea(self.source,read_only=True,soft_wrap=False)

        

class Debugger(Widget):
    def __init__(self, ws:Devtools):
        super().__init__(name="DevtoolsDebugger")
        self.styles.height = "auto"
        self._ws = ws 
    DEFAULT_CSS = """
.box {
  border: solid cyan;
}
    """
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical() as v:
                v.styles.width = 25
                with Container(classes="box") as callStack:
                    callStack.border_title = "Call Stack"
                with Container(classes="box") as variables:
                    variables.border_title = "Variables"
                with Container(classes="box") as breakpoints:
                    breakpoints.border_title = "Breakpoints"
            yield Source(self._ws)
        yield Static("gay")
