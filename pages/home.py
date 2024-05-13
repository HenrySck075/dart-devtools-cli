from textual.app import ComposeResult
from textual.widget import Widget 
from textual.containers import Container
from textual.widgets import Label, Static

from e import WebSocket2


class Home(Widget):
    def __init__(self, ws: WebSocket2) -> None:
        super().__init__(name="DevtoolsHome")
        self.styles.height = "auto"
        self._ws = ws
        
        self.info = ws.send_json("getVM")

    def compose(self) -> ComposeResult:
        i = self.info
        with Container():
            yield Label(f"[b]CPU / OS:[/b] {i['hostCPU']} ({i['architectureBits']} bit) {i['operatingSystem']}")
            yield Label(f"[b]Dart Version:[/b] {i['version']}")
