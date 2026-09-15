"""Theme engine with semantic tokens, state variants and cascading style rules."""
from __future__ import annotations
from dataclasses import dataclass,field
from copy import deepcopy

@dataclass
class ThemeTokens:
    colors:dict[str,str]=field(default_factory=dict); spacing:dict[str,float]=field(default_factory=dict); radii:dict[str,float]=field(default_factory=dict); typography:dict[str,dict]=field(default_factory=dict); shadows:dict[str,dict]=field(default_factory=dict); motion:dict[str,float]=field(default_factory=dict)
    def get(self,group,key,default=None): return getattr(self,group,{}).get(key,default)
    def set(self,group,key,value): getattr(self,group)[key]=value; return self
    def clone(self): return deepcopy(self)

@dataclass
class StyleRule:
    selector:str; properties:dict[str,object]; specificity:int=0

class Cascade:
    def __init__(self): self.rules=[]
    def add(self,selector,**properties):
        specificity=selector.count('#')*100+selector.count('.')*10+1
        rule=StyleRule(selector,properties,specificity); self.rules.append(rule); self.rules.sort(key=lambda r:r.specificity); return rule
    def resolve(self,widget):
        out={}
        for rule in self.rules:
            if matches(rule.selector,widget): out.update(rule.properties)
        return out

def matches(selector,widget):
    if selector=='*': return True
    name=widget.__class__.__name__; classes=set(getattr(widget,'style_class','').split())
    if selector.startswith('.') : return selector[1:] in classes
    if selector.startswith('#'): return selector[1:]==str(getattr(widget,'id',''))
    return selector==name

@dataclass
class Theme:
    name:str; tokens:ThemeTokens=field(default_factory=ThemeTokens); cascade:Cascade=field(default_factory=Cascade); parent:'Theme|None'=None
    def style(self,widget):
        values=self.parent.style(widget) if self.parent else {}
        values.update(self.cascade.resolve(widget)); return values
    def derive(self,name): return Theme(name,self.tokens.clone(),Cascade(),self)

DEFAULT_TOKENS=ThemeTokens(
 colors={'background':'#ffffff','surface':'#f7f7f8','text':'#111111','muted':'#6b7280','primary':'#2563eb','danger':'#dc2626','success':'#16a34a','warning':'#d97706','border':'#d1d5db','focus':'#3b82f6'},
 spacing={'xs':4,'sm':8,'md':12,'lg':16,'xl':24,'xxl':32},
 radii={'none':0,'sm':4,'md':8,'lg':12,'xl':18,'pill':999},
 typography={'body':{'size':14,'weight':400},'title':{'size':28,'weight':700},'caption':{'size':12,'weight':400}},
 shadows={'sm':{'blur':4,'offset':(0,1)},'md':{'blur':10,'offset':(0,4)},'lg':{'blur':24,'offset':(0,10)}},
 motion={'fast':0.12,'normal':0.2,'slow':0.35})
LIGHT_PRO=Theme('light-pro',DEFAULT_TOKENS)
DARK_PRO=Theme('dark-pro',DEFAULT_TOKENS.clone()); DARK_PRO.tokens.colors.update({'background':'#0b0f14','surface':'#151a21','text':'#f5f7fa','muted':'#9aa4b2','border':'#2c3440'})
