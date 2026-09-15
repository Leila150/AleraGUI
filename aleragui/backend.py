"""Platform backend contracts. Concrete backends can target native/GPU APIs."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class PlatformInfo:
    name: str="unknown"; version: str=""; density: float=1.0; touch: bool=False; mouse: bool=True; keyboard: bool=True; gpu: bool=False

class Backend:
    platform="generic"
    def __init__(self): self.info=PlatformInfo(name=self.platform)
    def initialize(self, app): pass
    def run(self, app): app._running=True
    def stop(self, app): app._running=False
    def create_window(self, **kwargs): raise NotImplementedError
    def present(self, window, commands): pass
    def clipboard_get(self): return ""
    def clipboard_set(self,text): pass
    def open_file(self, **kwargs): raise NotImplementedError
    def save_file(self, **kwargs): raise NotImplementedError
    def notify(self,title,message,**kwargs): pass

class HeadlessBackend(Backend):
    platform="headless"
    def create_window(self, **kwargs): return kwargs

class BackendRegistry:
    def __init__(self): self._backends={}
    def register(self,name,backend): self._backends[name]=backend; return backend
    def get(self,name): return self._backends[name]
    def names(self): return tuple(self._backends)

backends=BackendRegistry(); backends.register("headless",HeadlessBackend())
