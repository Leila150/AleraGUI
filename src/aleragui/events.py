from __future__ import annotations
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable

@dataclass
class EventContext:
    source: Any = None
    name: str = ""
    handled: bool = False
    stopped: bool = False
    data: dict[str, Any] = field(default_factory=dict)
    def stop(self): self.stopped = True
    def prevent_default(self): self.handled = True

class Event:
    def __init__(self, name: str): self.name, self._handlers = name, []
    def connect(self, handler):
        if handler not in self._handlers: self._handlers.append(handler)
        return handler
    def disconnect(self, handler):
        if handler in self._handlers: self._handlers.remove(handler)
    def emit(self, *args, **kwargs):
        results = []
        for handler in tuple(self._handlers): results.append(handler(*args, **kwargs))
        return results
    __call__ = emit

class EventEmitter:
    def __init__(self): self._events: dict[str, Event] = {}
    def event(self, name): return self._events.setdefault(name, Event(name))
    def on(self, name, handler=None):
        e = self.event(name)
        if handler is None: return e.connect
        return e.connect(handler)
    def off(self, name, handler): self.event(name).disconnect(handler)
    def emit(self, name, *args, **kwargs): return self.event(name).emit(*args, **kwargs)

def event(name=None):
    def deco(fn):
        fn.__alera_event__ = name or fn.__name__
        return fn
    return deco

def on(name):
    def deco(fn): fn.__alera_on__ = name; return fn
    return deco

def bind(source, target=None):
    def deco(fn):
        fn.__alera_binding__ = (source, target)
        return fn
    return deco

def watch(source):
    def deco(fn): fn.__alera_watch__ = source; return fn
    return deco
