from typing import TYPE_CHECKING, Generic, TypeVar


if TYPE_CHECKING:
    from stubs.flutter import *
else:
    LayoutNode = dict
    Node = dict
    Widget = dict 
    R = TypeVar("R",contravariant=True)
    class ExtensionResult(Generic[R],dict):
        pass 
    Location = dict
