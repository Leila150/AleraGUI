"""Strong, backend-neutral 2D value types and units."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, sin, radians
from typing import Any, Iterable


def _num(v: Any) -> float:
    return float(v.value if hasattr(v, "value") else v)

@dataclass(frozen=True)
class Point:
    x: float = 0
    y: float = 0
    def __iter__(self): return iter((self.x, self.y))
    def __add__(self, o): return Point(self.x + _num(o[0]), self.y + _num(o[1]))
    def __sub__(self, o): return Point(self.x - _num(o[0]), self.y - _num(o[1]))
    def distance_to(self, o): return ((self.x-o[0])**2 + (self.y-o[1])**2) ** .5

Vector2 = Point

@dataclass(frozen=True)
class Size:
    width: float = 0
    height: float = 0
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
    def top(self): return self.y
    @property
    def right(self): return self.x + self.width
    @property
    def bottom(self): return self.y + self.height
    @property
    def center(self): return Point(self.x + self.width/2, self.y + self.height/2)
    def contains(self, p): return self.left <= p[0] <= self.right and self.top <= p[1] <= self.bottom

@dataclass(frozen=True)
class Color:
    value: str = "#000000"
    alpha: float = 1.0
    def __str__(self): return self.value
    @classmethod
    def rgba(cls, r, g, b, a=1): return cls(f"#{int(r):02x}{int(g):02x}{int(b):02x}", a)
    @classmethod
    def rgb(cls, r, g, b): return cls.rgba(r, g, b)

@dataclass(frozen=True)
class GradientStop:
    offset: float
    color: Color | str

@dataclass(frozen=True)
class Gradient:
    stops: tuple[GradientStop, ...]
    kind: str = "linear"
    angle: float = 0
    def __init__(self, stops: Iterable[GradientStop], kind="linear", angle=0):
        object.__setattr__(self, "stops", tuple(stops)); object.__setattr__(self, "kind", kind); object.__setattr__(self, "angle", angle)

@dataclass(frozen=True)
class Font:
    family: str = "system"
    size: float = 14
    weight: int | str = 400
    style: str = "normal"

@dataclass(frozen=True)
class Shadow:
    color: Color | str = "#00000080"
    offset: Point = Point(0, 2)
    blur: float = 8
    spread: float = 0

@dataclass(frozen=True)
class Transform:
    position: Point = Point()
    rotation: float = 0
    scale: Point = Point(1, 1)
    skew: Point = Point()
    origin: Point = Point(.5, .5)

@dataclass(frozen=True)
class Matrix3:
    values: tuple[float, ...] = (1,0,0, 0,1,0, 0,0,1)
    def transform_point(self, p):
        a,b,c,d,e,f,g,h,i = self.values
        x,y = p
        w = g*x+h*y+i or 1
        return Point((a*x+b*y+c)/w, (d*x+e*y+f)/w)

@dataclass(frozen=True)
class Margin:
    top: float=0; right: float=0; bottom: float=0; left: float=0
    @classmethod
    def all(cls, value): return cls(value,value,value,value)

Padding = Margin

@dataclass(frozen=True)
class Radius:
    top_left: float=0; top_right: float=0; bottom_right: float=0; bottom_left: float=0
    @classmethod
    def all(cls, value): return cls(value,value,value,value)

@dataclass(frozen=True)
class Unit:
    value: float
    unit: str
    def resolve(self, parent=0, density=1, font_size=16, viewport=0):
        if self.unit == "px": return self.value
        if self.unit == "%": return parent * self.value / 100
        if self.unit == "dp": return self.value * density
        if self.unit == "sp": return self.value * density
        if self.unit == "em": return self.value * font_size
        if self.unit == "rem": return self.value * 16
        return self.value
    def __float__(self): return self.value

class Px(Unit):
    def __init__(self, value): super().__init__(value, "px")
class Percent(Unit):
    def __init__(self, value): super().__init__(value, "%")
class Dp(Unit):
    def __init__(self, value): super().__init__(value, "dp")
class Sp(Unit):
    def __init__(self, value): super().__init__(value, "sp")
class Em(Unit):
    def __init__(self, value): super().__init__(value, "em")
class Rem(Unit):
    def __init__(self, value): super().__init__(value, "rem")

class AutoType:
    def __repr__(self): return "Auto()"
class FillType:
    def __repr__(self): return "Fill()"
Auto = AutoType
Fill = FillType

@dataclass(frozen=True)
class Constraint:
    value: Any
@dataclass(frozen=True)
class Min(Constraint): pass
@dataclass(frozen=True)
class Max(Constraint): pass
@dataclass(frozen=True)
class Clamp:
    minimum: Any
    preferred: Any
    maximum: Any


def rotate_point(point, angle, origin=Point()):
    a=radians(angle); x=point[0]-origin.x; y=point[1]-origin.y
    return Point(origin.x+x*cos(a)-y*sin(a), origin.y+x*sin(a)+y*cos(a))

def lerp(a, b, t): return a + (b-a)*t

def clamp(value, minimum=0, maximum=1): return max(minimum, min(maximum, value))
