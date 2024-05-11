from typing import TypedDict

"""

"""
class idk(TypedDict):
    file: str 
    line: int
    column: int
    name: str
class Widget(TypedDict):
    description: str
    type: str
    style: str
    hasChildren: bool
    allowWrap: bool
    valueId: str
    summaryTree: bool
    locationId: int
    creationLocation: idk
    createdByLocalProject: bool
    textPreview: str 
    children: list[Widget]
    widgetRuntimeType: bool
    stateful: bool
