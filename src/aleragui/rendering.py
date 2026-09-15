from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol
from .types import Color, Rect, Point, Matrix3, Gradient

class BlendMode(str, Enum):
    NORMAL="normal"; MULTIPLY="multiply"; SCREEN="screen"; OVERLAY="overlay"; DARKEN="darken"; LIGHTEN="lighten"; ADD="add"; SUBTRACT="subtract"; DIFFERENCE="difference"; EXCLUSION="exclusion"; ERASE="erase"

class FillRule(str, Enum): NONZERO="nonzero"; EVEN_ODD="evenodd"
class LineCap(str, Enum): BUTT="butt"; ROUND="round"; SQUARE="square"
class LineJoin(str, Enum): MITER="miter"; ROUND="round"; BEVEL="bevel"

@dataclass
class Paint:
    fill: Color | Gradient | None = None
    stroke: Color | Gradient | None = None
    stroke_width: float = 1
    opacity: float = 1
    blend_mode: BlendMode = BlendMode.NORMAL
    fill_rule: FillRule = FillRule.NONZERO
    antialias: bool = True
    line_cap: LineCap = LineCap.BUTT
    line_join: LineJoin = LineJoin.MITER
    miter_limit: float = 4
    dash: tuple[float, ...] = ()
    dash_offset: float = 0

@dataclass
class DrawCommand:
    operation: str
    args: tuple[Any, ...] = ()
    paint: Paint = field(default_factory=Paint)
    transform: Matrix3 = field(default_factory=Matrix3)
    clip: Rect | None = None

class Renderer2D(Protocol):
    def begin_frame(self, width: int, height: int, scale: float = 1): ...
    def end_frame(self): ...
    def clear(self, color: Color): ...
    def save(self): ...
    def restore(self): ...
    def transform(self, matrix: Matrix3): ...
    def clip_rect(self, rect: Rect): ...
    def draw(self, command: DrawCommand): ...
    def flush(self): ...
    def measure_text(self, text: str, font: Any): ...
    def load_image(self, source: Any): ...
    def release_resource(self, resource: Any): ...
