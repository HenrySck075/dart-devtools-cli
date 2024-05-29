from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from stubs.vm import *

else:
    Breakpoint = dict
    Event = dict
    Frame = dict
    Isolate = dict 
    IsolateReference = dict 
    IsolateGroup = dict
    IsolateGroupReference = dict 
    InstanceReference = dict 
    Instance = dict
    Response = dict
    Script = dict
    ScriptReference = dict
    ScriptList = dict
    Stack = dict
    TimelineEvent = dict
    VM = dict
