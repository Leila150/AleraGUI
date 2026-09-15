"""High-level 2D views: data, documents, web, lists and media surfaces."""
from __future__ import annotations
from .widgets import Widget, Container

class View(Widget): pass

class WebView(View):
    def __init__(self,url=None,**kwargs):
        super().__init__(**kwargs); self.url=url; self.html=None; self.javascript_enabled=True; self.cookies_enabled=True; self.cache_enabled=True
        self.zoom=1; self.user_agent=None; self.transparent=False; self.devtools=False; self.downloads=True; self.navigation_enabled=True
        self.context_menu=True; self.scroll_enabled=True; self.local_storage=True; self.session_storage=True
    def load(self,url): self.url=url; self.emit("load",url); return self
    def reload(self): return self.load(self.url)
    def stop(self): self.emit("cancel",self)
    def go_back(self): self.emit("navigation","back")
    def go_forward(self): self.emit("navigation","forward")
    def execute_javascript(self,script): raise NotImplementedError("Web execution is backend-provided")
    def clear_cache(self): pass
    def clear_cookies(self): pass
    def find(self,text): self.emit("find",text)

class TreeNode:
    def __init__(self,value,**kwargs): self.value=value; self.children=[]; self.parent=None; self.expanded=kwargs.get("expanded",False); self.selected=False; self.checked=kwargs.get("checked",False); self.editable=kwargs.get("editable",True); self.icon=kwargs.get("icon",None)
    def add_child(self,value,**kwargs):
        n=TreeNode(value,**kwargs); n.parent=self; self.children.append(n); return n

class TreeView(View):
    def __init__(self,**kwargs):
        super().__init__(**kwargs); self.nodes=[]; self.selection=[]; self.multiple_selection=False; self.checkable=False; self.editable=True; self.drag_enabled=False; self.drop_enabled=False
        self.icons=True; self.indent=20; self.row_height=28; self.show_lines=True; self.show_root=True; self.expand_on_click=True; self.virtualized=True; self.sorting=False; self.filter=None; self.search=""
    def add_node(self,value,**kwargs): n=TreeNode(value,**kwargs); self.nodes.append(n); return n
    def expand(self,node): node.expanded=True; self.emit("change",node)
    def collapse(self,node): node.expanded=False; self.emit("change",node)
    def expand_all(self):
        def rec(n): n.expanded=True; [rec(c) for c in n.children]
        [rec(n) for n in self.nodes]
    def collapse_all(self):
        def rec(n): n.expanded=False; [rec(c) for c in n.children]
        [rec(n) for n in self.nodes]
    def select(self,node):
        if not self.multiple_selection: self.selection.clear()
        if node not in self.selection: self.selection.append(node)
        node.selected=True; self.emit("change",node)
    def remove(self,node):
        if node.parent and node in node.parent.children: node.parent.children.remove(node)
        elif node in self.nodes: self.nodes.remove(node)

class CollectionView(View):
    def __init__(self,items=None,**kwargs):
        super().__init__(**kwargs); self.items=list(items or []); self.layout="list"; self.columns=1; self.gap=0; self.virtualized=True; self.lazy_loading=True
        self.item_template=None; self.selected_index=None; self.multiple_selection=False; self.loading=False; self.empty_view=None; self.error_view=None
        self.filter=None; self.sort_key=None; self.group_key=None; self.page_size=None; self.page=0; self.overscan=3
    def add(self,item): self.items.append(item); self.emit("change",self.items); return item
    def remove(self,item):
        if item in self.items: self.items.remove(item); self.emit("change",self.items)
    def insert(self,index,item): self.items.insert(index,item); self.emit("change",self.items)
    def clear(self): self.items.clear(); self.emit("change",self.items)
    def get(self,index): return self.items[index]
    def select(self,index): self.selected_index=index; self.emit("select",index,self.items[index])
    def scroll_to(self,index): self.emit("scroll_to",index)
    def apply_filter(self,fn): self.filter=fn; return [x for x in self.items if fn(x)]
    def sort(self,key=None,reverse=False): self.items.sort(key=key,reverse=reverse); self.emit("change",self.items); return self

class ListView(CollectionView):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.layout="list"
class GridView(CollectionView):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.layout="grid"

class TableView(CollectionView):
    def __init__(self,columns=None,**kwargs):
        super().__init__(**kwargs); self.columns=columns or []; self.row_height=32; self.header_visible=True; self.footer_visible=False; self.resizable_columns=True; self.reorderable_columns=True
        self.sortable=True; self.filterable=True; self.editable=False; self.frozen_columns=0; self.frozen_rows=1; self.selection_mode="single"; self.grid_lines=True; self.pagination=False

class DataGrid(TableView):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.virtualized=True; self.column_menu=True; self.groupable=True; self.aggregation=True; self.row_numbers=True

class StackView(Container):
    def __init__(self,**kwargs): super().__init__(**kwargs); self.index=-1; self.transition="none"; self.history=[]
    def push(self,page): self.history.append(self.index); self.add(page); self.index=len(self.children)-1; return page
    def pop(self):
        if self.children: return self.children.pop() 
    def replace(self,page): self.clear(); return self.push(page)

class MarkdownView(View):
    def __init__(self,text="",**kwargs): super().__init__(**kwargs); self.text=text; self.allow_html=False; self.selectable=True; self.links_enabled=True
class RichTextView(View): pass
class CodeView(View):
    def __init__(self,code="",language="text",**kwargs): super().__init__(**kwargs); self.code=code; self.language=language; self.line_numbers=True; self.word_wrap=False; self.editable=True; self.syntax_highlighting=True
class ImageView(View):
    def __init__(self,source=None,**kwargs): super().__init__(**kwargs); self.source=source; self.zoom=1; self.min_zoom=.1; self.max_zoom=10; self.pan_enabled=True; self.rotation=0
class PDFView(View): pass
class MapView(View): pass
class CameraView(View): pass
class AudioPlayer(View): pass
class VideoView(View):
    def __init__(self,source=None,**kwargs): super().__init__(**kwargs); self.source=source; self.autoplay=False; self.loop=False; self.muted=False; self.volume=1; self.playback_rate=1; self.current_time=0; self.duration=0; self.controls=True; self.fullscreen=False; self.poster=None; self.subtitles=True
    def play(self): self.emit("play")
    def pause(self): self.emit("pause")
    def stop(self): self.current_time=0; self.emit("stop")
    def seek(self,time): self.current_time=time; self.emit("progress",time,self.duration)
