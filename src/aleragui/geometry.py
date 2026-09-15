from __future__ import annotations
from math import atan2, cos, sin, sqrt
from .types import Point, Rect

def lerp(a, b, t): return a + (b - a) * t

def lerp_point(a: Point, b: Point, t: float): return Point(lerp(a.x,b.x,t), lerp(a.y,b.y,t))

def rotate_point(point: Point, center: Point, degrees: float):
    from math import radians
    r=radians(degrees); x=point.x-center.x; y=point.y-center.y
    return Point(center.x+x*cos(r)-y*sin(r), center.y+x*sin(r)+y*cos(r))

def angle_between(a: Point, b: Point): return atan2(b.y-a.y, b.x-a.x)

def distance(a: Point, b: Point): return a.distance_to(b)

def clamp(value, minimum, maximum): return max(minimum, min(maximum, value))

def point_in_polygon(point: Point, points):
    inside=False; j=len(points)-1
    for i in range(len(points)):
        xi,yi=points[i]; xj,yj=points[j]
        if ((yi>point.y)!=(yj>point.y)) and point.x < (xj-xi)*(point.y-yi)/(yj-yi)+xi: inside=not inside
        j=i
    return inside

def polygon_bounds(points):
    xs=[p.x for p in points]; ys=[p.y for p in points]
    return Rect(min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys)) if points else Rect()

def snap(value, step): return round(value/step)*step if step else value
