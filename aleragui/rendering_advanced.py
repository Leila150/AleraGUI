"""Backend-neutral advanced 2D rendering graph, effects, clipping and batching."""
from __future__ import annotations
from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import Any
from .geometry_advanced import Affine2D

@dataclass
class Shader:
    name:str='default'; source:str=''; uniforms:dict[str,Any]=field(default_factory=dict)
    def set(self,name,value): self.uniforms[name]=value; return self

@dataclass
class Effect:
    name:str; parameters:dict[str,Any]=field(default_factory=dict); enabled:bool=True

@dataclass
class RenderTarget:
    width:int; height:int; samples:int=1; transparent:bool=True

@dataclass
class RenderPass:
    name:str='main'; target:RenderTarget|None=None; commands:list[Any]=field(default_factory=list)
    effects:list[Effect]=field(default_factory=list)
    def add(self,command): self.commands.append(command); return command

class Batch:
    def __init__(self): self.items=[]
    def add(self,texture,geometry,transform=None,material=None): self.items.append((texture,geometry,transform,material)); return self
    def clear(self): self.items.clear(); return self
    def __len__(self): return len(self.items)

class RenderGraph:
    def __init__(self): self.passes=[]
    def add_pass(self,name='main',target=None):
        p=RenderPass(name,target); self.passes.append(p); return p
    def clear(self): self.passes.clear()

class RendererFeatures:
    def __init__(self,**features): self.features=features
    def supports(self,name): return bool(self.features.get(name,False))

class RenderContext:
    def __init__(self,renderer=None):
        self.renderer=renderer; self.transform=Affine2D(); self.opacity=1.0; self.clip_stack=[]; self.effects=[]
    @contextmanager
    def save(self):
        state=(self.transform,self.opacity,list(self.clip_stack),list(self.effects))
        try: yield self
        finally:self.transform,self.opacity,self.clip_stack,self.effects=state
    def translate(self,x,y): self.transform=self.transform @ Affine2D.translation(x,y); return self
    def scale(self,x,y=None): self.transform=self.transform @ Affine2D.scale(x,y); return self
    def rotate(self,a): self.transform=self.transform @ Affine2D.rotation(a); return self
    def push_clip(self,shape): self.clip_stack.append(shape); return self
    def pop_clip(self):
        if self.clip_stack:self.clip_stack.pop()
        return self
    def add_effect(self,effect): self.effects.append(effect); return self

class FrameScheduler:
    def __init__(self): self.frame=0; self.invalidated=True
    def invalidate(self): self.invalidated=True
    def begin(self): self.frame+=1; self.invalidated=False; return self.frame
    def needs_frame(self): return self.invalidated
