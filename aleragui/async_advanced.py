"""Async primitives for responsive GUI applications."""
from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Awaitable,Callable,Any

@dataclass
class Progress:
    value:float=0.0; message:str=''
    def update(self,value,message=None): self.value=max(0,min(1,value)); self.message=message if message is not None else self.message; return self

class AsyncScope:
    def __init__(self): self.tasks=set(); self.cancelled=False
    def create_task(self,coro):
        if self.cancelled: raise asyncio.CancelledError()
        task=asyncio.create_task(coro); self.tasks.add(task); task.add_done_callback(self.tasks.discard); return task
    def cancel(self):
        self.cancelled=True
        for task in tuple(self.tasks): task.cancel()
    async def wait(self):
        if self.tasks: await asyncio.gather(*tuple(self.tasks),return_exceptions=True)
    async def __aenter__(self): return self
    async def __aexit__(self,*exc): self.cancel(); await self.wait()

async def run_in_executor(func,*args,executor=None):
    loop=asyncio.get_running_loop(); return await loop.run_in_executor(executor,lambda:func(*args))

async def iterate(awaitable,callback=None):
    result=await awaitable
    if callback: callback(result)
    return result

async def timeout(coro,seconds): return await asyncio.wait_for(coro,seconds)
async def next_frame(): await asyncio.sleep(0)
async def sleep_frame(seconds=0): await asyncio.sleep(seconds)

class AsyncSignal:
    def __init__(self): self._listeners=[]
    def connect(self,callback): self._listeners.append(callback); return callback
    def disconnect(self,callback):
        if callback in self._listeners:self._listeners.remove(callback)
    async def emit(self,*args,**kwargs):
        for cb in tuple(self._listeners):
            result=cb(*args,**kwargs)
            if asyncio.iscoroutine(result): await result
