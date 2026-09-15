"""Backend-neutral 2D render tree and draw-command system."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Paint:
    fill: Any=None; stroke: Any=None; stroke_width: float=1; opacity: float=1; blend_mode: str="normal"
    line_cap: str="round"; line_join: str="round"

@dataclass
class DrawCommand:
    kind: str
    args: tuple=()
    paint: Paint|None=None
    transform: Any=None
    clip: Any=None
    metadata: dict=field(default_factory=dict)

class RenderList:
    def __init__(self): self.commands=[]
    def add(self,kind,*args,paint=None,transform=None,clip=None,**metadata):
        self.commands.append(DrawCommand(kind,args,paint,transform,clip,metadata)); return self.commands[-1]
    def clear(self): self.commands.clear()
    def extend(self,other): self.commands.extend(other.commands if isinstance(other,RenderList) else other)
    def __len__(self): return len(self.commands)

class Renderer:
    """Interface implemented by platform/GPU backends."""
    name="abstract"; hardware_accelerated=False
    def begin(self, surface, clear=True): pass
    def render(self, render_list):
        for command in render_list.commands: self.draw(command)
    def draw(self, command): raise NotImplementedError
    def end(self): pass
    def present(self): pass
    def measure_text(self,text,font): return (0,0)
    def load_image(self,source): raise NotImplementedError
    def dispose(self,resource): pass

class SoftwareRenderer(Renderer):
    name="software"
    def __init__(self): self.last_frame=RenderList()
    def draw(self,command): self.last_frame.add(command.kind,*command.args,paint=command.paint,transform=command.transform,clip=command.clip,**command.metadata)

class RenderNode:
    def __init__(self, widget=None): self.widget=widget; self.children=[]; self.dirty=True; self.bounds=None
    def add(self,*nodes): self.children.extend(nodes); self.invalidate(); return nodes[-1] if nodes else None
    def invalidate(self): self.dirty=True
    def build(self,renderer):
        output=RenderList()
        if self.widget and getattr(self.widget,"visible",True):
            build=getattr(self.widget,"render",None)
            if build: output.extend(build(renderer) or RenderList())
        for child in self.children: output.extend(child.build(renderer))
        self.dirty=False; return output

class RenderEngine:
    def __init__(self,renderer=None): self.renderer=renderer or SoftwareRenderer(); self.root=RenderNode(); self.frame=0
    def invalidate(self,node=None,**_):
        (node or self.root).invalidate()
    def frame_once(self,surface=None):
        self.frame+=1; self.renderer.begin(surface); commands=self.root.build(self.renderer); self.renderer.render(commands); self.renderer.end(); self.renderer.present(); return commands
