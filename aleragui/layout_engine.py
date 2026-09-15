"""Deterministic 2D measure/layout helpers used by containers."""
from __future__ import annotations

def resolve(value, available, auto=None):
    if value is None or value == "auto": return available if auto is None else auto
    if isinstance(value,str) and value.endswith('%'):
        return available*float(value[:-1])/100
    if isinstance(value,(int,float)): return float(value)
    return available if auto is None else auto

def box(value):
    if isinstance(value,(int,float)): return (value,)*4
    if len(value)==2: return (value[0],value[1],value[0],value[1])
    if len(value)==4: return tuple(value)
    raise ValueError("box values need 1, 2 or 4 items")

def distribute(total, sizes, gaps=0):
    fixed=sum(x for x in sizes if isinstance(x,(int,float))); flex=sum(x for x in sizes if x in ("auto","fill"))
    remaining=max(0,total-gaps*max(0,len(sizes)-1)-fixed); each=remaining/flex if flex else 0
    return [each if x in ("auto","fill") else resolve(x,total) for x in sizes]

def flex_layout(items, width, height, direction="row", gap=0, justify="start", align="start"):
    main=width if direction=="row" else height; cross=height if direction=="row" else width
    sizes=distribute(main,[getattr(i,"size",("auto","auto"))[0 if direction=="row" else 1] for i in items],gap)
    used=sum(sizes)+gap*max(0,len(items)-1); extra=max(0,main-used)
    offset=0
    if justify=="center": offset=extra/2
    elif justify=="end": offset=extra
    elif justify=="space-between" and len(items)>1: gap+=extra/(len(items)-1)
    out=[]
    for item,size in zip(items,sizes):
        cross_size=resolve(getattr(item,"size",("auto","auto"))[1 if direction=="row" else 0],cross,cross)
        c=0 if align=="start" else (cross-cross_size if align=="end" else (cross-cross_size)/2)
        out.append((offset,c,size,cross_size) if direction=="row" else (c,offset,cross_size,size)); offset+=size+gap
    return out

def grid_layout(count, columns, width, height, gap=0):
    rows=(count+columns-1)//columns; cw=(width-gap*(columns-1))/columns if columns else 0; rh=(height-gap*(rows-1))/rows if rows else 0
    return [(i%columns*(cw+gap),i//columns*(rh+gap),cw,rh) for i in range(count)]
