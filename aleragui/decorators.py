"""Declarative decorators used by AleraGUI."""
from __future__ import annotations
from functools import wraps

def _mark(**metadata):
    def deco(obj):
        current=dict(getattr(obj, "__aleragui_meta__", {})); current.update(metadata); obj.__aleragui_meta__=current; return obj
    return deco

def page(name=None): return _mark(kind="page", name=name)
def draw(fn=None):
    deco=_mark(kind="draw")
    return deco(fn) if fn else deco

def canvas_event(name=None): return _mark(kind="canvas_event", event=name)
def observable(obj): return _mark(observable=True)(obj)
def computed(fn): return _mark(computed=True)(fn)
def bind(*args, **kwargs): return _mark(kind="bind", args=args, kwargs=kwargs)
def watch(*args, **kwargs): return _mark(kind="watch", args=args, kwargs=kwargs)
def animatable(obj): return _mark(animatable=True)(obj)
def command(name=None, **kwargs): return _mark(kind="command", name=name, **kwargs)
def accessible(**kwargs): return _mark(accessible=True, **kwargs)
def shortcut(keys, **kwargs): return _mark(kind="shortcut", keys=keys, **kwargs)
def background(fn): return _mark(kind="background")(fn)
def task(fn): return _mark(kind="task")(fn)
def worker(fn): return _mark(kind="worker")(fn)
def validator(*args, **kwargs): return _mark(kind="validator", args=args, kwargs=kwargs)
def serializable(obj): return _mark(serializable=True)(obj)
def deserializable(obj): return _mark(deserializable=True)(obj)
