from typing import TYPE_CHECKING
from textual.app import ComposeResult
from textual.widget import Widget 
from textual.containers import Container
from textual.widgets import Label, Static

from e import JsonRpc

if TYPE_CHECKING:
    from vm import VM
else: 
    VM = dict


class Home(Widget):
    def __init__(self, ws: JsonRpc, info: VM) -> None:
        super().__init__(name="DevtoolsHome")
        self.styles.height = "auto"
        self._ws = ws
        
        self.info = info 

    def compose(self) -> ComposeResult:
        i = self.info
        with Container():
            yield Label(f"[b]CPU / OS:[/b] {i['hostCPU']} ({i['architectureBits']} bit) {i['operatingSystem']}")
            yield Label(f"[b]Dart Version:[/b] {i['version']}")
