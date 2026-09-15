"""Extended 2D rendering command system: gradients, paths, clipping, effects and batching."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Gradient:
    kind: str="linear"; start: tuple=(0,0); end: tuple=(1,0); stops: list=field(default_factory=list); radius: float=0

@dataclass
class Stroke:
    color: Any="#000000"; width: float=1; cap: str="butt"; join: str="miter"; dash: tuple=(); dash_offset: float=0; miter_limit: float=4

@dataclass
class Fill:
    color: Any=None; gradient: Gradient|None=None; opacity: float=1; blend_mode: str="normal"

@dataclass
class Clip:
    shape: Any; antialias: bool=True

@dataclass
class RenderState:
    opacity: float=1; transform: tuple=(1,0,0,1,0,0); clip_stack: list=field(default_factory=list)
    blend_mode: str="normal"

@dataclass
class Command2D:
    operation: str; args: tuple=(); kwargs: dict=field(default_factory=dict); state: RenderState|None=None

class RenderBatch:
    def __init__(self): self.commands=[]; self.state=RenderState()
    def add(self,operation,*args,**kwargs):
        self.commands.append(Command2D(operation,args,kwargs,self.state)); return self
    def save(self): self.add("save"); return self
    def restore(self): self.add("restore"); return self
    def translate(self,x,y): return self.add("translate",x,y)
    def rotate(self,angle): return self.add("rotate",angle)
    def scale(self,x,y=None): return self.add("scale",x,x if y is None else y)
    def transform(self,matrix): return self.add("transform",matrix)
    def clip(self,shape): return self.add("clip",shape)
    def clear_clip(self): return self.add("clear_clip")
    def line(self,*points,stroke=None): return self.add("line",*points,stroke=stroke)
    def polyline(self,points,stroke=None): return self.add("polyline",points,stroke=stroke)
    def polygon(self,points,fill=None,stroke=None): return self.add("polygon",points,fill=fill,stroke=stroke)
    def rect(self,rect,fill=None,stroke=None,radius=0): return self.add("rect",rect,fill=fill,stroke=stroke,radius=radius)
    def circle(self,center,radius,fill=None,stroke=None): return self.add("circle",center,radius,fill=fill,stroke=stroke)
    def ellipse(self,rect,fill=None,stroke=None): return self.add("ellipse",rect,fill=fill,stroke=stroke)
    def arc(self,center,radius,start,end,stroke=None): return self.add("arc",center,radius,start,end,stroke=stroke)
    def path(self,path,fill=None,stroke=None): return self.add("path",path,fill=fill,stroke=stroke)
    def text(self,text,position,font=None,fill=None): return self.add("text",text,position,font=font,fill=fill)
    def image(self,source,rect,**kwargs): return self.add("image",source,rect,**kwargs)
    def effect(self,name,**kwargs): return self.add("effect",name,**kwargs)
    def flush(self,renderer): return renderer.submit(self.commands)

class Renderer2D:
    """Backend contract. Native/GPU implementations consume RenderBatch commands."""
    name="abstract-2d"
    capabilities={"paths","text","images","gradients","clipping","effects","batching"}
    def submit(self,commands): raise NotImplementedError
    def begin_frame(self,width,height): return RenderBatch()
    def end_frame(self): pass
    def clear(self,color=None): pass

class RecordingRenderer(Renderer2D):
    name="recording"
    def __init__(self): self.frames=[]
    def submit(self,commands): self.frames.append(list(commands)); return len(commands)
    def clear(self,color=None): self.frames.clear()

class RenderCache:
    def __init__(self): self._items={}
    def get(self,key,default=None): return self._items.get(key,default)
    def set(self,key,value): self._items[key]=value; return value
    def invalidate(self,key=None): self._items.clear() if key is None else self._items.pop(key,None)
    def clear(self): self._items.clear()
