"""Async-first GUI helpers: cancellation, throttling, debouncing and UI-safe calls."""
from __future__ import annotations
import asyncio
from functools import wraps

class CancelScope:
    def __init__(self): self.tasks=set(); self.cancelled=False
    def create(self,coro):
        if self.cancelled: raise asyncio.CancelledError
        task=asyncio.create_task(coro); self.tasks.add(task); task.add_done_callback(self.tasks.discard); return task
    def cancel(self):
        self.cancelled=True
        for task in tuple(self.tasks): task.cancel()
    async def __aenter__(self): return self
    async def __aexit__(self,*exc): self.cancel()

async def sleep(seconds): await asyncio.sleep(seconds)
async def yield_control(): await asyncio.sleep(0)

def async_handler(callback):
    @wraps(callback)
    def wrapper(*args,**kwargs): return asyncio.create_task(callback(*args,**kwargs))
    return wrapper

def debounce(wait):
    def deco(fn):
        state={"task":None}
        async def runner(*args,**kwargs):
            await asyncio.sleep(wait); return await fn(*args,**kwargs)
        @wraps(fn)
        def wrapped(*args,**kwargs):
            if state["task"] and not state["task"].done(): state["task"].cancel()
            state["task"]=asyncio.create_task(runner(*args,**kwargs)); return state["task"]
        return wrapped
    return deco

def throttle(interval):
    def deco(fn):
        state={"last":0.0}
        import time
        @wraps(fn)
        def wrapped(*args,**kwargs):
            now=time.monotonic()
            if now-state["last"]>=interval:
                state["last"]=now; return fn(*args,**kwargs)
        return wrapped
    return deco

async def gather(*aws,return_exceptions=False): return await asyncio.gather(*aws,return_exceptions=return_exceptions)
