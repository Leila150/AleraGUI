"""Composable 2D containers and layout primitives."""
from __future__ import annotations
from .widgets import Container

class Layout(Container):
    spacing=0; padding=0
    def layout_children(self): return list(self.children)

class CustomLayout(Layout):
    """No automatic placement; children keep developer-controlled positions."""
    def layout_children(self): return list(self.children)

class AbsoluteLayout(CustomLayout): pass

class FlexLayout(Layout):
    def __init__(self,direction="row",wrap=False,spacing=0,**kwargs):
        super().__init__(**kwargs); self.direction=direction; self.wrap=wrap; self.spacing=spacing; self.justify_content="start"; self.align_items="stretch"; self.gap=spacing

class GridLayout(Layout):
    def __init__(self,columns=1,rows=None,**kwargs):
        super().__init__(**kwargs); self.columns=columns; self.rows=rows; self.column_gap=0; self.row_gap=0; self.auto_flow="row"; self.stretch=True

class StackLayout(Layout):
    def __init__(self,direction="vertical",**kwargs): super().__init__(**kwargs); self.direction=direction; self.spacing=0
class FlowLayout(Layout): pass
class WrapLayout(FlexLayout):
    def __init__(self,**kwargs): super().__init__(wrap=True,**kwargs)
class AnchorLayout(Layout):
    def __init__(self,anchor="center",**kwargs): super().__init__(**kwargs); self.anchor=anchor
class ConstraintLayout(Layout):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.constraints=[]
    def add_constraint(self,constraint): self.constraints.append(constraint); return constraint
class ResponsiveLayout(Layout):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.breakpoints={}; self.current_breakpoint=None
    def breakpoint(self,name,minimum_width,**values): self.breakpoints[name]=(minimum_width,values); return self
class DockLayout(Layout):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.dock="fill"

class Panel(Container): pass
class Card(Panel):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.elevation=0; self.interactive=False
class Frame(Panel): pass
class Surface(Panel): pass

class OverlayContainer(Container):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.modal=False; self.dismiss_on_outside=False; self.backdrop=None
    def open(self): self.visible=True; self.emit("show")
    def close(self): self.visible=False; self.emit("hide")
class LayerContainer(Container): pass
class SplitView(Container):
    def __init__(self,orientation="horizontal",**kwargs): super().__init__(**kwargs); self.orientation=orientation; self.divider_size=1; self.ratio=.5; self.resizable=True; self.min_ratio=.1; self.max_ratio=.9
class TabView(Container):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.tabs=[]; self.selected_index=0; self.tab_position="top"; self.scrollable=True; self.closable=False
    def add_tab(self,title,content): self.tabs.append((title,content)); self.add(content); return content
    def select(self,index): self.selected_index=index; self.emit("change",index)
class PageView(Container):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.pages=[]; self.index=0; self.orientation="horizontal"; self.swipe_enabled=True; self.loop=False
    def add_page(self,page): self.pages.append(page); self.add(page); return page
    def next(self):
        if self.pages: self.index=(self.index+1)%len(self.pages) if self.loop else min(self.index+1,len(self.pages)-1); self.emit("change",self.index)
    def previous(self):
        if self.pages: self.index=(self.index-1)%len(self.pages) if self.loop else max(self.index-1,0); self.emit("change",self.index)
class Drawer(OverlayContainer):
    def __init__(self,side="left",**kwargs): super().__init__(**kwargs); self.side=side; self.width=300; self.opened=False
    def open(self): self.opened=True; super().open()
    def close(self): self.opened=False; super().close()
