"""Extended backend-neutral 2D computational geometry."""
from __future__ import annotations
from dataclasses import dataclass
from math import atan2, cos, hypot, pi, sin, sqrt
from typing import Iterable

@dataclass(frozen=True)
class Vec2:
    x: float = 0.0; y: float = 0.0
    def __add__(self,o): return Vec2(self.x+o.x,self.y+o.y)
    def __sub__(self,o): return Vec2(self.x-o.x,self.y-o.y)
    def __mul__(self,k): return Vec2(self.x*k,self.y*k)
    __rmul__=__mul__
    def __truediv__(self,k): return Vec2(self.x/k,self.y/k)
    def dot(self,o): return self.x*o.x+self.y*o.y
    def cross(self,o): return self.x*o.y-self.y*o.x
    def length(self): return hypot(self.x,self.y)
    def normalized(self):
        n=self.length(); return self/n if n else Vec2()
    def distance(self,o): return (self-o).length()
    def angle(self): return atan2(self.y,self.x)
    def rotate(self,a,origin=None):
        origin=origin or Vec2(); p=self-origin; c,s=cos(a),sin(a)
        return Vec2(origin.x+p.x*c-p.y*s,origin.y+p.x*s+p.y*c)

@dataclass(frozen=True)
class Size2D:
    width: float=0; height: float=0

@dataclass(frozen=True)
class Rect2D:
    x: float=0; y: float=0; width: float=0; height: float=0
    @property
    def left(self): return self.x
    @property
    def right(self): return self.x+self.width
    @property
    def top(self): return self.y
    @property
    def bottom(self): return self.y+self.height
    @property
    def center(self): return Vec2(self.x+self.width/2,self.y+self.height/2)
    def contains(self,p): return self.left<=p.x<=self.right and self.top<=p.y<=self.bottom
    def intersects(self,r): return not (self.right<r.left or r.right<self.left or self.bottom<r.top or r.bottom<self.top)
    def inset(self,n): return Rect2D(self.x+n,self.y+n,max(0,self.width-2*n),max(0,self.height-2*n))
    def outset(self,n): return Rect2D(self.x-n,self.y-n,self.width+2*n,self.height+2*n)

def distance(a,b): return a.distance(b)
def midpoint(a,b): return (a+b)*0.5
def dot(a,b): return a.dot(b)
def cross(a,b): return a.cross(b)
def angle_between(a,b): return atan2(a.cross(b),a.dot(b))
def polygon_area(points): return abs(sum(a.x*b.y-b.x*a.y for a,b in zip(points,points[1:]+points[:1])))/2
def polygon_centroid(points):
    area2=sum(a.x*b.y-b.x*a.y for a,b in zip(points,points[1:]+points[:1]))
    if not area2: return Vec2()
    cx=sum((a.x+b.x)*(a.x*b.y-b.x*a.y) for a,b in zip(points,points[1:]+points[:1]))/ (3*area2)
    cy=sum((a.y+b.y)*(a.x*b.y-b.x*a.y) for a,b in zip(points,points[1:]+points[:1]))/ (3*area2)
    return Vec2(cx,cy)
def bounding_rect(points):
    xs=[p.x for p in points]; ys=[p.y for p in points]
    return Rect2D(min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)) if xs else Rect2D()
def point_in_polygon(p,points):
    inside=False
    for a,b in zip(points,points[1:]+points[:1]):
        if (a.y>p.y)!=(b.y>p.y) and p.x < (b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x: inside=not inside
    return inside
def line_intersection(a,b,c,d):
    r=b-a; s=d-c; den=r.cross(s)
    if abs(den)<1e-12: return None
    t=(c-a).cross(s)/den
    return a+r*t
def distance_to_segment(p,a,b):
    ab=b-a; denom=ab.dot(ab)
    if not denom: return p.distance(a)
    t=max(0,min(1,(p-a).dot(ab)/denom)); return p.distance(a+ab*t)
def lerp(a,b,t): return a+(b-a)*t
def bezier_quadratic(p0,p1,p2,t): return p0*(1-t)**2+p1*(2*(1-t)*t)+p2*t*t
def bezier_cubic(p0,p1,p2,p3,t): return p0*(1-t)**3+p1*(3*(1-t)**2*t)+p2*(3*(1-t)*t*t)+p3*t**3
def circle_point(center,radius,angle): return center+Vec2(cos(angle),sin(angle))*radius
def regular_polygon(center,radius,sides,rotation=-pi/2): return [circle_point(center,radius,rotation+2*pi*i/sides) for i in range(sides)]
def star_polygon(center,outer,inner,points,rotation=-pi/2):
    return [circle_point(center,outer if i%2==0 else inner,rotation+pi*i/points) for i in range(points*2)]
def rounded_rect_points(rect,radius,segments=8):
    radius=max(0,min(radius,min(rect.width,rect.height)/2)); out=[]
    corners=((rect.right-radius,rect.top+radius,-pi/2,0),(rect.right-radius,rect.bottom-radius,0,pi/2),(rect.left+radius,rect.bottom-radius,pi/2,pi),(rect.left+radius,rect.top+radius,pi,3*pi/2))
    for cx,cy,a,b in corners:
        for i in range(segments+1):
            t=i/segments; ang=a+(b-a)*t; out.append(Vec2(cx+radius*cos(ang),cy+radius*sin(ang)))
    return out
