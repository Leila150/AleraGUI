"""AleraGUI - universal 2D GUI foundation.

The public API is backend-neutral. 3D is intentionally not part of this
initial foundation.
"""
from .app import AleraGUI, Application
from .canvas import Canvas, Layer, Brush, Path, Shape
from .types import (
    Point, Vector2, Size, Rect, Color, Gradient, GradientStop, Font,
    Shadow, Transform, Matrix3, Margin, Padding, Radius,
    Px, Percent, Dp, Sp, Em, Rem, Auto, Fill, Min, Max, Clamp,
)
from .widgets import Widget, Label, Button, TextInput, Image, ScrollView, Container
from .containers import (
    Layout, CustomLayout, AbsoluteLayout, FlexLayout, GridLayout,
    StackLayout, FlowLayout, WrapLayout, AnchorLayout, ConstraintLayout,
    ResponsiveLayout, DockLayout, OverlayContainer, LayerContainer,
    SplitView, TabView, PageView, Drawer, Panel, Card, Frame, Surface,
)
from .events import Event, EventDispatcher
from .decorators import (
    page, draw, canvas_event, observable, computed, bind, watch,
    animatable, command, accessible, shortcut, background, task, worker,
    validator, serializable, deserializable,
)
from .animation import Animation, Timeline, Easing

__all__ = [name for name in globals() if not name.startswith('_')]
__version__ = "0.1.0-alpha"
