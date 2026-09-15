"""Production-oriented 2D geometry helpers: affine transforms, paths, curves and intersections."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos,sin,sqrt,atan2
from .geometry2d import Vec2, Rect2D

@dataclass(frozen=True)
class Affine2D:
    a:float=1; b:float=0; c:float=0; d:float=1; tx:float=0; ty:float=0
    def apply(self,p): return Vec2(self.a*p.x+self.c*p.y+self.tx,self.b*p.x+self.d*p.y+self.ty)
    def __matmul__(self,o):
        return Affine2D(self.a*o.a+self.c*o.b,self.b*o.a+self.d*o.b,self.a*o.c+self.c*o.d,self.b*o.c+self.d*o.d,self.a*o.tx+self.c*o.ty+self.tx,self.b*o.tx+self.d*o.ty+self.ty)
    def inverse(self):
        det=self.a*self.d-self.b*self.c
        if abs(det)<1e-12: raise ValueError('Singular transform')
        return Affine2D(self.d/det,-self.b/det,-self.c/det,self.a/det,(self.c*self.ty-self.d*self.tx)/det,(self.b*self.tx-self.a*self.ty)/det)
    @staticmethod
    def translation(x,y): return Affine2D(tx=x,ty=y)
    @staticmethod
    def scale(x,y=None): return Affine2D(a=x,d=x if y is None else y)
    @staticmethod
    def rotation(angle): return Affine2D(c=-sin(angle),b=sin(angle),a=cos(angle),d=cos(angle))

@dataclass(frozen=True)
class Segment2D:
    start:Vec2; end:Vec2
    @property
    def length(self): return self.start.distance(self.end)
    def point(self,t): return self.start+(self.end-self.start)*t

@dataclass(frozen=True)
class Circle2D:
    center:Vec2; radius:float
    def contains(self,p): return self.center.distance(p)<=self.radius
    def bounds(self): return Rect2D(self.center.x-self.radius,self.center.y-self.radius,self.radius*2,self.radius*2)

@dataclass(frozen=True)
class Ellipse2D:
    center:Vec2; radius_x:float; radius_y:float
    def contains(self,p):
        x=(p.x-self.center.x)/self.radius_x; y=(p.y-self.center.y)/self.radius_y
        return x*x+y*y<=1

class Path2D:
    def __init__(self): self.commands=[]
    def move_to(self,x,y): self.commands.append(('M',Vec2(x,y))); return self
    def line_to(self,x,y): self.commands.append(('L',Vec2(x,y))); return self
    def quad_to(self,cx,cy,x,y): self.commands.append(('Q',Vec2(cx,cy),Vec2(x,y))); return self
    def cubic_to(self,c1x,c1y,c2x,c2y,x,y): self.commands.append(('C',Vec2(c1x,c1y),Vec2(c2x,c2y),Vec2(x,y))); return self
    def close(self): self.commands.append(('Z',)); return self
    def clear(self): self.commands.clear(); return self
    def transformed(self,matrix):
        out=Path2D()
        for cmd in self.commands:
            out.commands.append((cmd[0],)+tuple(matrix.apply(p) for p in cmd[1:]))
        return out

def segment_intersection(a,b,c,d):
    r=b-a; s=d-c; den=r.cross(s)
    if abs(den)<1e-12: return None
    t=(c-a).cross(s)/den; u=(c-a).cross(r)/den
    return a+r*t if 0<=t<=1 and 0<=u<=1 else None

def distance_to_circle(p,circle): return abs(p.distance(circle.center)-circle.radius)

def project_point_to_line(p,a,b):
    v=b-a; n=v.dot(v)
    if not n:return a
    return a+v*((p-a).dot(v)/n)

def polygon_perimeter(points): return sum(a.distance(b) for a,b in zip(points,points[1:]+points[:1]))

def convex_hull(points):
    pts=sorted(set((p.x,p.y) for p in points))
    if len(pts)<=1:return [Vec2(*p) for p in pts]
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    hi=[]
    for p in reversed(pts):
        while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    return [Vec2(*p) for p in lo[:-1]+hi[:-1]]
