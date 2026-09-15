"""Unified GUI events with propagation and cancellation support."""
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
    default_prevented: bool = False
    bubbles: bool = True
    cancelable: bool = True
    target: Any = None
    current_target: Any = None
    path: tuple[Any, ...] = ()
    def stop(self): self.stopped=True; return self
    def stop_propagation(self): return self.stop()
    def prevent_default(self):
        if self.cancelable: self.default_prevented=True
        self.handled=True; return self

class EventDispatcher:
    def __init__(self): self._handlers={}
    def on(self,event,callback=None):
        if callback is None: return lambda fn:self.on(event,fn)
        self._handlers.setdefault(event,[]).append(callback); return callback
    def once(self,event,callback):
        def wrapper(*args,**kwargs):
            self.off(event,wrapper); return callback(*args,**kwargs)
        return self.on(event,wrapper)
    def off(self,event,callback):
        handlers=self._handlers.get(event,[])
        try: handlers.remove(callback)
        except ValueError: pass
        if not handlers: self._handlers.pop(event,None)
    def emit(self,event,*args,**kwargs):
        return [cb(*args,**kwargs) for cb in tuple(self._handlers.get(event,()))]
    def clear_events(self,event=None):
        if event is None: self._handlers.clear()
        else: self._handlers.pop(event,None)
    def listeners(self,event): return tuple(self._handlers.get(event,()))

EVENTS=(
    "press","release","click","double_click","long_press","hover","enter","leave",
    "focus","blur","change","input","submit","scroll","drag_start","drag","drag_end",
    "drop","move","resize","show","hide","mount","unmount","key_down","key_up",
    "pointer_down","pointer_move","pointer_up","touch_down","touch_move","touch_up",
    "wheel","context_menu","cancel","load","error","connect","disconnect","buffer",
    "progress","text_change","selection_change","value_change","layout","paint","destroy"
)
