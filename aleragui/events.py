"""Unified GUI event primitives."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class Event:
    type: str
    source: Any = None
    data: dict = field(default_factory=dict)
    handled: bool = False
    stopped: bool = False
    def stop(self): self.stopped = True
    def prevent_default(self): self.handled = True

class EventDispatcher:
    def __init__(self): self._handlers = {}
    def on(self, event: str, callback: Callable):
        self._handlers.setdefault(event, []).append(callback); return callback
    def off(self, event: str, callback: Callable):
        if event in self._handlers and callback in self._handlers[event]: self._handlers[event].remove(callback)
    def emit(self, event: str, *args, **kwargs):
        results=[]
        for cb in tuple(self._handlers.get(event, ())):
            results.append(cb(*args, **kwargs))
        return results
    def clear_events(self): self._handlers.clear()

EVENTS = (
    "press","release","click","double_click","long_press","hover","enter","leave",
    "focus","blur","change","input","submit","scroll","drag_start","drag","drag_end",
    "drop","move","resize","show","hide","mount","unmount","key_down","key_up",
    "pointer_down","pointer_move","pointer_up","touch_down","touch_move","touch_up",
    "wheel","context_menu","cancel","load","error"
)
