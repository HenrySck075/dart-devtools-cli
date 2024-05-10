from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from websocket import WebSocket

from ..e import send


class Home(Widget):
    def __init__(self, ws: WebSocket) -> None:
        super().__init__(name="DevtoolsHome")
        self._ws = ws
        
        self.info = send(ws,"getVM")

    def compose(self) -> ComposeResult:
        i = self.info
        yield Static(f"[b]CPU / OS:[/b] {i['hostCPU']} ({i['architectureBits']} bit) {i['operatingSystem']}")
        yield Static(f"[b]Dart Version:[/b] {i['version']}")
