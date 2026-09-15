"""2D floating layers, overlays, dialogs, menus and notifications."""
from .containers import OverlayContainer

class Overlay(OverlayContainer):
    def __init__(self,content=None,**kwargs): super().__init__(**kwargs); self.content=content; self.modal=kwargs.get("modal",False); self.backdrop=kwargs.get("backdrop",None); self.dismiss_on_escape=True; self.dismiss_on_outside=False; self.focus_trap=False
    def open(self):
        if self.content and self.content not in self.children: self.add(self.content)
        super().open(); return self

class Popup(Overlay): pass
class Popover(Overlay):
    def __init__(self,anchor=None,**kwargs): super().__init__(**kwargs); self.anchor=anchor; self.placement="bottom"; self.offset=(0,0); self.flip=True
class Tooltip(Popover):
    def __init__(self,text="",**kwargs): super().__init__(**kwargs); self.text=text; self.delay=.5; self.duration=0; self.follow_cursor=False
class Modal(Overlay):
    def __init__(self,**kwargs): super().__init__(modal=True,**kwargs)
class Dialog(Modal):
    def __init__(self,title="",**kwargs): super().__init__(**kwargs); self.title=title; self.resizable=False; self.close_button=True; self.buttons=[]
class ContextMenu(Popup):
    def __init__(self,items=None,**kwargs): super().__init__(**kwargs); self.items=list(items or []); self.keyboard_navigation=True
class Dropdown(Popup):
    def __init__(self,items=None,**kwargs): super().__init__(**kwargs); self.items=list(items or []); self.selected=None; self.searchable=False
class Toast(Overlay):
    def __init__(self,message="",**kwargs): super().__init__(**kwargs); self.message=message; self.duration=3; self.position="bottom-right"
class Snackbar(Toast): pass
class Notification(Toast):
    def __init__(self,title="",message="",**kwargs): super().__init__(message,**kwargs); self.title=title; self.icon=None; self.actions=[]
class Sheet(Modal):
    def __init__(self,side="bottom",**kwargs): super().__init__(**kwargs); self.side=side; self.detents=[.25,.5,1]; self.current_detent=1
class BottomSheet(Sheet):
    def __init__(self,**kwargs): super().__init__(side="bottom",**kwargs)
class ActionSheet(BottomSheet): pass
class CommandPalette(Modal):
    def __init__(self,commands=None,**kwargs): super().__init__(**kwargs); self.commands=list(commands or []); self.query=""; self.selected_index=0
class Spotlight(Overlay): pass
class Tour(Overlay):
    def __init__(self,steps=None,**kwargs): super().__init__(**kwargs); self.steps=list(steps or []); self.index=0
