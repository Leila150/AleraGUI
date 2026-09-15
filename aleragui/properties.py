"""Reactive property and binding primitives for AleraGUI."""
from __future__ import annotations
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Any, Callable

_UNSET = object()

@dataclass(frozen=True)
class Change:
    owner: Any
    name: str
    old: Any
    new: Any

class Property:
    def __init__(self, default=None, *, validator=None, converter=None, readonly=False):
        self.default, self.validator, self.converter, self.readonly = default, validator, converter, readonly
        self.name = None
    def __set_name__(self, owner, name): self.name = name
    def _value(self, obj): return obj.__dict__.get(self.name, self.default() if callable(self.default) else self.default)
    def __get__(self, obj, owner=None): return self if obj is None else self._value(obj)
    def __set__(self, obj, value):
        if self.readonly: raise AttributeError(f"{self.name} is read-only")
        if self.converter: value = self.converter(value)
        if self.validator and not self.validator(value): raise ValueError(f"Invalid value for {self.name}: {value!r}")
        old = self._value(obj); obj.__dict__[self.name] = value
        if old != value and hasattr(obj, "_property_changed"): obj._property_changed(self.name, old, value)

class Binding:
    def __init__(self, target, target_name, source, source_name, transform=None):
        self.target, self.target_name, self.source, self.source_name, self.transform = target, target_name, source, source_name, transform
        self.active = True
        self._callback = lambda value, old=None: self._update(value)
        source.watch(source_name, self._callback)
        self._update(getattr(source, source_name))
    def _update(self, value):
        if self.active: setattr(self.target, self.target_name, self.transform(value) if self.transform else value)
    def unbind(self):
        self.active = False
        watchers = getattr(self.source, "_watchers", {}).get(self.source_name, [])
        if self._callback in watchers: watchers.remove(self._callback)

class ObservableMixin:
    def _property_changed(self, name, old, new):
        self.__dict__.setdefault("_watchers", {}).get(name, [])
        for cb in tuple(self.__dict__.get("_watchers", {}).get(name, ())): cb(new, old)
        hook = self.__dict__.get("_on_any_change")
        if hook: hook(Change(self, name, old, new))
        invalidate = getattr(self, "invalidate", None)
        if invalidate: invalidate(property=name)
    def watch(self, name, callback):
        self.__dict__.setdefault("_watchers", {}).setdefault(name, []).append(callback); return callback
    def unwatch(self, name, callback):
        try: self.__dict__.get("_watchers", {}).get(name, []).remove(callback)
        except ValueError: pass
    def bind(self, name, source, source_name, transform=None): return Binding(self, name, source, source_name, transform)
    @contextmanager
    def batch(self):
        pending=[]; old_hook=self.__dict__.get("_on_any_change")
        self.__dict__["_on_any_change"] = pending.append
        try: yield self
        finally:
            self.__dict__["_on_any_change"] = old_hook
            if pending and hasattr(self, "invalidate"): self.invalidate(property="batch")

def observable(cls):
    if not hasattr(cls, "_property_changed"):
        cls._property_changed = ObservableMixin._property_changed
        cls.watch = ObservableMixin.watch; cls.unwatch = ObservableMixin.unwatch; cls.bind = ObservableMixin.bind; cls.batch = ObservableMixin.batch
    return cls

def computed(fn):
    name = fn.__name__
    def getter(self):
        cache = self.__dict__.setdefault("_computed_cache", {})
        if name not in cache: cache[name] = fn(self)
        return cache[name]
    return property(getter)
