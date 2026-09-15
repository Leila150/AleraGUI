"""Unified mouse, keyboard, touch, pen, wheel, gesture and gamepad input."""
from __future__ import annotations
from dataclasses import dataclass, field
from time import monotonic

@dataclass(frozen=True)
class InputEvent:
    type: str; x: float=0; y: float=0; timestamp: float=field(default_factory=monotonic)
    device: str="unknown"; pointer_id: int=0; button: str|None=None; key: str|None=None
    modifiers: frozenset=frozenset(); pressure: float=0; delta_x: float=0; delta_y: float=0; data: dict=field(default_factory=dict)

@dataclass(frozen=True)
class MouseEvent(InputEvent): device: str="mouse"
@dataclass(frozen=True)
class TouchEvent(InputEvent): device: str="touch"
@dataclass(frozen=True)
class PenEvent(InputEvent): device: str="pen"
@dataclass(frozen=True)
class KeyEvent(InputEvent): device: str="keyboard"
@dataclass(frozen=True)
class GamepadEvent(InputEvent): device: str="gamepad"

class InputRouter:
    def __init__(self): self.handlers={}; self.capture={}; self.focused=None
    def on(self,event,callback): self.handlers.setdefault(event,[]).append(callback); return callback
    def off(self,event,callback):
        if callback in self.handlers.get(event,[]): self.handlers[event].remove(callback)
    def dispatch(self,event):
        for cb in tuple(self.handlers.get(event.type,())): cb(event)
        target=self.capture.get(event.pointer_id) or self.focused
        if target is not None and hasattr(target,"emit"): target.emit(event.type,event)
        return event
    def capture_pointer(self,pointer_id,widget): self.capture[pointer_id]=widget
    def release_pointer(self,pointer_id): self.capture.pop(pointer_id,None)
    def set_focus(self,widget):
        self.focused=widget
        if widget is not None and hasattr(widget,"emit"): widget.emit("focus")

class GestureEngine:
    def __init__(self): self._start={}; self.threshold=8
    def feed(self,event):
        if event.type in ("touch_down","pointer_down"): self._start[event.pointer_id]=event
        elif event.type in ("touch_up","pointer_up"): self._start.pop(event.pointer_id,None)
    def distance(self,a,b): return ((b.x-a.x)**2+(b.y-a.y)**2)**0.5
