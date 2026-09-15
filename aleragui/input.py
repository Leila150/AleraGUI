"""Unified pointer, keyboard, touch and gesture primitives."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot

@dataclass
class Pointer:
    x: float; y: float; button: str="left"; pointer_id: int=0; pressure: float=1.0
@dataclass
class Key:
    key: str; text: str=""; modifiers: frozenset=frozenset(); repeat: bool=False
@dataclass
class Touch:
    x: float; y: float; id: int=0; pressure: float=1.0

class GestureRecognizer:
    def __init__(self, threshold=8): self.threshold=threshold; self._start={}
    def begin(self,touch): self._start[touch.id]=(touch.x,touch.y)
    def end(self,touch):
        start=self._start.pop(touch.id,None)
        if not start: return None
        dx,dy=touch.x-start[0],touch.y-start[1]
        if hypot(dx,dy)<self.threshold: return "tap"
        if abs(dx)>abs(dy): return "swipe_right" if dx>0 else "swipe_left"
        return "swipe_down" if dy>0 else "swipe_up"

class FocusManager:
    def __init__(self): self.current=None
    def focus(self,widget):
        if self.current is widget: return
        if self.current: self.current.blur()
        self.current=widget
        if widget: widget.focus()
    def clear(self): self.focus(None)
