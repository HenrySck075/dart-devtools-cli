from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .stubs.services import *
else:
    HttpProfile = dict 
    HttpProfileRequest = dict
