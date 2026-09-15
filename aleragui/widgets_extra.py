"""Additional 2D widgets with a consistent property/event surface."""
from __future__ import annotations
from .widgets import Widget, Container

class Icon(Widget):
    def __init__(self,name=None,**kw): super().__init__(**kw); self.name=name; self.source=None; self.size=kw.get("size",24); self.color=kw.get("color","currentColor"); self.rotation=0; self.flip=False
class Link(Widget):
    def __init__(self,text="",url=None,**kw): super().__init__(**kw); self.text=text; self.url=url; self.underline=True; self.visited=False; self.hover_color="#2563eb"; self.enabled=True
class CheckBox(Widget):
    def __init__(self,checked=False,**kw): super().__init__(**kw); self.checked=checked; self.label=kw.get("label",""); self.indeterminate=False; self.check_color="#2563eb"; self.on_change_callback=None
    def toggle(self): self.checked=not self.checked; self.emit("change",self.checked); return self
class RadioButton(CheckBox):
    def __init__(self,group=None,**kw): super().__init__(**kw); self.group=group
class Switch(CheckBox):
    def __init__(self,value=False,**kw): super().__init__(checked=value,**kw); self.on_color="#2563eb"; self.off_color="#94a3b8"; self.thumb_size=20
class Slider(Widget):
    def __init__(self,value=0,min_value=0,max_value=1,**kw): super().__init__(**kw); self.value=value; self.min_value=min_value; self.max_value=max_value; self.step=kw.get("step",0); self.orientation=kw.get("orientation","horizontal"); self.track_size=6; self.thumb_size=20; self.on_change_callback=None
    def set_value(self,v): self.value=max(self.min_value,min(self.max_value,v)); self.emit("change",self.value); return self
class ProgressBar(Widget):
    def __init__(self,value=0,**kw): super().__init__(**kw); self.value=value; self.min_value=0; self.max_value=1; self.indeterminate=False; self.progress_color="#2563eb"; self.track_color="#e2e8f0"; self.border_radius=8
class Spinner(Widget):
    def __init__(self,**kw): super().__init__(**kw); self.active=True; self.value=0; self.speed=1; self.line_width=3; self.variant="ring"
class Stepper(Widget):
    def __init__(self,value=0,**kw): super().__init__(**kw); self.value=value; self.minimum=kw.get("minimum",0); self.maximum=kw.get("maximum",100); self.step=kw.get("step",1)
    def increment(self): self.value=min(self.maximum,self.value+self.step); self.emit("change",self.value); return self
    def decrement(self): self.value=max(self.minimum,self.value-self.step); self.emit("change",self.value); return self
class List(Container):
    def __init__(self,items=None,**kw): super().__init__(**kw); self.items=list(items or []); self.selected_index=None; self.selection_mode="single"; self.spacing=4; self.virtualized=True
    def select(self,index): self.selected_index=index; self.emit("change",index); return self
class Menu(Container):
    def __init__(self,items=None,**kw): super().__init__(**kw); self.items=list(items or []); self.open=False; self.trigger=None; self.keyboard_navigation=True; self.close_on_select=True
    def show(self): self.open=True; self.emit("show")
    def hide(self): self.open=False; self.emit("hide")
class NavigationBar(Container):
    def __init__(self,items=None,**kw): super().__init__(**kw); self.items=list(items or []); self.selected=0; self.position_mode="top"; self.background=None
class Sidebar(Container):
    def __init__(self,**kw): super().__init__(**kw); self.open=True; self.width=280; self.side="left"; self.overlay=False; self.collapsed=False
class Breadcrumb(Container):
    def __init__(self,items=None,**kw): super().__init__(**kw); self.items=list(items or []); self.separator="/"; self.current=None
class CodeEditor(Widget):
    def __init__(self,text="",**kw): super().__init__(**kw); self.text=text; self.language=kw.get("language","text"); self.theme=kw.get("theme","default"); self.line_numbers=True; self.word_wrap=False; self.minimap=False; self.read_only=False; self.tab_size=4; self.auto_indent=True; self.highlight_current_line=True
class RichText(Widget):
    def __init__(self,text="",**kw): super().__init__(**kw); self.text=text; self.markup=True; self.selectable=True; self.links=True; self.font_size=14; self.line_spacing=1.2
class Chart(Widget):
    def __init__(self,data=None,**kw): super().__init__(**kw); self.data=data or []; self.chart_type=kw.get("chart_type","line"); self.x_label=""; self.y_label=""; self.show_legend=True; self.grid=True; self.animate=True; self.line_width=2
