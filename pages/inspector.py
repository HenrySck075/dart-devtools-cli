import asyncio
import time
from typing import TYPE_CHECKING, Generic, TypeVar
from textual.app import ComposeResult, LayoutDefinition, events
from textual.containers import Container, Horizontal, Vertical
from textual.geometry import SpacingDimensions
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Static, Tree

from e import WebSocket2
if TYPE_CHECKING:
    from flutter import LayoutNode, Widget as FlutterWidget, ExtensionResult
else:
    LayoutNode = dict
    FlutterWidget = dict
    idk = TypeVar("idk", contravariant=True)
    class ExtensionResult(Generic[idk], dict):
        pass

class LayoutExplorer(Widget):
    def __init__(self, ws: WebSocket2, isolateId: str) -> None:
        super().__init__(name="DevtoolsInspectorLayout")
        self._ws = ws
        self._isolate = isolateId
        self._output = [Static("Select a widget to view its layout")]
        self._node = None
        # self.styles.background = "$background-lighten-2"

    def compose(self) -> ComposeResult:
        yield from self._output

    def composeLayoutNodeBox(self, node: LayoutNode, sizeRatio = "1fr"):
        e = Container()
        e.styles.width = sizeRatio
        e.styles.height = sizeRatio
        e.border_title = node["description"] + " - " + node["renderObject"]["description"]
        e.styles.border_title_background = "$primary"
        e.styles.border_title_color = "black"
        e.styles.border  = ("solid", "$primary")
        return e

    def displayNodeLayout(self, node: LayoutNode):
        try:
            child = self.composeLayoutNodeBox(node, "0.7fr")
            child.styles.offset = (2,3)
            parent = self.composeLayoutNodeBox(node["parentRenderElement"])
            parent.styles.layer = "below"
            self._output = [parent, child]
        except Exception as e:
            self._output = [Static(e.__str__())]
        asyncio.ensure_future(self.recompose())
        


class Inspector(Widget):
    "inspector gadget"

    def __init__(self, ws: WebSocket2, isolateId: str) -> None:
        super().__init__(name="DevtoolsInspector")
        self.styles.height = "auto"
        self._ws = ws
        self._isolate = isolateId
        self.treeSummary = None 
        def h(data: ExtensionResult[FlutterWidget]): 
            self.treeSummary = data 
            asyncio.ensure_future(self.query_one("#treee").recompose())
        time.sleep(0.5)
        ws.send_json("ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews", {"groupName": "tree_1", "isolateId": isolateId},h)
        self._layoutExplorer = LayoutExplorer(self._ws,self._isolate)
        self._node = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal() as j:
                j.styles.height = 3
                yield Button("Select widget")
            with Horizontal() as idk:
                idk.styles.height = 2
                yield Checkbox("Slow Animations", classes="borderless", id="slowanim")
                yield Checkbox("Guidelines", classes="borderless", id="debugpaint")
                yield Checkbox("Baselines", classes="borderless")
                yield Checkbox("Highlight Repaints", classes="borderless")
                yield Checkbox("Highlight Oversized Images", classes="borderless")
            with Horizontal(id="treee"):
                if self.treeSummary != None:
                    root = self.treeSummary["result"]
                    t = Tree("[root]")
                    t.root.set_label("root")
                    t.root.data = root 
                    queue = [(t.root,root["children"])]
                    while queue.__len__()!=0:
                        new = []
                        for h in queue:
                            for i in h[1]:
                                n = h[0]
                                if len(i["children"]): 
                                    new.append((n.add(i["description"],i), i.pop("children"))) # type: ignore
                                else: n.add_leaf(i["description"],i)
                        queue = new
                    t.styles.width = 30
                    self._node = root
                    t.root.data.pop("children") # type: ignore
                    
                    yield t
                else: 
                    t = Tree("")
                    t.styles.width = 30
                    yield t
                yield self._layoutExplorer 

    def on_checkbox_changed(self, e: Checkbox.Changed):
        if e.checkbox.id == "slowanim":
            self._ws.send_json("ext.flutter.timeDilation", {"timeDilation":5 if e.value else 1, "isolateId": self._isolate})
        if e.checkbox.id == "debugpaint":
            self._ws.send_json("ext.flutter.debugPaint", {"enabled":e.value, "isolateId": self._isolate})

    def on_tree_node_highlighted(self, e: Tree.NodeHighlighted):
        self._node = e.node
    #def on_tree_node_selected(self, e: Tree.NodeSelected):
    #    self._layoutExplorer.displayNodeLayout(e.node.data)
    def on_key(self, e: events.Key):
        if e.key == "h":
            self._layoutExplorer.displayNodeLayout(self._node.data)
