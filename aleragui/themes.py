"""Advanced theme system with semantic tokens, states, density and platform variants."""
from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class ThemeTokens:
    colors: dict = field(default_factory=dict)
    typography: dict = field(default_factory=dict)
    spacing: dict = field(default_factory=dict)
    radii: dict = field(default_factory=dict)
    shadows: dict = field(default_factory=dict)
    motion: dict = field(default_factory=dict)
    dimensions: dict = field(default_factory=dict)
    icons: dict = field(default_factory=dict)

class AdvancedTheme:
    def __init__(self,name="custom",mode="light",tokens=None):
        self.name=name; self.mode=mode; self.tokens=tokens or ThemeTokens(); self.platforms={}; self.components={}; self.states={}
    def clone(self,name=None):
        other=AdvancedTheme(name or self.name,self.mode,deepcopy(self.tokens)); other.platforms=deepcopy(self.platforms); other.components=deepcopy(self.components); other.states=deepcopy(self.states); return other
    def set(self,path,value):
        target=self.tokens
        parts=path.split(".")
        for part in parts[:-1]:
            target=getattr(target,part) if hasattr(target,part) else target.setdefault(part,{})
        if hasattr(target,parts[-1]): setattr(target,parts[-1],value)
        else: target[parts[-1]]=value
        return self
    def component(self,name,**style): self.components[name]=style; return self
    def state(self,name,**style): self.states[name]=style; return self
    def platform(self,name,**style): self.platforms[name]=style; return self
    def resolve(self,component=None,state=None,platform=None):
        out={}
        out.update(self.components.get(component,{})); out.update(self.states.get(state,{})); out.update(self.platforms.get(platform,{})); return out

def make_theme(name,mode,accent):
    t=AdvancedTheme(name,mode)
    t.tokens.colors.update({"accent":accent,"background":"#ffffff" if mode=="light" else "#111111","surface":"#f7f7f7" if mode=="light" else "#1b1b1b","text":"#111111" if mode=="light" else "#f5f5f5","muted":"#666666" if mode=="light" else "#aaaaaa","border":"#dddddd" if mode=="light" else "#333333","danger":"#d93025","success":"#188038","warning":"#f9ab00"})
    t.tokens.spacing.update({"xs":4,"sm":8,"md":12,"lg":16,"xl":24,"xxl":32})
    t.tokens.radii.update({"none":0,"sm":4,"md":8,"lg":14,"xl":22,"pill":999})
    t.tokens.motion.update({"fast":.12,"normal":.2,"slow":.35,"reduced":0})
    t.tokens.typography.update({"body":14,"small":12,"large":18,"title":24,"display":36})
    return t

LIGHT_MODERN=make_theme("Modern Light","light","#3867ff")
DARK_MODERN=make_theme("Modern Dark","dark","#7c8cff")
HIGH_CONTRAST=make_theme("High Contrast","dark","#ffff00").set("colors.background","#000000").set("colors.text","#ffffff").set("colors.border","#ffffff")
