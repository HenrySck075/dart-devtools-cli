import asyncio
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
        self.info2 = {}

        async def m():
            self.info2 = await self._ws.send_json("s0.flutterVersion", {"isolateId": self._ws.isolate['id']})
            await self.recompose()
        self.__idk__ = asyncio.ensure_future(m(),loop=asyncio.get_event_loop())

    def compose(self) -> ComposeResult:
        i = self.info
        i2 = self.info2
        yield Label(f"[b]CPU / OS:[/b] {i['hostCPU']} ({i['architectureBits']} bit) {i['operatingSystem']}")
        yield Label(f"[b]Dart Version:[/b] {i['version']}")
        if self.info2 != {}:
            yield Label(f"[b]Flutter Version:[/b] {i2['flutterVersion']} / {i2['channel']}")
            yield Label(f"[b]Framework / Engine[/b] {i2['frameworkRevisionShort']} / {i2['engineRevisionShort']}")
        
