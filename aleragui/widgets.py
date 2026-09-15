"""Core reactive 2D widget objects. Rendering is delegated to a backend."""
from __future__ import annotations
from .events import EventDispatcher

class Reactive:
    def __init__(self): self._values={}; self._watchers={}
    def __setattr__(self,name,value):
        if name.startswith("_"): object.__setattr__(self,name,value); return
        old=self._values.get(name,object())
        self._values[name]=value; object.__setattr__(self,name,value)
        if old != value:
            for cb in tuple(self._watchers.get(name,())): cb(value,old)
    def watch(self,name,callback): self._watchers.setdefault(name,[]).append(callback); return callback

class Widget(Reactive, EventDispatcher):
    def __init__(self, **kwargs):
        EventDispatcher.__init__(self); Reactive.__init__(self)
        self.parent=None; self.children=[]
        self.position=kwargs.pop("position",(0,0)); self.size=kwargs.pop("size",("auto","auto"))
        self.visible=kwargs.pop("visible",True); self.enabled=kwargs.pop("enabled",True); self.opacity=kwargs.pop("opacity",1)
        self.rotation=kwargs.pop("rotation",0); self.scale=kwargs.pop("scale",(1,1)); self.z_index=kwargs.pop("z_index",0)
        self.background=kwargs.pop("background",None); self.border_width=kwargs.pop("border_width",0); self.border_color=kwargs.pop("border_color",None)
        self.border_radius=kwargs.pop("border_radius",0); self.padding=kwargs.pop("padding",0); self.margin=kwargs.pop("margin",0)
        self.clip=kwargs.pop("clip",False); self.shadow=kwargs.pop("shadow",None); self.tooltip=kwargs.pop("tooltip",None)
        self.focusable=kwargs.pop("focusable",False); self.accessible=kwargs.pop("accessible",True)
        self.accessibility_label=kwargs.pop("accessibility_label",None); self.tab_index=kwargs.pop("tab_index",0)
        for k,v in kwargs.items(): setattr(self,k,v)
    def add(self,*children):
        for child in children:
            if child.parent is not None: child.parent.remove(child)
            child.parent=self; self.children.append(child)
        return children[-1] if children else None
    def remove(self,child):
        if child in self.children: self.children.remove(child); child.parent=None
    def clear(self):
        for c in self.children: c.parent=None
        self.children.clear()
    def show(self): self.visible=True
    def hide(self): self.visible=False
    def focus(self): self.emit("focus"); return self
    def blur(self): self.emit("blur"); return self
    def animate(self, **kwargs):
        from .animation import Animation
        return Animation(**kwargs).play(self)
    def on(self,event,callback): return EventDispatcher.on(self,event,callback)
    def __repr__(self): return f"{type(self).__name__}(children={len(self.children)})"

class Container(Widget): pass

class Label(Widget):
    def __init__(self,text="",**kwargs):
        super().__init__(**kwargs); self.text=text; self.font_size=kwargs.get("font_size",14); self.font_family=kwargs.get("font_family","system")
        self.font_weight=kwargs.get("font_weight",400); self.font_style=kwargs.get("font_style","normal"); self.text_color=kwargs.get("text_color","#000000")
        self.alignment=kwargs.get("alignment","left"); self.vertical_alignment=kwargs.get("vertical_alignment","center"); self.line_spacing=1
        self.letter_spacing=0; self.word_spacing=0; self.wrap=True; self.max_lines=None; self.ellipsis=False; self.selectable=False; self.auto_size=False

class Button(Widget):
    def __init__(self,text=None,image=None,**kwargs):
        if (text is None) == (image is None): raise ValueError("Button requires exactly one of text or image")
        super().__init__(**kwargs); self.text=text; self.image=image; self.font_size=kwargs.get("font_size",14); self.text_color=kwargs.get("text_color","#000000")
        self.pressed=False; self.hovered=False; self.content_position=kwargs.get("content_position","center"); self.content_size=kwargs.get("content_size",None)
    def press(self): self.pressed=True; self.emit("press"); return self
    def release(self): self.pressed=False; self.emit("release"); self.emit("click"); return self
    def on_release(self,callback=None): return self.on("release",callback) if callback else lambda fn:self.on("release",fn)
    def on_click(self,callback=None): return self.on("click",callback) if callback else lambda fn:self.on("click",fn)

class TextInput(Widget):
    def __init__(self,text="",placeholder="",**kwargs):
        super().__init__(**kwargs); self.text=text; self.placeholder=placeholder; self.font_size=kwargs.get("font_size",14); self.font_family="system"; self.font_weight=400
        self.text_color="#000000"; self.placeholder_color="#888888"; self.background=kwargs.get("background",None); self.border_focus_color=kwargs.get("border_focus_color",None)
        self.multiline=kwargs.get("multiline",False); self.password=kwargs.get("password",False); self.read_only=kwargs.get("read_only",False); self.max_length=kwargs.get("max_length",None)
        self.alignment="left"; self.vertical_alignment="center"; self.cursor_position=0; self.selection_start=0; self.selection_end=0; self.cursor_color="#000000"; self.selection_color="#4488ff"
        self.auto_complete=False; self.spellcheck=False; self.keyboard_type="text"; self.return_key="default"; self.scrollable=True; self.undo_enabled=True; self.redo_enabled=True
    def set_text(self,value):
        if self.read_only: return
        if self.max_length is not None: value=value[:self.max_length]
        self.text=value; self.cursor_position=min(len(value),self.cursor_position); self.emit("change",value)
    def on_change(self,callback=None): return self.on("change",callback) if callback else lambda fn:self.on("change",fn)
    def on_submit(self,callback=None): return self.on("submit",callback) if callback else lambda fn:self.on("submit",fn)

class Image(Widget):
    def __init__(self,source=None,**kwargs):
        super().__init__(**kwargs); self.source=source; self.fit=kwargs.get("fit","contain"); self.alignment="center"; self.aspect_ratio=None; self.keep_aspect_ratio=True; self.crop=None
        self.crop_position="center"; self.flip_horizontal=False; self.flip_vertical=False; self.tint=None; self.brightness=1; self.contrast=1; self.saturation=1; self.gamma=1; self.blur=0; self.sharpen=0
        self.cache=True; self.preload=False; self.placeholder=None; self.error_image=None; self.interpolation="linear"; self.antialiasing=True
    def load(self,source=None):
        if source is not None: self.source=source
        self.emit("load",self); return self
    def on_load(self,callback=None): return self.on("load",callback) if callback else lambda fn:self.on("load",fn)
    def on_error(self,callback=None): return self.on("error",callback) if callback else lambda fn:self.on("error",fn)

class ScrollView(Container):
    def __init__(self,**kwargs):
        super().__init__(**kwargs); self.scroll_x=0; self.scroll_y=0; self.content_width=0; self.content_height=0; self.horizontal=True; self.vertical=True
        self.scrollbar_visible=True; self.scrollbar_width=8; self.overscroll=True; self.bounce=True; self.scroll_speed=1
    def scroll_to(self,x=None,y=None):
        if x is not None: self.scroll_x=x
        if y is not None: self.scroll_y=y
        self.emit("scroll",self.scroll_x,self.scroll_y)
