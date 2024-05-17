import asyncio
import time
from typing import TYPE_CHECKING, Generic, TypeVar
from textual import reactive
from textual.app import ComposeResult, LayoutDefinition, events
from textual.containers import Container, Horizontal, Vertical
from textual.geometry import SpacingDimensions
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Static, Tree

from e import JsonRpc

if TYPE_CHECKING:
    from flutter import LayoutNode
    from vm import Event
else:
    Event = dict
    LayoutNode = dict
    FlutterWidget = dict
    idk = TypeVar("idk", contravariant=True)
    class ExtensionResult(Generic[idk], dict):
        pass

class LayoutExplorer(Widget):
    def __init__(self, ws: JsonRpc, isolateId: str) -> None:
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

    treeSummary = reactive.reactive(None)
    "this does not recompose, even when recompose=True"

    def __init__(self, ws: JsonRpc) -> None:
        super().__init__(name="DevtoolsInspector")
        self.styles.height = "auto"
        self._ws = ws
        self._isolate = ws.isolate["id"]
        async def h(): 
            self.treeSummary = await ws.send_json("ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews", {"groupName": "tree_1", "isolateId": self._isolate})
            await self.recompose()
        asyncio.ensure_future(h())
        time.sleep(0.5)
        self._layoutExplorer = LayoutExplorer(self._ws,self._isolate)
        self._node = None

    def compose(self) -> ComposeResult:
        with Vertical() as tf:
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
            with Horizontal():
                if self.treeSummary != None:
                    root = self.treeSummary["result"]
                    t = Tree("[root]",id="treee")
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
                    t = Tree("",id="treee")
                    t.styles.width = 30
                    yield t
                yield self._layoutExplorer 
            with Vertical() as console:
                console.styles.height = 10 # 7 for output, 3 for eval
                out = Static()
                async def on_log(e: Event):
                    out.update(out.renderable+"\n"+e["logRecord"]["message"].get("valueAsString","")) # type: ignore
                self._ws.addEventListener('Logging/Logging',on_log)
                yield out

    def on_checkbox_changed(self, e: Checkbox.Changed):
        if e.checkbox.id == "slowanim":
            coro = self._ws.send_json("ext.flutter.timeDilation", {"timeDilation":5 if e.value else 1, "isolateId": self._isolate})
        if e.checkbox.id == "debugpaint":
            coro = self._ws.send_json("ext.flutter.debugPaint", {"enabled":e.value, "isolateId": self._isolate})
        try: 
            asyncio.ensure_future(coro) # type: ignore # yes i know
        except NameError: pass

    def on_tree_node_highlighted(self, e: Tree.NodeHighlighted):
        self._node = e.node
    #def on_tree_node_selected(self, e: Tree.NodeSelected):
    #    self._layoutExplorer.displayNodeLayout(e.node.data)
    def on_key(self, e: events.Key):
        if e.key == "h":
            # TODO: where do they even get the groupName
            self._layoutExplorer.displayNodeLayout(self._node.data)
