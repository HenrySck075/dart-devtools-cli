from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable

from e import JsonRpc
from ..types.vm import Event


class Logging(Widget):
    def __init__(self,ws: JsonRpc):
        super().__init__(name="DevtoolsLogging")
        self._ws = ws 

    def compose(self) -> ComposeResult:
        d = DataTable()
        d.add_columns("When", "Kind", "Message")
        yield d

    def on_ready(self):
        async def on_log(e: Event):
            log = e["logRecord"]
            self.query_one(DataTable).add_row([log["time"], log["loggerName"], log["message"]])
        self._ws.addEventListener("Logging/Logging",on_log)
