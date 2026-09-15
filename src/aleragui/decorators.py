from __future__ import annotations


def _tag(key, value=None):
    def deco(fn):
        setattr(fn, key, value if value is not None else True)
        return fn
    return deco


def canvas_event(name): return _tag("__alera_canvas_event__", name)
def draw(fn): return _tag("__alera_draw__")(fn)
def on_pointer_down(fn=None): return _tag("__alera_event__", "pointer_down")(fn) if fn else lambda f: _tag("__alera_event__", "pointer_down")(f)
def on_pointer_move(fn=None): return _tag("__alera_event__", "pointer_move")(fn) if fn else lambda f: _tag("__alera_event__", "pointer_move")(f)
def on_pointer_up(fn=None): return _tag("__alera_event__", "pointer_up")(fn) if fn else lambda f: _tag("__alera_event__", "pointer_up")(f)
def on_pointer_enter(fn=None): return _tag("__alera_event__", "pointer_enter")(fn) if fn else lambda f: _tag("__alera_event__", "pointer_enter")(f)
def on_pointer_leave(fn=None): return _tag("__alera_event__", "pointer_leave")(fn) if fn else lambda f: _tag("__alera_event__", "pointer_leave")(f)
def on_click(fn=None): return _tag("__alera_event__", "click")(fn) if fn else lambda f: _tag("__alera_event__", "click")(f)
def on_double_click(fn=None): return _tag("__alera_event__", "double_click")(fn) if fn else lambda f: _tag("__alera_event__", "double_click")(f)
def on_long_press(fn=None): return _tag("__alera_event__", "long_press")(fn) if fn else lambda f: _tag("__alera_event__", "long_press")(f)
def on_drag(fn=None): return _tag("__alera_event__", "drag")(fn) if fn else lambda f: _tag("__alera_event__", "drag")(f)
def on_drop(fn=None): return _tag("__alera_event__", "drop")(fn) if fn else lambda f: _tag("__alera_event__", "drop")(f)
def on_scroll(fn=None): return _tag("__alera_event__", "scroll")(fn) if fn else lambda f: _tag("__alera_event__", "scroll")(f)
def on_resize(fn=None): return _tag("__alera_event__", "resize")(fn) if fn else lambda f: _tag("__alera_event__", "resize")(f)
def on_move(fn=None): return _tag("__alera_event__", "move")(fn) if fn else lambda f: _tag("__alera_event__", "move")(f)
def on_mount(fn=None): return _tag("__alera_event__", "mount")(fn) if fn else lambda f: _tag("__alera_event__", "mount")(f)
def on_unmount(fn=None): return _tag("__alera_event__", "unmount")(fn) if fn else lambda f: _tag("__alera_event__", "unmount")(f)
def animatable(fn): return _tag("__alera_animatable__")(fn)
def observable(fn): return _tag("__alera_observable__")(fn)
def computed(fn): return _tag("__alera_computed__")(fn)
def command(name=None): return _tag("__alera_command__", name or True)
