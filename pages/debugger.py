from typing import TYPE_CHECKING, Literal, Text
from rich.segment import Segment
from rich.style import Style
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets.option_list import Option
from textual.message import Message
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Input, OptionList, TextArea
from textual import log

from e import JsonRpc
if TYPE_CHECKING:
    from vm import ScriptReference, Event, Breakpoint
else:
    from not_typing import *

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
        if y not in self.markers:
            self.markers.append(y)
            self.post_message(self.Marked(y+1))
        else: 
            self.markers.remove(y)
            self.post_message(self.Unmarked(y+1))
        self.refresh_line(y-self.scroll_y.__round__())

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

    class Unmarked(Message):
        def __init__(self, line: int) -> None:
            self.line = line
            super().__init__()
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
        self.bps = {}
        self.breakpointableLocations = []

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
        self.breakpointableLocations = [i[0]-1 for i in script.get("tokenPosTable",[])]
        self.bps = {}
        await self.recompose()
    
    def compose(self) -> ComposeResult:
        if self.uri == "":
            return
        yield Input(self.uri)
        d = MarkableTextArea(self.source,read_only=True,soft_wrap=False,valid_locations=self.breakpointableLocations,show_line_numbers=True)
        d.markers = [i["location"].get("line",0) for i in self._ws.isolate.get("breakpoints",[])]
        yield d

    async def on_markable_text_area_unmarked(self, e: MarkableTextArea.Unmarked):
        await self._ws.send_json("removeBreakpoint", {"breakpointId": self.bps[e.line], "isolateId": self._ws.isolate["id"]})
    async def on_markable_text_area_marked(self, e: MarkableTextArea.Marked):
        self.bps[e.line] = (await self._ws.send_json("addBreakpoint", {"line": e.line, "scriptId": self.sid, "isolateId": self._ws.isolate["id"]}))["id"]


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
                self.query_one("#bp",OptionList).add_option(self.construct_bp_option(d["breakpoint"]))

            async def _on_breakpoint_removed(d: Event):
                self.breakpoints.remove(d["breakpoint"]) # type: ignore
                self.query_one("#bp",OptionList).remove_option(d["breakpoint"]["breakpointNumber"].__str__())

            self._ws.addEventListener("Debug/BreakpointAdded",_on_breakpoint_added)
            self._ws.addEventListener("Debug/BreakpointRemoved",_on_breakpoint_removed)
                
        self._debugListened = True

    def construct_bp_option(self, i:Breakpoint):
        return Option(":".join([i["location"]["script"]["uri"].split("/")[-1],i["location"]["line"].__str__()]),id=i["breakpointNumber"].__str__()) # type: ignore
    def on_option_list_option_selected(self, e:OptionList.OptionSelected):
        self.query_one(MarkableTextArea).cursor_location = (int(e.option.prompt.split(":")[1])-1,0)
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="uwu") as v:
                v.styles.height = "auto"
                
                v.styles.width = 25
                j = [self.construct_bp_option(i) for i in self.breakpoints]
                with Container(classes="box") as callStack:
                    callStack.border_title = "Call Stack"
                with Container(classes="box") as variables:
                    variables.border_title = "Variables"
                with OptionList(*j,classes="box",id="bp") as breakpoints:
                    breakpoints.border_title = "Breakpoints"
            yield Source(self._ws)
