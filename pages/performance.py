from textual.widget import Widget
from textual.widgets import Sparkline

from e import JsonRpc


class Performance(Widget):
    def __init__(self, ws: JsonRpc):
        super().__init__(name="DevtoolsPerformance")
        self._ws = ws
