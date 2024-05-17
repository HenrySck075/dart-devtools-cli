from typing import TYPE_CHECKING, Literal, Text
from rich.segment import Segment
from rich.style import Style
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Input, OptionList, Static, TextArea
from textual import log

from e import JsonRpc
if TYPE_CHECKING:
    from vm import ScriptReference, Event
else:
    Event = dict

class MarkableTextArea(TextArea):
    def __init__(self, text: str = "", *, language: str | None = None, theme: str = "css", soft_wrap: bool = True, tab_behavior: Literal["focus", "indent"] = "focus", read_only: bool = False, show_line_numbers: bool = False, max_checkpoints: int = 50, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, valid_locations: list[int] = []) -> None:
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled)
        self.markers: list[int] = []
        "Marker locations. "
        self.validLocations = valid_locations

    BINDINGS = [
        ("enter", "mark()", "Set breakpoints")
    ]
    
    def action_mark(self):
        y = self.cursor_location[0]
        self.markers.append(y)
        self.refresh_line(y-self.scroll_y.__round__())
        self.post_message(self.Marked(y))

    def render_line(self, y: int):
        s = "  "
        color = "white"
        if self.validLocations.__len__() != 0 and self.cursor_location[0] not in self.validLocations:
            pass
        else:
            if y == self.cursor_location[0]-self.scroll_y.__round__():
                s = "● "
                color="#800000"
        if y+self.scroll_y.__round__() in self.markers: 
            s = "● "
            color="#FF0000"
            
        out = Strip.join([Strip([Segment(s, style=Style(color=color))]),super().render_line(y)])
        # TODO: impl
        return out

    class Marked(Message):
        def __init__(self, line: int) -> None:
            self.line = line
            super().__init__()

class Source(Widget):
    def __init__(self, ws:JsonRpc):
        super().__init__(name="k")
        self._ws = ws 
        self.scripts: dict[str, ScriptReference] = {}
        self.source = ""
        self.uri = ""
        self.sid = ""
        self.breakpointLocations = []

    async def on_show(self, e):
        if self.scripts.__len__() == 0:
            for s in (await self._ws.send_json("getScripts",{"isolateId": self._ws.isolate["id"]}))["scripts"]:
                self.scripts[s["uri"]] = s
            await self.load(self._ws.rootFileUri)
        
    async def load(self,uri:str):
        script = await self._ws.getObject(self.scripts[uri])
        self.sid = script["id"]
        self.source = script.get("source","")
        self.uri = uri
        self.breakpointLocations = [i[0]-1 for i in script.get("tokenPosTable",[])]
        await self.recompose()
    
    def compose(self) -> ComposeResult:
        if self.uri == "":
            return
        yield Input(self.uri)
        yield MarkableTextArea(self.source,read_only=True,soft_wrap=False,valid_locations=self.breakpointLocations)

    async def on_markable_text_area_marked(self, e: MarkableTextArea.Marked):
        await self._ws.send_json("addBreakpoint", {"line": e.line, "scriptId": self.sid, "isolateId": self._ws.isolate["id"]})

class Debugger(Widget):
    def __init__(self, ws:JsonRpc):
        super().__init__(name="DevtoolsDebugger")
        self.styles.height = "auto"
        self._ws = ws 
        self._debugListened = False
        self.breakpoints = ws.isolate["breakpoints"]
    DEFAULT_CSS = """
.box {
  border: solid $primary-lighten-3;
  height: 1fr
}
    """
    async def on_show(self):
        if not self._debugListened:
            async def _on_breakpoint_added(d: Event):
                self.breakpoints.append(d["breakpoint"]) # type: ignore
                await self.query_one("#uwu").recompose()

            async def _on_breakpoint_removed(d: Event):
                self.breakpoints.remove(d["breakpoint"]) # type: ignore
                await self.query_one("#uwu").recompose()

            self._ws.addEventListener("Debug/BreakpointAdded",_on_breakpoint_added)
            self._ws.addEventListener("Debug/BreakpointRemoved",_on_breakpoint_removed)
                
        self._debugListened = True
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="uwu") as v:
                v.styles.width = 25
                j = [":".join([i["location"]["script"]["uri"].split("/")[-1],i["location"]["line"].__str__(),i["location"]["column"].__str__()]) for i in self.breakpoints]
                with Container(classes="box") as callStack:
                    callStack.border_title = "Call Stack"
                with Container(classes="box") as variables:
                    variables.border_title = "Variables"
                with OptionList(*j,classes="box") as breakpoints:
                    breakpoints.border_title = "Breakpoints"
            yield Source(self._ws)
