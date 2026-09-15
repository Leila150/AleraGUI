"""2D animation, easing and timeline primitives."""
from __future__ import annotations
import math

class Easing:
    linear=staticmethod(lambda t:t)
    ease_in=staticmethod(lambda t:t*t)
    ease_out=staticmethod(lambda t:1-(1-t)*(1-t))
    ease_in_out=staticmethod(lambda t:2*t*t if t<.5 else 1-((-2*t+2)**2)/2)
    smoothstep=staticmethod(lambda t:t*t*(3-2*t))
    cubic_in=staticmethod(lambda t:t**3)
    cubic_out=staticmethod(lambda t:1-(1-t)**3)
    sine_in=staticmethod(lambda t:1-math.cos(t*math.pi/2))
    sine_out=staticmethod(lambda t:math.sin(t*math.pi/2))
    sine_in_out=staticmethod(lambda t:-(math.cos(math.pi*t)-1)/2)
    bounce=staticmethod(lambda t: 1-(1-t)*(1-t)*abs(math.sin(t*math.pi*4)))
    def custom(fn):
        if not callable(fn): raise TypeError("Custom easing must be callable")
        return fn

class Animation:
    def __init__(self,duration=1,easing=Easing.linear,repeat=0,yoyo=False,**properties):
        self.duration=duration; self.easing=easing; self.repeat=repeat; self.yoyo=yoyo; self.properties=properties
        self.target=None; self.running=False; self.paused=False; self.progress=0; self.elapsed=0
        self.on_start=[]; self.on_update=[]; self.on_complete=[]; self.on_cancel=[]
    def play(self,target=None):
        if target is not None: self.target=target
        if self.target is None: raise ValueError("Animation requires a target")
        self.running=True; self.paused=False
        for cb in self.on_start: cb(self)
        return self
    def pause(self): self.paused=True; return self
    def resume(self): self.paused=False; return self
    def stop(self): self.running=False; return self
    def cancel(self): self.running=False; [cb(self) for cb in self.on_cancel]; return self
    def restart(self): self.progress=0; self.elapsed=0; return self.play()
    def reverse(self): self.yoyo=not self.yoyo; return self
    def seek(self,progress): self.progress=max(0,min(1,progress)); return self
    def then(self,animation): return Sequence(self,animation)
    def update(self,progress):
        self.progress=max(0,min(1,progress)); t=self.easing(self.progress)
        for name,end in self.properties.items():
            if isinstance(end,(int,float)):
                start=getattr(self.target,name,end); setattr(self.target,name,start+(end-start)*t)
        for cb in self.on_update: cb(self,self.progress)
        if self.progress>=1:
            self.running=False
            for cb in self.on_complete: cb(self)
        return self

class Sequence:
    def __init__(self,*animations): self.animations=list(animations); self.index=0
    def play(self,target=None):
        for a in self.animations: a.play(target)
        return self

class Timeline:
    def __init__(self): self.items=[]; self.playing=False; self.time=0; self.duration=0
    def add(self,animation,at=0): self.items.append((at,animation)); self.duration=max(self.duration,at+animation.duration); return animation
    def animate(self,target,**kwargs): return self.add(Animation(**kwargs),0)
    def delay(self,seconds): self.duration+=seconds; return self
    def parallel(self,*animations):
        for a in animations: self.add(a, self.time)
        return self
    def sequence(self,*animations):
        t=self.time
        for a in animations: self.add(a,t); t+=a.duration
        self.time=t; return self
    def play(self): self.playing=True; return self
    def pause(self): self.playing=False; return self
    def stop(self): self.playing=False; self.time=0; return self
    def seek(self,time): self.time=max(0,min(self.duration,time)); return self
