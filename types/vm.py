from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from stubs.vm import *

else:
    Event = dict
    Isolate = dict 
    IsolateReference = dict 
    IsolateGroup = dict
    IsolateGroupReference = dict 
    InstanceReference = dict 
    Instance = dict
