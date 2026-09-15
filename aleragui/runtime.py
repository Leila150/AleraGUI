"""Useful runtime primitives connecting AleraGUI widgets into a real UI tree."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable

class DuplicateIDError(ValueError): pass

class IDRegistry:
    def __init__(self): self._items={}; self._counter=0
    def generate(self,prefix="widget"):
        while True:
            self._counter+=1; value=f"{prefix}-{self._counter}"
            if value not in self._items: return value
    def register(self,widget,widget_id=None):
        value=widget_id or getattr(widget,"id",None) or self.generate(type(widget).__name__.lower())
        if value in self._items and self._items[value] is not widget: raise DuplicateIDError(f"AleraGUI ID already exists: {value!r}")
        self._items[value]=widget; widget.id=value
        if not getattr(widget,"key",None): widget.key=value
        return value
    def unregister(self,widget_or_id):
        key=widget_or_id if isinstance(widget_or_id,str) else getattr(widget_or_id,"id",None)
        if key in self._items and (isinstance(widget_or_id,str) or self._items[key] is widget_or_id): del self._items[key]
    def get(self,widget_id,default=None): return self._items.get(widget_id,default)
    def __contains__(self,widget_id): return widget_id in self._items
    def all(self): return tuple(self._items.values())

@dataclass(frozen=True)
class HitResult:
    widget: Any
    local_position: tuple[float,float]
    path: tuple[Any,...]

def _rect(widget):
    rect=getattr(widget,"layout_rect",None)
    if rect is not None: return tuple(rect)
    x,y=getattr(widget,"position",(0,0)); w,h=getattr(widget,"size",(0,0))
    if isinstance(w,str) or isinstance(h,str): return None
    return float(x),float(y),float(w),float(h)

def hit_test(root,point):
    px,py=point
    def visit(node,ox,oy,ancestors):
        if not getattr(node,"visible",True) or not getattr(node,"enabled",True) or getattr(node,"opacity",1)<=0: return None
        rect=_rect(node)
        if rect is None: return None
        x,y,w,h=rect; ax,ay=ox+x,oy+y
        if not(ax<=px<=ax+w and ay<=py<=ay+h): return None
        path=ancestors+(node,)
        children=sorted(getattr(node,"children",()),key=lambda c:getattr(c,"z_index",0))
        for child in reversed(children):
            result=visit(child,ax,ay,path)
            if result is not None: return result
        return HitResult(node,(px-ax,py-ay),path)
    return visit(root,0.0,0.0,())

class EventRouter:
    def dispatch(self,target,event):
        from .events import Event
        if isinstance(event,str): event=Event(event,source=target)
        path=self._path(target); event.target=target; event.path=tuple(path)
        for node in path[:-1]:
            if event.stopped: return event
            event.current_target=node; node.emit(f"{event.type}:capture",event)
        if not event.stopped: event.current_target=target; target.emit(event.type,event)
        if event.bubbles:
            for node in reversed(path[:-1]):
                if event.stopped: break
                event.current_target=node; node.emit(event.type,event)
        return event
    @staticmethod
    def _path(target):
        path=[]; node=target
        while node is not None: path.append(node); node=getattr(node,"parent",None)
        return list(reversed(path))

class WidgetTree:
    def __init__(self,root=None): self.ids=IDRegistry(); self.root=None; self.set_root(root) if root is not None else None
    def set_root(self,root): self.root=root; self._register_recursive(root); return root
    def _register_recursive(self,node):
        self.ids.register(node,getattr(node,"id",None) or None)
        for child in getattr(node,"children",()): self._register_recursive(child)
    def register(self,widget): self.ids.register(widget,getattr(widget,"id",None) or None); return widget
    def unregister(self,widget):
        for child in tuple(getattr(widget,"children",())): self.unregister(child)
        self.ids.unregister(widget)
    def get(self,widget_id): return self.ids.get(widget_id)
    def find(self,predicate=None,**attrs):
        result=[]
        for node in self.walk():
            if predicate is not None and not predicate(node): continue
            if all(getattr(node,k,object())==v for k,v in attrs.items()): result.append(node)
        return result
    def first(self,predicate=None,**attrs):
        items=self.find(predicate,**attrs); return items[0] if items else None
    def query(self,selector):
        """Small selector language: '#id', '.style_class', or 'ClassName'."""
        if selector.startswith("#"): return self.find(id=selector[1:])
        if selector.startswith("."): return self.find(style_class=selector[1:])
        return self.find(lambda node:type(node).__name__==selector)
    def walk(self,node=None):
        node=self.root if node is None else node
        if node is None: return
        yield node
        for child in getattr(node,"children",()): yield from self.walk(child)

class FrameScheduler:
    def __init__(self,fps=60.0): self.fps=max(1.0,float(fps)); self.frame=0; self.running=False; self.last_time=monotonic(); self._callbacks=[]
    def add(self,callback):
        if callback not in self._callbacks: self._callbacks.append(callback)
        return callback
    def remove(self,callback):
        if callback in self._callbacks: self._callbacks.remove(callback)
    def tick(self,now=None):
        current=monotonic() if now is None else now; dt=max(0.0,current-self.last_time); self.last_time=current; self.frame+=1
        for callback in tuple(self._callbacks): callback(dt)
        return dt
    def step(self,frames=1):
        for _ in range(max(0,frames)): self.tick()
        return self.frame

class InvalidationQueue:
    def __init__(self): self._queue=[]; self._set=set()
    def add(self,widget):
        key=id(widget)
        if key not in self._set: self._set.add(key); self._queue.append(widget)
    def drain(self):
        items=tuple(self._queue); self._queue.clear(); self._set.clear(); return items
    def __len__(self): return len(self._queue)

__all__=["DuplicateIDError","IDRegistry","HitResult","hit_test","EventRouter","WidgetTree","FrameScheduler","InvalidationQueue"]
