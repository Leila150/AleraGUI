"""2D geometry, hit-testing, polygon and Bezier utilities."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot, sqrt, sin, cos, pi

@dataclass(frozen=True)
class Vec2:
    x: float=0; y: float=0
    def __add__(self,o): return Vec2(self.x+o.x,self.y+o.y)
    def __sub__(self,o): return Vec2(self.x-o.x,self.y-o.y)
    def __mul__(self,n): return Vec2(self.x*n,self.y*n)
    __rmul__=__mul__
    def __truediv__(self,n): return Vec2(self.x/n,self.y/n)
    def length(self): return hypot(self.x,self.y)
    def normalized(self):
        n=self.length(); return self if n==0 else self/n
    def dot(self,o): return self.x*o.x+self.y*o.y
    def cross(self,o): return self.x*o.y-self.y*o.x
    def distance_to(self,o): return (self-o).length()

@dataclass(frozen=True)
class Bounds:
    x: float; y: float; width: float; height: float
    @property
    def left(self): return self.x
    @property
    def top(self): return self.y
    @property
    def right(self): return self.x+self.width
    @property
    def bottom(self): return self.y+self.height
    @property
    def center(self): return Vec2(self.x+self.width/2,self.y+self.height/2)
    def contains(self,p): return self.left<=p.x<=self.right and self.top<=p.y<=self.bottom
    def intersects(self,o): return not (self.right<o.left or o.right<self.left or self.bottom<o.top or o.bottom<self.top)
    def union(self,o):
        x=min(self.left,o.left); y=min(self.top,o.top); r=max(self.right,o.right); b=max(self.bottom,o.bottom)
        return Bounds(x,y,r-x,b-y)

Rect2D=Bounds

def polygon_area(points): return abs(sum(a.x*b.y-b.x*a.y for a,b in zip(points,points[1:]+points[:1])))/2

def point_in_polygon(point, points):
    inside=False
    for i,a in enumerate(points):
        b=points[(i+1)%len(points)]
        if (a.y>point.y)!=(b.y>point.y) and point.x < (b.x-a.x)*(point.y-a.y)/(b.y-a.y)+a.x: inside=not inside
    return inside

def distance_to_segment(p,a,b):
    d=b-a; denom=d.dot(d)
    t=0 if denom==0 else max(0,min(1,(p-a).dot(d)/denom))
    return p.distance_to(a+d*t)

def bezier_quadratic(p0,p1,p2,t):
    u=1-t; return p0*u*u+p1*(2*u*t)+p2*t*t

def bezier_cubic(p0,p1,p2,p3,t):
    u=1-t; return p0*u**3+p1*(3*u*u*t)+p2*(3*u*t*t)+p3*t**3

def rotate(point, angle, origin=Vec2()):
    a=angle*pi/180; p=point-origin; return Vec2(p.x*cos(a)-p.y*sin(a),p.x*sin(a)+p.y*cos(a))+origin

def bounding_box(points):
    if not points: return Bounds(0,0,0,0)
    xs=[p.x for p in points]; ys=[p.y for p in points]; return Bounds(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
