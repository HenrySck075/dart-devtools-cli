from typing import Generic, Literal, TypeVar, TypedDict

"""

"""
class idk(TypedDict):
    file: str 
    line: int
    column: int
    name: str

class Node(TypedDict):
    description: str
    type: str
    hasChildren: bool
    allowWrap: bool
    valueId: str
    locationId: int
    creationLocation: idk
    createdByLocalProject: bool
    summaryTree: bool
    style: str
class Widget(Node):
    textPreview: str 
    children: list[Widget]
    widgetRuntimeType: bool
    stateful: bool
class ExtensionResponse(TypedDict):
    method: str
    type: Literal["_extensionType"]
R = TypeVar("R", contravariant=True)
class ExtensionResult(Generic[R],ExtensionResponse):
    result: R

class TimeDilationResponse(ExtensionResponse):
    timeDilation: str
class DebugPaintResponse(ExtensionResponse):
    enabled: bool

class _RenderObjectPropertyRequired(Node):
    allowNameWrap: bool
    properties: list[RenderObjectProperty]
    ifNull: str
    missingIfNull: bool
    propertyType: str
    defaultLevel: str
class RenderObjectProperty(_RenderObjectPropertyRequired, total=False):
    tooltip: str
    isDiagnosticableValue: bool

class RenderObject(Node):
    properties: list[RenderObjectProperty]
class BoxConstraints(TypedDict):
    type: str
    description: str
    minWidth: str
    minHeigh: str
    maxWidth: str
    maxHeight: str
class BoxSize(TypedDict):
    width: str 
    height: str
class LayoutNode(Widget):
    renderObject: RenderObject
    parentRenderElement: LayoutNode
    constraints: BoxConstraints 
    isBox: bool
    size: BoxSize 
    """
    "properties": [
        {
            "description": "[Directionality]",
            "type": "DiagnosticsProperty<Set<InheritedElement>>",
            "name": "dependencies",
            "style": "singleLine",
            "allowNameWrap": true,
            "valueId": "inspector-74",
            "summaryTree": true,
            "properties": [],
            "missingIfNull": false,
            "propertyType": "Set<InheritedElement>",
            "defaultLevel": "info"
        },
        {
            "description": "_RenderAppBarTitleBox#68394 relayoutBoundary=up13",
            "type": "DiagnosticsProperty<RenderObject>",
            "name": "renderObject",
            "style": "singleLine",
            "allowNameWrap": true,
            "valueId": "inspector-70",
            "summaryTree": true,
            "properties": [
                {
                    "description": "<none> (can use size)",
                    "type": "DiagnosticsProperty<ParentData>",
                    "name": "parentData",
                    "style": "singleLine",
                    "allowNameWrap": true,
                    "valueId": "inspector-71",
                    "summaryTree": true,
                    "ifNull": "MISSING",
                    "tooltip": "can use size",
                    "missingIfNull": true,
                    "propertyType": "ParentData",
                    "defaultLevel": "info"
                },
                {
                    "description": "BoxConstraints(0.0<=w<=1248.0, 0.0<=h<=56.0)",
                    "type": "DiagnosticsProperty<Constraints>",
                    "name": "constraints",
                    "style": "singleLine",
                    "allowNameWrap": true,
                    "valueId": "inspector-72",
                    "summaryTree": true,
                    "ifNull": "MISSING",
                    "missingIfNull": true,
                    "propertyType": "Constraints",
                    "defaultLevel": "info"
                },
                {
                    "description": "Size(277.1, 28.0)",
                    "type": "DiagnosticsProperty<Size>",
                    "name": "size",
                    "style": "singleLine",
                    "allowNameWrap": true,
                    "valueId": "inspector-73",
                    "summaryTree": true,
                    "ifNull": "MISSING",
                    "missingIfNull": true,

                    "propertyType": "Size",
                    "defaultLevel": "info"
                },
                {
                    "description": "Alignment.center",
                    "type": "DiagnosticsProperty<AlignmentGeometry>",
                    "name": "alignment",
                    "style": "singleLine",
                    "allowNameWrap": true,
                    "valueId": "inspector-50",
                    "summaryTree": true,
                    "missingIfNull": false,
                    "propertyType": "AlignmentGeometry",
                    "defaultLevel": "info"
                },
                {
                    "description": "ltr",
                    "type": "EnumProperty<TextDirection>",
                    "name": "textDirection",
                    "style": "singleLine",
                    "allowNameWrap": true,
                    "valueId": "inspector-33",
                    "summaryTree": true,
                    "defaultValue": "null",
                    "missingIfNull": false,
                    "propertyType": "TextDirection",
                    "defaultLevel": "info"
                }
            ],
            "defaultValue": "null",
            "missingIfNull": false,
            "propertyType": "RenderObject",
            "defaultLevel": "info",
            "isDiagnosticableValue": true
        }
    ],
    """
    stateful: bool
