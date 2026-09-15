"""Unified high-level input model for mouse, touch, pen, keyboard and gamepads."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class DeviceKind(str,Enum): MOUSE='mouse'; TOUCH='touch'; PEN='pen'; KEYBOARD='keyboard'; GAMEPAD='gamepad'; ACCESSIBILITY='accessibility'
@dataclass
class InputEvent:
    kind:DeviceKind; type:str; x:float=0; y:float=0; button:int|None=None; key:str|None=None; modifiers:set[str]=field(default_factory=set); pressure:float=0; device_id:str|None=None; data:dict[str,Any]=field(default_factory=dict); handled:bool=False
    def stop(self): self.handled=True; return self

@dataclass
class PointerState:
    x:float=0; y:float=0; pressed:bool=False; pressure:float=0; buttons:set[int]=field(default_factory=set)

class InputManager:
    def __init__(self): self.handlers:dict[str,list[Callable]]={}; self.pointer=PointerState(); self.focus=None; self.capture=None
    def on(self,event,handler): self.handlers.setdefault(event,[]).append(handler); return handler
    def off(self,event,handler):
        if event in self.handlers and handler in self.handlers[event]: self.handlers[event].remove(handler)
    def dispatch(self,event:InputEvent):
        if event.type.startswith('pointer'): self.pointer.x,self.pointer.y=event.x,event.y
        for handler in tuple(self.handlers.get(event.type,())):
            if event.handled: break
            result=handler(event)
            if result is True:event.handled=True
        return event
    def capture_pointer(self,target): self.capture=target; return target
    def release_pointer(self): self.capture=None
    def set_focus(self,target): self.focus=target; return target

class ShortcutManager:
    def __init__(self): self.bindings={}
    def register(self,shortcut,callback): self.bindings[shortcut]=callback; return callback
    def trigger(self,shortcut,*args,**kwargs):
        callback=self.bindings.get(shortcut)
        return callback(*args,**kwargs) if callback else None

class Gesture:
    def __init__(self,name,callback=None,threshold=8): self.name=name; self.callback=callback; self.threshold=threshold
class GestureManager:
    names=('tap','double_tap','long_press','drag','swipe','pinch','rotate','pan','scroll','fling','hover','press','release')
    def __init__(self): self.gestures={}
    def register(self,name,callback=None,threshold=8): self.gestures[name]=Gesture(name,callback,threshold); return self.gestures[name]
