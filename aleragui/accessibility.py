"""Accessibility tree and platform-neutral semantics."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class AccessibilityNode:
    role: str="generic"; label: str|None=None; hint: str|None=None; value: str|None=None; enabled: bool=True; focused: bool=False; hidden: bool=False; actions: list[str]=field(default_factory=list)

class AccessibilityManager:
    def __init__(self): self.nodes={}; self.focused=None
    def register(self,widget,node=None):
        node=node or AccessibilityNode(); self.nodes[id(widget)]=node; return node
    def unregister(self,widget): self.nodes.pop(id(widget),None)
    def focus(self,widget):
        if self.focused and id(self.focused) in self.nodes: self.nodes[id(self.focused)].focused=False
        self.focused=widget; self.register(widget).focused=True
    def announce(self,message): return str(message)
    def tree(self): return tuple(self.nodes.values())
