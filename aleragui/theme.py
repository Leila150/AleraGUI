"""Theme, palette and style resolution for AleraGUI."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Palette:
    primary="#4f46e5"; secondary="#64748b"; background="#ffffff"; surface="#f8fafc"; text="#0f172a"; muted="#64748b"; border="#cbd5e1"; error="#dc2626"; success="#16a34a"; warning="#d97706"

@dataclass
class Theme:
    name="default"; palette: Palette=field(default_factory=Palette); font_family="system"; font_size=14; spacing=8; radius=8; elevation=4; animation_scale=1.0; high_contrast=False; reduced_motion=False
    def style(self, **overrides):
        data={"font_family":self.font_family,"font_size":self.font_size,"spacing":self.spacing,"radius":self.radius}; data.update(overrides); return data

LIGHT=Theme("light")
DARK=Theme("dark",Palette(primary="#818cf8",secondary="#94a3b8",background="#0f172a",surface="#1e293b",text="#f8fafc",muted="#94a3b8",border="#475569",error="#f87171",success="#4ade80",warning="#fbbf24"))

class StyleSheet:
    def __init__(self): self.rules=[]
    def add(self, selector, **properties): self.rules.append((selector,properties)); return self
    def resolve(self, widget):
        result={}
        for selector,props in self.rules:
            if callable(selector) and selector(widget) or isinstance(selector,str) and (selector==type(widget).__name__ or selector==getattr(widget,"style_class",None)): result.update(props)
        return result
