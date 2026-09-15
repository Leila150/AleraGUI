"""Application and window lifecycle for AleraGUI."""
from __future__ import annotations
from .events import Event, EventDispatcher
from .runtime import WidgetTree, FrameScheduler, EventRouter, hit_test

class Window(EventDispatcher):
    def __init__(self,**kwargs):
        super().__init__(); self.id=kwargs.get("id") or None; self.title=kwargs.get("title",""); self.icon=kwargs.get("icon"); self.position=kwargs.get("position",(0,0)); self.size=kwargs.get("size",(800,600)); self.min_size=kwargs.get("min_size",(100,100)); self.max_size=kwargs.get("max_size"); self.resizable=kwargs.get("resizable",True); self.fullscreen=kwargs.get("fullscreen",False); self.maximized=False; self.minimized=False; self.always_on_top=False; self.opacity=1; self.transparent=False; self.decorations=True; self.content=None; self.visible=False
        self.tree=WidgetTree(); self.scheduler=FrameScheduler(kwargs.get("fps",60))
    def set_content(self,content):
        self.content=content; self.tree.set_root(content); self.emit("layout",content); return content
    def find(self,widget_id): return self.tree.get(widget_id)
    def hit_test(self,point): return hit_test(self.content,point) if self.content is not None else None
    def dispatch(self,target,event): return EventRouter().dispatch(target,event)
    def show(self): self.visible=True; self.emit("show",self); return self
    def hide(self): self.visible=False; self.emit("hide",self); return self
    def close(self): self.visible=False; self.emit("close",self); return self
    def frame(self,now=None): return self.scheduler.tick(now)

class Application:
    def __init__(self,**kwargs):
        self.windows=[]; self.pages={}; self.theme=kwargs.get("theme"); self.running=False; self.scheduler=FrameScheduler(kwargs.get("fps",60)); self.main_window=None
    def window(self,**kwargs):
        w=Window(**kwargs); self.windows.append(w); self.main_window=self.main_window or w; return w
    def register_page(self,name,fn): self.pages[name]=fn; return fn
    def build(self): return None
    def run(self):
        self.running=True
        if not self.windows: self.window(title="AleraGUI")
        built=self.build()
        if built is not None: self.main_window.set_content(built)
        self.main_window.show(); self.emit("start") if hasattr(self,"emit") else None
        return self
    def frame(self,now=None):
        dt=self.scheduler.tick(now)
        for window in tuple(self.windows): window.frame(now)
        return dt
    def stop(self):
        self.running=False
        for window in self.windows: window.hide()
        return self

class AleraGUI(Application,EventDispatcher):
    """Base class for an AleraGUI application; no routing framework is imposed."""
    def __init__(self,**kwargs): EventDispatcher.__init__(self); Application.__init__(self,**kwargs); self._collect_pages()
    def _collect_pages(self):
        for name in dir(self):
            value=getattr(self,name)
            page_name=getattr(value,"__aleragui_page__",None)
            if page_name: self.pages[page_name]=value
    @staticmethod
    def page(name=None):
        def decorator(fn): fn.__aleragui_page__=name or fn.__name__; return fn
        return decorator
    @staticmethod
    def command(name=None):
        def decorator(fn): fn.__aleragui_command__=name or fn.__name__; return fn
        return decorator
