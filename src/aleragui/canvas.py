from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .types import Color, Point, Rect, Size, LineStyle, Gradient
from .events import EventEmitter

@dataclass
class Brush:
    color: Color = field(default_factory=Color)
    size: float = 1
    opacity: float = 1
    hardness: float = 1
    spacing: float = .1
    smoothing: float = 0
    angle: float = 0
    rotation: float = 0
    pressure: bool = True
    texture: Any = None
    blend_mode: str = "normal"
    eraser: bool = False

@dataclass
class Shape:
    kind: str
    data: dict[str, Any] = field(default_factory=dict)
    fill: Any = None
    stroke: Any = None
    stroke_width: float = 1
    opacity: float = 1
    rotation: float = 0
    scale: Point = field(default_factory=lambda: Point(1, 1))
    visible: bool = True
    name: str | None = None

@dataclass
class Text:
    value: str
    position: Point = field(default_factory=Point)
    font: Any = None
    fill: Any = None
    rotation: float = 0
    opacity: float = 1

@dataclass
class ImageDrawable:
    source: Any
    rect: Rect | None = None
    opacity: float = 1
    rotation: float = 0
    scale: Point = field(default_factory=lambda: Point(1, 1))

class Path:
    def __init__(self): self.commands: list[tuple] = []
    def move_to(self, x, y): self.commands.append(("M", x, y)); return self
    def line_to(self, x, y): self.commands.append(("L", x, y)); return self
    def horizontal_to(self, x): self.commands.append(("H", x)); return self
    def vertical_to(self, y): self.commands.append(("V", y)); return self
    def quad_to(self, cx, cy, x, y): self.commands.append(("Q", cx, cy, x, y)); return self
    def curve_to(self, *values): self.commands.append(("C", *values)); return self
    def arc_to(self, *values): self.commands.append(("A", *values)); return self
    def close(self): self.commands.append(("Z",)); return self
    def clear(self): self.commands.clear(); return self

class Layer(EventEmitter):
    def __init__(self, name="Layer"):
        super().__init__(); self.name=name; self.items=[]; self.visible=True; self.opacity=1; self.z_index=0; self.blend_mode="normal"; self.clip=None; self.mask=None
    def add(self, item): self.items.append(item); self.emit("change", self); return item
    def remove(self, item): self.items.remove(item); self.emit("change", self)
    def clear(self): self.items.clear(); self.emit("change", self)
    def raise_(self): self.z_index += 1; self.emit("change", self)
    def lower(self): self.z_index -= 1; self.emit("change", self)
    def move_to(self, index): self.z_index=index; self.emit("change", self)
    def show(self): self.visible=True; self.emit("change", self)
    def hide(self): self.visible=False; self.emit("change", self)

class Canvas(EventEmitter):
    """Backend-neutral 2D drawing board. Rendering is intentionally delegated to a platform renderer."""
    def __init__(self, *, width=0, height=0):
        super().__init__(); self.width=width; self.height=height; self.position=Point(); self.size=Size(width,height); self.opacity=1; self.visible=True
        self.background=Color("#00000000"); self.antialiasing=True; self.device_pixel_ratio=1; self.brushes=[]; self.current_brush=None; self.layers=[]; self.active_layer=None
        self._history=[]; self._redo=[]; self._batch=None
        self.create_layer("Background")
        self.create_layer("Content")

    def create_layer(self, name="Layer", *, index=None):
        layer=Layer(name)
        if index is None: self.layers.append(layer)
        else: self.layers.insert(index, layer)
        self.active_layer=layer
        return layer
    def remove_layer(self, layer): self.layers.remove(layer); self.active_layer=self.layers[-1] if self.layers else None
    def move_layer(self, layer, index): self.layers.remove(layer); self.layers.insert(index, layer)
    def merge_layers(self, first, second):
        first.items.extend(second.items); self.remove_layer(second); return first
    def add_brush(self, color="#000000", **kwargs):
        brush=Brush(Color(color), **kwargs); self.brushes.append(brush); self.current_brush=brush; return brush
    def set_brush(self, brush): self.current_brush=brush; return brush
    def brush(self, **kwargs): return self.add_brush(**kwargs)
    def _add(self, kind, **data):
        item=Shape(kind, data=data); (self.active_layer or self.create_layer()).add(item); self.emit("draw", item); return item
    def line(self, start, end, *, stroke=None, width=1, **kwargs): return self._add("line", start=Point(*start), end=Point(*end), stroke=stroke or (self.current_brush.color if self.current_brush else Color()), width=width, **kwargs)
    def polyline(self, points, **kwargs): return self._add("polyline", points=[Point(*p) for p in points], **kwargs)
    def polygon(self, points, **kwargs): return self._add("polygon", points=[Point(*p) for p in points], **kwargs)
    def rectangle(self, rect, **kwargs): return self._add("rectangle", rect=rect, **kwargs)
    def rounded_rectangle(self, rect, radius=0, **kwargs): return self._add("rounded_rectangle", rect=rect, radius=radius, **kwargs)
    def circle(self, center, radius, **kwargs): return self._add("circle", center=Point(*center), radius=radius, **kwargs)
    def ellipse(self, rect, **kwargs): return self._add("ellipse", rect=rect, **kwargs)
    def arc(self, rect, start, sweep, **kwargs): return self._add("arc", rect=rect, start=start, sweep=sweep, **kwargs)
    def sector(self, center, radius, start, sweep, **kwargs): return self._add("sector", center=Point(*center), radius=radius, start=start, sweep=sweep, **kwargs)
    def star(self, center, radius, points=5, inner_radius=None, **kwargs): return self._add("star", center=Point(*center), radius=radius, points=points, inner_radius=inner_radius, **kwargs)
    def arrow(self, start, end, head_size=10, **kwargs): return self._add("arrow", start=Point(*start), end=Point(*end), head_size=head_size, **kwargs)
    def path(self, path: Path, **kwargs): return self._add("path", path=path, **kwargs)
    def text(self, value, position, **kwargs):
        item=Text(value, Point(*position), **kwargs); (self.active_layer or self.create_layer()).add(item); self.emit("draw", item); return item
    def image(self, source, rect, **kwargs):
        item=ImageDrawable(source, rect, **kwargs); (self.active_layer or self.create_layer()).add(item); self.emit("draw", item); return item
    def fill(self, color, *, point=None, tolerance=0): return self._add("fill", color=Color(color), point=point, tolerance=tolerance)
    def eraser(self, size=None):
        b=self.current_brush or self.add_brush(); b.eraser=True
        if size is not None: b.size=size
        return b
    def clear(self, layer=None): (layer or self.active_layer).clear()
    def clear_all(self):
        for layer in self.layers: layer.clear()
    def begin_action(self): self._batch=[]; return self
    def end_action(self):
        if self._batch is not None: self._history.append(self._batch); self._redo.clear(); self._batch=None
    def undo(self): return self._history.pop() if self._history else None
    def redo(self): return self._redo.pop() if self._redo else None
    def export(self, path, *, format=None, scale=1): raise NotImplementedError("A platform renderer must provide Canvas export")
    def to_image(self, *, scale=1): raise NotImplementedError("A platform renderer must provide Canvas rasterization")
    def to_svg(self): raise NotImplementedError("SVG serialization will be provided by the vector renderer")
