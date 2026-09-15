"""Useful runtime primitives that connect AleraGUI's declarative objects into a real UI tree.

This module is backend-neutral: platform backends consume the invalidation/render work it
produces, while applications can already use IDs, queries, hit testing and event routing.
"""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable, Iterable


class DuplicateIDError(ValueError):
    pass


class IDRegistry:
    """Fast ID registry with deterministic generated IDs and collision detection."""
    def __init__(self):
        self._items: dict[str, Any] = {}
        self._counter = 0

    def generate(self, prefix: str = "widget") -> str:
        while True:
            self._counter += 1
            value = f"{prefix}-{self._counter}"
            if value not in self._items:
                return value

    def register(self, widget: Any, widget_id: str | None = None) -> str:
        value = widget_id or self.generate(type(widget).__name__.lower())
        if value in self._items and self._items[value] is not widget:
            raise DuplicateIDError(f"AleraGUI ID already exists: {value!r}")
        self._items[value] = widget
        return value

    def unregister(self, widget_or_id: Any) -> None:
        key = widget_or_id if isinstance(widget_or_id, str) else getattr(widget_or_id, "id", None)
        if key in self._items and (isinstance(widget_or_id, str) or self._items[key] is widget_or_id):
            del self._items[key]

    def get(self, widget_id: str, default=None):
        return self._items.get(widget_id, default)

    def __contains__(self, widget_id: str) -> bool:
        return widget_id in self._items

    def all(self) -> tuple[Any, ...]:
        return tuple(self._items.values())


@dataclass(frozen=True)
class HitResult:
    widget: Any
    local_position: tuple[float, float]
    path: tuple[Any, ...]


def _rect(widget: Any):
    x, y = getattr(widget, "position", (0, 0))
    w, h = getattr(widget, "size", (0, 0))
    if isinstance(w, str) or isinstance(h, str):
        return None
    return float(x), float(y), float(w), float(h)


def hit_test(root: Any, point: tuple[float, float]) -> HitResult | None:
    """Return the topmost visible widget containing a point.

    Percentage/auto sizes are intentionally left to the layout engine; once a layout pass
    resolves them into numeric ``layout_rect`` values, hit testing uses those values.
    """
    px, py = point

    def visit(node: Any, ox: float, oy: float, ancestors: tuple[Any, ...]):
        if not getattr(node, "visible", True) or getattr(node, "opacity", 1) <= 0:
            return None
        rect = getattr(node, "layout_rect", None)
        if rect is None:
            rect = _rect(node)
        if rect is None:
            return None
        x, y, w, h = rect
        ax, ay = ox + x, oy + y
        if not (ax <= px <= ax + w and ay <= py <= ay + h):
            return None
        path = ancestors + (node,)
        children = sorted(getattr(node, "children", ()), key=lambda c: getattr(c, "z_index", 0))
        for child in reversed(children):
            result = visit(child, ax, ay, path)
            if result is not None:
                return result
        return HitResult(node, (px - ax, py - ay), path)

    return visit(root, 0.0, 0.0, ())


class EventRouter:
    """DOM-like capture/target/bubble routing for widget trees."""
    def dispatch(self, target: Any, event: Any) -> Any:
        path = getattr(event, "path", None)
        if path is None:
            path = self._path(target)
        event.target = target
        event.path = tuple(path)
        # Capture: root -> parent of target.
        for node in event.path[:-1]:
            if getattr(event, "stopped", False): return event
            node.emit(f"{event.type}:capture", event)
        if not getattr(event, "stopped", False):
            target.emit(event.type, event)
        # Bubble: target parent -> root.
        if getattr(event, "bubbles", True):
            for node in reversed(event.path[:-1]):
                if getattr(event, "stopped", False): break
                node.emit(event.type, event)
        return event

    @staticmethod
    def _path(target: Any) -> list[Any]:
        path=[]
        node=target
        while node is not None:
            path.append(node)
            node=getattr(node, "parent", None)
        return list(reversed(path))


class WidgetTree:
    """Owns IDs and provides useful tree operations for an application/window."""
    def __init__(self, root: Any | None = None):
        self.ids = IDRegistry()
        self.root = None
        if root is not None: self.set_root(root)

    def set_root(self, root: Any):
        self.root = root
        self._register_recursive(root)
        return root

    def _register_recursive(self, node):
        self.ids.register(node, getattr(node, "id", None))
        for child in getattr(node, "children", ()): self._register_recursive(child)

    def register(self, widget: Any):
        self.ids.register(widget, getattr(widget, "id", None)); return widget

    def unregister(self, widget: Any):
        for child in tuple(getattr(widget, "children", ())): self.unregister(child)
        self.ids.unregister(widget)

    def get(self, widget_id: str): return self.ids.get(widget_id)

    def find(self, predicate: Callable[[Any], bool] | None = None, **attrs):
        result=[]
        for node in self.walk():
            if predicate is not None and not predicate(node): continue
            if all(getattr(node, key, object()) == value for key, value in attrs.items()): result.append(node)
        return result

    def first(self, predicate=None, **attrs):
        items=self.find(predicate, **attrs)
        return items[0] if items else None

    def walk(self, node=None):
        node = self.root if node is None else node
        if node is None: return
        yield node
        for child in getattr(node, "children", ()): yield from self.walk(child)


class FrameScheduler:
    """Small deterministic scheduler for invalidation and per-frame callbacks."""
    def __init__(self, fps: float = 60.0):
        self.fps=max(1.0, float(fps)); self.frame=0; self.running=False; self.last_time=monotonic(); self._callbacks=[]

    def add(self, callback: Callable[[float], Any]):
        if callback not in self._callbacks: self._callbacks.append(callback)
        return callback

    def remove(self, callback):
        if callback in self._callbacks: self._callbacks.remove(callback)

    def tick(self, now: float | None = None) -> float:
        current=monotonic() if now is None else now
        dt=max(0.0, current-self.last_time); self.last_time=current; self.frame+=1
        for callback in tuple(self._callbacks): callback(dt)
        return dt

    def step(self, frames: int = 1):
        for _ in range(max(0, frames)): self.tick()
        return self.frame


class InvalidationQueue:
    """Coalesces widget invalidations so a frame only processes each widget once."""
    def __init__(self): self._queue=[]; self._set=set()
    def add(self, widget):
        key=id(widget)
        if key not in self._set: self._set.add(key); self._queue.append(widget)
    def drain(self):
        items=tuple(self._queue); self._queue.clear(); self._set.clear(); return items
    def __len__(self): return len(self._queue)


__all__=["DuplicateIDError","IDRegistry","HitResult","hit_test","EventRouter","WidgetTree","FrameScheduler","InvalidationQueue"]
