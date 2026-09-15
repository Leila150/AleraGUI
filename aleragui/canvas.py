"""Backend-neutral 2D canvas, vector paths, brushes and layers."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .types import Color, Point, Rect, Gradient, Shadow

@dataclass
class Brush:
    color: Color|str="#000000"; size: float=1; opacity: float=1; hardness: float=1
    spacing: float=.1; smoothing: float=0; angle: float=0; rotation: float=0
    pressure: bool=True; texture: Any=None; blend_mode: str="normal"
    def clone(self): return Brush(**self.__dict__)

@dataclass
class Shape:
    kind: str
    data: dict = field(default_factory=dict)
    fill: Any = None
    stroke: Any = None
    stroke_width: float = 1
    opacity: float = 1
    rotation: float = 0
    scale: tuple = (1,1)
    visible: bool = True
    blend_mode: str = "normal"

@dataclass
class Layer:
    name: str="Layer"
    visible: bool=True
    opacity: float=1
    z_index: int=0
    blend_mode: str="normal"
    locked: bool=False
    shapes: list=field(default_factory=list)
    def add(self, item):
        if not self.locked: self.shapes.append(item)
        return item
    def remove(self, item):
        if item in self.shapes: self.shapes.remove(item)
    def clear(self):
        if not self.locked: self.shapes.clear()
    def show(self): self.visible=True
    def hide(self): self.visible=False

class LayerStack(list):
    def create(self, name="Layer"):
        layer=Layer(name=name, z_index=len(self)); self.append(layer); return layer
    def move_up(self, layer):
        i=self.index(layer)
        if i < len(self)-1: self[i],self[i+1]=self[i+1],self[i]
    def move_down(self, layer):
        i=self.index(layer)
        if i > 0: self[i],self[i-1]=self[i-1],self[i]
    def remove_layer(self, layer):
        if layer in self: self.remove(layer)
    def merge(self, a, b):
        target=a; target.shapes.extend(b.shapes); self.remove(b); return target

class Path:
    def __init__(self): self.commands=[]
    def move_to(self,x,y): self.commands.append(("move",x,y)); return self
    def line_to(self,x,y): self.commands.append(("line",x,y)); return self
    def quad_to(self,cx,cy,x,y): self.commands.append(("quad",cx,cy,x,y)); return self
    def curve_to(self,c1x,c1y,c2x,c2y,x,y): self.commands.append(("cubic",c1x,c1y,c2x,c2y,x,y)); return self
    def arc_to(self,*args): self.commands.append(("arc",*args)); return self
    def close(self): self.commands.append(("close",)); return self
    def clear(self): self.commands.clear(); return self

class Canvas:
    def __init__(self, **kwargs):
        self.position=kwargs.get("position",(0,0)); self.size=kwargs.get("size",("100%","100%"))
        self.opacity=kwargs.get("opacity",1); self.visible=kwargs.get("visible",True)
        self.layers=LayerStack(); self.current_layer=self.layers.create("Default")
        self.brushes=[]; self.current_brush=None; self.history=[]; self.redo_stack=[]
        self.background=kwargs.get("background",None); self.antialiasing=True
    def add_brush(self, color="#000000", **kwargs):
        b=Brush(color=color, **kwargs); self.brushes.append(b); self.current_brush=b; return b
    def set_brush(self, brush): self.current_brush=brush; return brush
    def create_layer(self,name="Layer"): return self.layers.create(name)
    def _shape(self,kind,**data):
        s=Shape(kind,data=data,fill=data.pop("fill",None),stroke=data.pop("stroke",None),stroke_width=data.pop("stroke_width",1)); self.current_layer.add(s); self.history.append(("add",self.current_layer,s)); self.redo_stack.clear(); return s
    def line(self,x1,y1,x2,y2,**style): return self._shape("line",x1=x1,y1=y1,x2=x2,y2=y2,**style)
    def polyline(self,points,**style): return self._shape("polyline",points=list(points),**style)
    def polygon(self,points,**style): return self._shape("polygon",points=list(points),**style)
    def rectangle(self,x,y,width,height,**style): return self._shape("rectangle",x=x,y=y,width=width,height=height,**style)
    def rounded_rectangle(self,x,y,width,height,radius=0,**style): return self._shape("rounded_rectangle",x=x,y=y,width=width,height=height,radius=radius,**style)
    def circle(self,x,y,radius,**style): return self._shape("circle",x=x,y=y,radius=radius,**style)
    def ellipse(self,x,y,width,height,**style): return self._shape("ellipse",x=x,y=y,width=width,height=height,**style)
    def arc(self,x,y,width,height,start,end,**style): return self._shape("arc",x=x,y=y,width=width,height=height,start=start,end=end,**style)
    def sector(self,x,y,width,height,start,end,**style): return self._shape("sector",x=x,y=y,width=width,height=height,start=start,end=end,**style)
    def star(self,x,y,outer_radius,points=5,inner_radius=None,**style): return self._shape("star",x=x,y=y,outer_radius=outer_radius,points=points,inner_radius=inner_radius,**style)
    def arrow(self,x1,y1,x2,y2,**style): return self._shape("arrow",x1=x1,y1=y1,x2=x2,y2=y2,**style)
    def path(self,path,**style): return self._shape("path",path=path,**style)
    def text(self,text,x,y,**style): return self._shape("text",text=text,x=x,y=y,**style)
    def image(self,source,x,y,width=None,height=None,**style): return self._shape("image",source=source,x=x,y=y,width=width,height=height,**style)
    def fill(self,color,point=None,**kwargs): return self._shape("fill",color=color,point=point,**kwargs)
    def stroke(self,points,**style): return self.polyline(points,**style)
    def erase(self,points,**style): return self._shape("erase",points=list(points),**style)
    def clear(self):
        self.current_layer.clear(); self.history.clear(); self.redo_stack.clear()
    def undo(self):
        if not self.history: return None
        action=self.history.pop(); _,layer,item=action
        if item in layer.shapes: layer.shapes.remove(item); self.redo_stack.append(action)
        return item
    def redo(self):
        if not self.redo_stack: return None
        action=self.redo_stack.pop(); _,layer,item=action; layer.shapes.append(item); self.history.append(action); return item
    def export(self,path,**kwargs):
        raise NotImplementedError("Rendering/export is provided by an AleraGUI backend")
    def to_image(self): raise NotImplementedError("Rendering is backend-provided")
    def to_svg(self): raise NotImplementedError("SVG serialization is backend-provided")
