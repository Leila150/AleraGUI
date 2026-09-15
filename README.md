# AleraGUI

A universal Python GUI framework built around a backend-neutral, reactive **2D** engine.

## 2D-first architecture

AleraGUI currently provides the foundation for:

- Reactive widgets and automatic invalidation
- Custom, absolute, flex, grid, stack, anchor, constraint, responsive and dock layouts
- 2D Canvas drawing, paths, polygons and layers
- Geometry, hit testing, Bezier curves and transforms
- Backend-neutral render commands and render trees
- Animation/easing primitives
- Unified mouse, keyboard, touch and gesture input
- Accessibility semantics
- Themes and stylesheets
- Async/background tasks
- Desktop/mobile/web-oriented backend contracts
- Extensible widgets, views and overlays

## Reactive UI

```python
from aleragui import Label

label = Label("Hello")
label.text = "Updated"
label.position = (100, 200)
```

Property changes invalidate the affected widget automatically; a concrete platform renderer can consume those invalidations without requiring manual `refresh()` calls.

## CustomLayout

```python
from aleragui import CustomLayout, Label, Button

layout = CustomLayout()
label = layout.add(Label("Hello"))
button = layout.add(Button(text="Click"))
label.position = (100, 100)
button.position = (100, 180)
```

## Canvas

```python
from aleragui import Canvas

canvas = Canvas()
canvas.add_brush("#ff0000")
canvas.line((0, 0), (100, 100))
canvas.polygon([(50, 10), (100, 80), (10, 80)])
```

## Scope

AleraGUI is a **GUI framework**, not an application/web router. Visual navigation such as pages, tabs, drawers and views belongs in the GUI layer; URL/API/server routing does not.

3D rendering is intentionally not included in the current 2D implementation phase.
