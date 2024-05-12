from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.geometry import SpacingDimensions
from textual.widget import Widget
from textual.widgets import Button, Placeholder

from e import WebSocket2


class Inspector(Widget):
    "inspector gadget"

    def __init__(self, ws: WebSocket2) -> None:
        super().__init__(name="DevtoolsInspector")
        self._ws = ws

    def std(self,b: Button):
        b.styles.width = "1fr"
        return b


    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("Select widget")
            with Horizontal(classes="control") as j:
                j.styles.layout = "grid"
                yield self.std(Button("Slow Animations"))
                yield self.std(Button("Show Guidelines"))
                yield self.std(Button("Show Baselines"))
                yield self.std(Button("Highlight Repaints"))
                yield self.std(Button("Highlight Oversized Images"))
