"""Application/window lifecycle and declarative page registration."""
from __future__ import annotations
from .events import EventDispatcher

class Window(EventDispatcher):
    def __init__(self,**kwargs):
        super().__init__(); self.title=kwargs.get("title",""); self.icon=kwargs.get("icon",None); self.position=kwargs.get("position",(0,0)); self.size=kwargs.get("size",(800,600))
        self.min_size=kwargs.get("min_size",(100,100)); self.max_size=kwargs.get("max_size",None); self.resizable=kwargs.get("resizable",True); self.fullscreen=False; self.maximized=False; self.minimized=False
        self.always_on_top=False; self.opacity=1; self.transparent=False; self.decorations=True; self.content=None
    def set_content(self,content): self.content=content; return content
    def show(self): self.emit("show")
    def hide(self): self.emit("hide")
    def close(self): self.emit("close")

class Application:
    def __init__(self,**kwargs): self.windows=[]; self.pages={}; self.theme=kwargs.get("theme",None); self.running=False
    def window(self,**kwargs):
        w=Window(**kwargs); self.windows.append(w); return w
    def register_page(self,name,fn): self.pages[name]=fn; return fn
    def run(self):
        self.running=True
        if not self.windows: self.window(title="AleraGUI")
        return self
    def stop(self): self.running=False

class AleraGUI(Application):
    """Base class for an AleraGUI application."""
    @staticmethod
    def page(name=None):
        def decorator(fn): fn.__aleragui_page__=name or fn.__name__; return fn
        return decorator
    @staticmethod
    def command(name=None):
        def decorator(fn): fn.__aleragui_command__=name or fn.__name__; return fn
        return decorator
