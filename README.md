# AleraGUI

A universal Python GUI framework designed around a reactive UI model and a backend-neutral rendering architecture.

## Current development stage

**2D foundation only.** 3D rendering is intentionally not implemented yet.

The first foundation contains:

- Rich 2D geometry and unit types
- Colors, gradients, fonts, shadows and transforms
- 2D Canvas and drawing primitives
- Lines, polylines, polygons, rectangles, circles, ellipses, arcs, sectors and stars
- Vector paths and Bézier-style path commands
- Text and image drawables
- Brushes and erasing
- Canvas layers and compositing metadata
- Event emitter infrastructure
- Drawing, pointer, gesture and lifecycle decorators
- Observable/computed/binding/command decorator metadata

## Design goals

AleraGUI is intended to provide one GUI API that can eventually target desktop platforms, mobile applications and the web. Platform rendering, packaging and native integration belong to later backend layers; the core API remains platform-neutral.

The project deliberately does **not** contain a URL router, HTTP server or backend framework. AleraGUI is a GUI framework.

## Example

```python
from aleragui import Canvas, Color

canvas = Canvas(width=800, height=600)
canvas.add_brush("#ff3366", size=12, smoothing=0.8)
canvas.polygon([(100, 100), (300, 80), (250, 250)], fill=Color("#3366ff"))
canvas.circle((400, 300), 80, fill=Color("#22cc88"))
canvas.line((0, 0), (800, 600), width=4)
```

This API is the beginning of the 2D engine, not the final renderer. Rendering backends will be added without changing the public drawing model.
