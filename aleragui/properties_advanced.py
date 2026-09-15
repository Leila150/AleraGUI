"""Advanced reactive property primitives: validation, coercion, defaults, aliases and transactions."""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class PropertySpec:
    name: str
    default: Any = None
    validator: Callable[[Any], bool] | None = None
    coerce: Callable[[Any], Any] | None = None
    aliases: tuple[str, ...] = ()

class AdvancedProperty:
    def __init__(self, default=None, *, validator=None, coerce=None, aliases=()):
        self.spec = None
        self.default, self.validator, self.coerce, self.aliases = default, validator, coerce, tuple(aliases)
        self.name = None
    def __set_name__(self, owner, name):
        self.name = name; self.spec = PropertySpec(name, self.default, self.validator, self.coerce, self.aliases)
        for alias in self.aliases:
            setattr(owner, alias, _Alias(self))
    def _value(self, obj): return obj.__dict__.get(self.name, self.default() if callable(self.default) else self.default)
    def __get__(self,obj,owner=None): return self if obj is None else self._value(obj)
    def __set__(self,obj,value):
        if self.coerce: value=self.coerce(value)
        if self.validator and not self.validator(value): raise ValueError(f"Invalid value for {self.name}: {value!r}")
        old=self._value(obj); obj.__dict__[self.name]=value
        if old != value and hasattr(obj,"invalidate"): obj.invalidate(property=self.name)

class _Alias:
    def __init__(self,target): self.target=target
    def __get__(self,obj,owner=None): return self.target.__get__(obj,owner)
    def __set__(self,obj,value): self.target.__set__(obj,value)

def enum(*values): return lambda value: value in values
def number(minimum=None, maximum=None):
    def check(value):
        if not isinstance(value,(int,float)): return False
        return (minimum is None or value>=minimum) and (maximum is None or value<=maximum)
    return check

def one_of(*types): return lambda value: isinstance(value,types)
def positive(value): return isinstance(value,(int,float)) and value>=0

def transaction(obj):
    @contextmanager
    def scope():
        old=getattr(obj,"_invalidated",False); obj.__dict__["_property_transaction"]=True
        try: yield obj
        finally:
            obj.__dict__.pop("_property_transaction",None); obj.__dict__["_invalidated"]=True
            if hasattr(obj,"invalidate"): obj.invalidate(property="transaction")
    return scope()
