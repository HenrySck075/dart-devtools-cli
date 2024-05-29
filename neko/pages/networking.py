"""

Timeline event name: HTTP CLIENT response of {method}
Timeline args type: HttpClientResponse
"""

from datetime import datetime, timedelta
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import DataTable, TabbedContent
from e import JsonRpc
from textual.events import Show, Hide

class Networking(Widget):
    def __init__(self, ws: JsonRpc):
        super().__init__(name="DevtoolsNetworking")
        self._ws = ws
        self.inited = False
        self.shown = False 
        self.updatedSince = 0
        "i dont trust you"
    
    def _on_show(self, event: Show) -> None:
        self.shown = True
        return super()._on_show(event)
    def _on_hide(self, event: Hide) -> None:
        self.shown = False
        return super()._on_hide(event)

    async def on_ready(self):
        if not self.inited:
            async def j(e):
                if self.shown:
                    m = await self._ws.send_json("ext.dart.io.getHttpProfile", {"isolateId": self._ws.isolate["id"], "updatedSince":self.updatedSince})
                    d = self.query_one("j", DataTable)
                    for i in m["requests"]:
                        d.add_row(
                            i["method"],
                            i["uri"],
                            i["response"]["statusCode"], #type: ignore
                            i["type"],
                            i.get("endTime",0)-i["startTime"],
                            timedelta(i["startTime"])
                        )
                    self.updatedSince = int(datetime.now().timestamp())
            self._ws.addTimelineEventListener("HTTP CLIENT response of GET", j)
        self.inited = True


    def compose(self) -> ComposeResult:
        with Horizontal():
            d = DataTable(id="j")
            d.add_columns('Method', "Uri", "Status", "Type", "Duration", "Timestamp")
            yield d

            #with Container():
            #    with TabbedContent([""])

