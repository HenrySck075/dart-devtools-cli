from __future__ import annotations

from typing import Callable, Generic, TypeVar, overload, Self

T = TypeVar("T")


def replace(value: T, proxies: dict[str, Callable]) -> T:
    for k,v in proxies:
        setattr(value, k, v)
    return value
