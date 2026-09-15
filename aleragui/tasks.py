"""Async and background task helpers that keep UI work cancellable."""
from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Task:
    def __init__(self, awaitable=None): self.awaitable=awaitable; self.future=None
    def start(self):
        if self.awaitable is None: return self
        self.future=asyncio.create_task(self.awaitable) if hasattr(self.awaitable,"__await__") else None; return self
    def cancel(self):
        if self.future: self.future.cancel()
    @property
    def done(self): return bool(self.future and self.future.done())

class TaskManager:
    def __init__(self,max_workers=4): self.executor=ThreadPoolExecutor(max_workers=max_workers); self.tasks=set()
    def run(self,fn,*args,**kwargs):
        future=self.executor.submit(fn,*args,**kwargs); self.tasks.add(future); future.add_done_callback(self.tasks.discard); return future
    async def run_async(self,fn,*args,**kwargs): return await asyncio.to_thread(fn,*args,**kwargs)
    def shutdown(self): self.executor.shutdown(wait=False,cancel_futures=True)
