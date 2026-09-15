"""Core reactive 2D widgets with stable IDs and backend-neutral runtime behavior."""
from __future__ import annotations
from .events import Event, EventDispatcher
from .runtime import InvalidationQueue

_INVALIDATIONS=InvalidationQueue()

class Reactive:
    def __init__(self):
        object.__setattr__(self,"_values",{}); object.__setattr__(self,"_watchers",{}); object.__setattr__(self,"_invalidated",True)
    def __setattr__(self,name,value):
        if name.startswith("_"):
            object.__setattr__(self,name,value); return
        values=getattr(self,"_values",{})
        old=values.get(name,_MISSING)
        if old is not _MISSING and old == value:
            object.__setattr__(self,name,value); return
        values[name]=value; object.__setattr__(self,name,value)
        for cb in tuple(getattr(self,"_watchers",{}).get(name,())): cb(value,None if old is _MISSING else old)
        invalidate=getattr(self,"invalidate",None)
        if invalidate: invalidate(property=name,old=None if old is _MISSING else old,new=value)
    def watch(self,name,callback): self._watchers.setdefault(name,[]).append(callback); return callback
    def unwatch(self,name,callback):
        try: self._watchers.get(name,[]).remove(callback)
        except ValueError: pass
    def bind(self,name,other,other_name=None):
        other_name=other_name or name
        def sync(value,_old): setattr(self,name,value)
        sync(getattr(other,other_name),None); other.watch(other_name,sync); return sync
    def notify(self,name): self.invalidate(property=name)

_MISSING=object()

class Widget(Reactive,EventDispatcher):
    def __init__(self,**kwargs):
        EventDispatcher.__init__(self); Reactive.__init__(self)
        self.id=kwargs.pop("id",None) or kwargs.pop("key",None) or ""
        self.key=kwargs.pop("key",self.id or None)
        self.parent=None; self.children=[]; self.layout_rect=None
        self.position=kwargs.pop("position",(0,0)); self.size=kwargs.pop("size",("auto","auto"))
        self.visible=kwargs.pop("visible",True); self.enabled=kwargs.pop("enabled",True); self.opacity=kwargs.pop("opacity",1)
        self.rotation=kwargs.pop("rotation",0); self.scale=kwargs.pop("scale",(1,1)); self.z_index=kwargs.pop("z_index",0)
        self.background=kwargs.pop("background",None); self.border_width=kwargs.pop("border_width",0); self.border_color=kwargs.pop("border_color",None)
        self.border_radius=kwargs.pop("border_radius",0); self.padding=kwargs.pop("padding",0); self.margin=kwargs.pop("margin",0)
        self.clip=kwargs.pop("clip",False); self.shadow=kwargs.pop("shadow",None); self.tooltip=kwargs.pop("tooltip",None)
        self.focusable=kwargs.pop("focusable",False); self.accessible=kwargs.pop("accessible",True)
        self.accessibility_label=kwargs.pop("accessibility_label",None); self.accessibility_hint=kwargs.pop("accessibility_hint",None)
        self.accessibility_role=kwargs.pop("accessibility_role",None); self.accessibility_value=kwargs.pop("accessibility_value",None)
        self.tab_index=kwargs.pop("tab_index",0); self.style_class=kwargs.pop("style_class",None); self.cursor=kwargs.pop("cursor","default")
        self.data=kwargs.pop("data",{})
        for k,v in kwargs.items(): setattr(self,k,v)
    def add(self,*children):
        for child in children:
            if child is self: raise ValueError("A widget cannot contain itself")
            if child.parent is not None: child.parent.remove(child)
            child.parent=self; self.children.append(child); child.emit("mount",child)
        self.invalidate(property="children"); return children[-1] if children else None
    def remove(self,child):
        if child in self.children:
            self.children.remove(child); child.parent=None; child.emit("unmount",child); self.invalidate(property="children")
        return child
    def clear(self):
        for c in tuple(self.children): self.remove(c)
        return self
    def find(self,widget_id):
        if self.id==widget_id: return self
        for child in self.children:
            found=child.find(widget_id)
            if found: return found
        return None
    def walk(self):
        yield self
        for child in self.children: yield from child.walk()
    def invalidate(self,**reason):
        self._invalidated=True; _INVALIDATIONS.add(self); self.emit("invalidate",self,reason)
        if self.parent is not None: self.parent.emit("child_invalidate",self,reason)
    def validate(self): self._invalidated=False; return self
    @property
    def invalidated(self): return self._invalidated
    @property
    def dirty(self): return self._invalidated
    def show(self): self.visible=True; self.emit("show",self); return self
    def hide(self): self.visible=False; self.emit("hide",self); return self
    def focus(self): self.emit("focus",self); return self
    def blur(self): self.emit("blur",self); return self
    def dispatch(self,event):
        from .runtime import EventRouter
        if isinstance(event,str): event=Event(event,source=self)
        return EventRouter().dispatch(self,event)
    def animate(self,**kwargs):
        from .animation import Animation
        return Animation(**kwargs).play(self)
    def on(self,event,callback=None): return EventDispatcher.on(self,event,callback)
    def __repr__(self): return f"{type(self).__name__}(id={self.id!r}, children={len(self.children)})"

class Container(Widget): pass

class Label(Widget):
    def __init__(self,text="",**kwargs):
        super().__init__(**kwargs); self.text=text; self.font_size=kwargs.get("font_size",14); self.font_family=kwargs.get("font_family","system")
        self.font_weight=kwargs.get("font_weight",400); self.font_style=kwargs.get("font_style","normal"); self.text_color=kwargs.get("text_color","#000000")
        self.alignment=kwargs.get("alignment","left"); self.vertical_alignment=kwargs.get("vertical_alignment","center"); self.line_spacing=kwargs.get("line_spacing",1)
        self.letter_spacing=kwargs.get("letter_spacing",0); self.word_spacing=kwargs.get("word_spacing",0); self.wrap=kwargs.get("wrap",True); self.max_lines=kwargs.get("max_lines",None); self.ellipsis=kwargs.get("ellipsis",False); self.selectable=kwargs.get("selectable",False); self.auto_size=kwargs.get("auto_size",False)

class Button(Widget):
    def __init__(self,text=None,image=None,**kwargs):
        if (text is None)==(image is None): raise ValueError("Button requires exactly one of text or image")
        super().__init__(**kwargs); self.text=text; self.image=image; self.font_size=kwargs.get("font_size",14); self.text_color=kwargs.get("text_color","#000000")
        self.pressed=False; self.hovered=False; self.content_position=kwargs.get("content_position","center"); self.content_size=kwargs.get("content_size",None)
    def press(self):
        if not self.enabled: return self
        self.pressed=True; self.emit("press",self); return self
    def release(self):
        if not self.enabled: return self
        was=self.pressed; self.pressed=False; self.emit("release",self)
        if was: self.emit("click",self)
        return self
    def click(self): return self.press().release()
    def on_release(self,callback=None): return self.on("release",callback)
    def on_click(self,callback=None): return self.on("click",callback)

class TextInput(Widget):
    def __init__(self,text="",placeholder="",**kwargs):
        super().__init__(**kwargs); self.text=text; self.placeholder=placeholder; self.font_size=kwargs.get("font_size",14); self.font_family=kwargs.get("font_family","system"); self.font_weight=kwargs.get("font_weight",400)
        self.text_color=kwargs.get("text_color","#000000"); self.placeholder_color=kwargs.get("placeholder_color","#888888"); self.background=kwargs.get("background",None); self.border_focus_color=kwargs.get("border_focus_color",None)
        self.multiline=kwargs.get("multiline",False); self.password=kwargs.get("password",False); self.read_only=kwargs.get("read_only",False); self.max_length=kwargs.get("max_length",None)
        self.alignment=kwargs.get("alignment","left"); self.vertical_alignment=kwargs.get("vertical_alignment","center"); self.cursor_position=len(text); self.selection_start=0; self.selection_end=0; self.cursor_color="#000000"; self.selection_color="#4488ff"
        self.auto_complete=kwargs.get("auto_complete",False); self.spellcheck=kwargs.get("spellcheck",False); self.keyboard_type=kwargs.get("keyboard_type","text"); self.return_key=kwargs.get("return_key","default"); self.scrollable=True; self.undo_enabled=True; self.redo_enabled=True
    def set_text(self,value):
        if self.read_only: return self
        value=str(value); value=value[:self.max_length] if self.max_length is not None else value
        self.text=value; self.cursor_position=min(len(value),self.cursor_position); self.emit("input",value); self.emit("change",value); return self
    def submit(self): self.emit("submit",self.text); return self
    def on_change(self,callback=None): return self.on("change",callback)
    def on_submit(self,callback=None): return self.on("submit",callback)
    def on_focus(self,callback=None): return self.on("focus",callback)
    def on_blur(self,callback=None): return self.on("blur",callback)

class Image(Widget):
    def __init__(self,source=None,**kwargs):
        super().__init__(**kwargs); self.source=source; self.fit=kwargs.get("fit","contain"); self.alignment=kwargs.get("alignment","center"); self.aspect_ratio=None; self.keep_aspect_ratio=True; self.crop=None; self.crop_position="center"; self.flip_horizontal=False; self.flip_vertical=False; self.tint=None; self.brightness=1; self.contrast=1; self.saturation=1; self.gamma=1; self.blur=0; self.sharpen=0; self.cache=True; self.preload=False; self.placeholder=None; self.error_image=None; self.interpolation="linear"; self.antialiasing=True; self.loading=False; self.progress=0
    def load(self,source=None):
        if source is not None: self.source=source
        self.loading=False; self.progress=1; self.emit("load",self); return self
    def fail(self,error): self.loading=False; self.emit("error",error); return self
    def on_load(self,callback=None): return self.on("load",callback)
    def on_error(self,callback=None): return self.on("error",callback)

class ScrollView(Container):
    def __init__(self,**kwargs):
        super().__init__(**kwargs); self.scroll_x=0; self.scroll_y=0; self.content_width=0; self.content_height=0; self.horizontal=True; self.vertical=True; self.scrollbar_visible=True; self.scrollbar_width=8; self.overscroll=True; self.bounce=True; self.scroll_speed=1
    def scroll_to(self,x=None,y=None):
        if x is not None: self.scroll_x=max(0,x)
        if y is not None: self.scroll_y=max(0,y)
        self.emit("scroll",self.scroll_x,self.scroll_y); return self

__all__=["Reactive","Widget","Container","Label","Button","TextInput","Image","ScrollView"]
