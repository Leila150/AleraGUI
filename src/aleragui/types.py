from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, sin
from typing import Any, Iterable


class Unit(float):
    kind = "px"
    def __new__(cls, value=0): return float.__new__(cls, value)
    def __repr__(self): return f"{self.kind}({float(self):g})"

class Px(Unit): kind = "px"
class Percent(Unit): kind = "%"
class Dp(Unit): kind = "dp"
class Sp(Unit): kind = "sp"
class Em(Unit): kind = "em"
class Rem(Unit): kind = "rem"

@dataclass(frozen=True)
class Auto: pass

@dataclass(frozen=True)
class Fill:
    weight: float = 1.0

@dataclass(frozen=True)
class Min:
    value: Any

@dataclass(frozen=True)
class Max:
    value: Any

@dataclass(frozen=True)
class Clamp:
    minimum: Any
    preferred: Any
    maximum: Any

@dataclass(frozen=True)
class Point:
    x: float = 0
    y: float = 0
    def __iter__(self): return iter((self.x, self.y))
    def __add__(self, o): return Point(self.x + o.x, self.y + o.y)
    def __sub__(self, o): return Point(self.x - o.x, self.y - o.y)
    def __mul__(self, n): return Point(self.x * n, self.y * n)
    def distance_to(self, o): return ((self.x-o.x)**2 + (self.y-o.y)**2) ** .5

Vector2 = Point

@dataclass(frozen=True)
class Size:
    width: Any = 0
    height: Any = 0
    def __iter__(self): return iter((self.width, self.height))

@dataclass(frozen=True)
class Rect:
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0
    @property
    def left(self): return self.x
    @property
    def right(self): return self.x + self.width
    @property
    def top(self): return self.y
    @property
    def bottom(self): return self.y + self.height
    @property
    def center(self): return Point(self.x + self.width/2, self.y + self.height/2)
    def contains(self, p: Point): return self.left <= p.x <= self.right and self.top <= p.y <= self.bottom
    def intersects(self, r: "Rect"): return not (self.right < r.left or self.left > r.right or self.bottom < r.top or self.top > r.bottom)

@dataclass(frozen=True)
class Margin:
    top: Any = 0; right: Any = 0; bottom: Any = 0; left: Any = 0
    def __init__(self, value=0, right=None, bottom=None, left=None):
        if right is None: right = bottom = left = value
        elif bottom is None: bottom = value
        elif left is None: left = right
        object.__setattr__(self, "top", value); object.__setattr__(self, "right", right)
        object.__setattr__(self, "bottom", bottom); object.__setattr__(self, "left", left)

Padding = Margin

@dataclass(frozen=True)
class Radius:
    top_left: Any = 0; top_right: Any = 0; bottom_right: Any = 0; bottom_left: Any = 0
    def __init__(self, value=0, top_right=None, bottom_right=None, bottom_left=None):
        if top_right is None: top_right = bottom_right = bottom_left = value
        elif bottom_right is None: bottom_right = value
        elif bottom_left is None: bottom_left = top_right
        object.__setattr__(self, "top_left", value); object.__setattr__(self, "top_right", top_right)
        object.__setattr__(self, "bottom_right", bottom_right); object.__setattr__(self, "bottom_left", bottom_left)

@dataclass(frozen=True)
class Color:
    r: int; g: int; b: int; a: int = 255
    def __init__(self, value=0, g=None, b=None, a=255):
        if isinstance(value, str):
            s = value.strip().lstrip("#")
            if len(s) in (3, 4): s = "".join(c*2 for c in s)
            if len(s) == 6: s += "ff"
            if len(s) != 8: raise ValueError("Color must be #RGB, #RGBA, #RRGGBB or #RRGGBBAA")
            vals = tuple(int(s[i:i+2], 16) for i in range(0, 8, 2))
            object.__setattr__(self, "r", vals[0]); object.__setattr__(self, "g", vals[1]); object.__setattr__(self, "b", vals[2]); object.__setattr__(self, "a", vals[3]); return
        object.__setattr__(self, "r", int(value)); object.__setattr__(self, "g", int(g or 0)); object.__setattr__(self, "b", int(b or 0)); object.__setattr__(self, "a", int(a))
    def __str__(self): return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"
    def with_alpha(self, alpha): return Color(self.r, self.g, self.b, alpha)

@dataclass(frozen=True)
class Shadow:
    color: Color = field(default_factory=lambda: Color("#00000066"))
    offset: Point = field(default_factory=Point)
    blur: float = 0
    spread: float = 0

@dataclass(frozen=True)
class Transform:
    position: Point = field(default_factory=Point)
    rotation: float = 0
    scale: Vector2 = field(default_factory=lambda: Vector2(1, 1))
    skew: Vector2 = field(default_factory=Vector2)
    origin: Vector2 = field(default_factory=lambda: Vector2(.5, .5))

@dataclass(frozen=True)
class Matrix3:
    values: tuple[float, ...] = (1,0,0, 0,1,0, 0,0,1)
    def transform(self, p: Point):
        a,b,c,d,e,f,g,h,i = self.values
        w = g*p.x + h*p.y + i
        return Point((a*p.x+b*p.y+c)/w, (d*p.x+e*p.y+f)/w)

@dataclass(frozen=True)
class Anchor:
    x: float = 0
    y: float = 0

@dataclass(frozen=True)
class Stop:
    offset: float
    color: Color

@dataclass(frozen=True)
class Gradient:
    stops: tuple[Stop, ...]
    kind: str = "linear"
    angle: float = 0
    center: Point = field(default_factory=lambda: Point(.5, .5))
    @classmethod
    def linear(cls, *stops, angle=0): return cls(tuple(stops), "linear", angle)
    @classmethod
    def radial(cls, *stops, center=Point(.5,.5)): return cls(tuple(stops), "radial", 0, center)

@dataclass(frozen=True)
class Font:
    family: str = "system"
    size: float = 16
    weight: int | str = 400
    style: str = "normal"
    stretch: str = "normal"
    line_height: Any = "normal"

@dataclass(frozen=True)
class LineStyle:
    width: float = 1
    cap: str = "butt"
    join: str = "miter"
    dash: tuple[float, ...] = ()
    dash_offset: float = 0

StrokeStyle = LineStyle
