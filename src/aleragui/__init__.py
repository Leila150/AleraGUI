"""AleraGUI - universal GUI foundation.

The 0.1 development API starts with the 2D engine. 3D is intentionally not
part of this release.
"""

from .types import (
    Color, Point, Size, Rect, Margin, Padding, Radius, Shadow, Transform,
    Px, Percent, Dp, Sp, Em, Rem, Auto, Fill, Clamp, Min, Max, Anchor,
    Vector2, Matrix3, Gradient, Stop, Font, LineStyle, StrokeStyle,
)
from .events import Event, EventEmitter, EventContext, event, on, bind, watch
from .canvas import Canvas, Layer, Path, Brush, Shape, Text, ImageDrawable
from .rendering import BlendMode, FillRule, LineCap, LineJoin, Paint, DrawCommand, Renderer2D
from .geometry import lerp, lerp_point, rotate_point, angle_between, distance, clamp, point_in_polygon, polygon_bounds, snap
from .decorators import (
    canvas_event, draw, on_pointer_down, on_pointer_move, on_pointer_up,
    on_pointer_enter, on_pointer_leave, on_click, on_double_click,
    on_long_press, on_drag, on_drop, on_scroll, on_resize, on_move,
    on_mount, on_unmount, animatable, observable, computed, command,
)

__all__ = [
    "Color", "Point", "Size", "Rect", "Margin", "Padding", "Radius",
    "Shadow", "Transform", "Px", "Percent", "Dp", "Sp", "Em", "Rem",
    "Auto", "Fill", "Clamp", "Min", "Max", "Anchor", "Vector2", "Matrix3",
    "Gradient", "Stop", "Font", "LineStyle", "StrokeStyle", "Event",
    "EventEmitter", "EventContext", "event", "on", "bind", "watch",
    "Canvas", "Layer", "Path", "Brush", "Shape", "Text", "ImageDrawable",
    "BlendMode", "FillRule", "LineCap", "LineJoin", "Paint", "DrawCommand", "Renderer2D",
    "lerp", "lerp_point", "rotate_point", "angle_between", "distance", "clamp",
    "point_in_polygon", "polygon_bounds", "snap", "canvas_event", "draw",
    "on_pointer_down", "on_pointer_move", "on_pointer_up", "on_pointer_enter",
    "on_pointer_leave", "on_click", "on_double_click", "on_long_press", "on_drag",
    "on_drop", "on_scroll", "on_resize", "on_move", "on_mount", "on_unmount",
    "animatable", "observable", "computed", "command",
]
