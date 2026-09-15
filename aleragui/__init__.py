"""AleraGUI - universal, backend-neutral 2D GUI foundation.

3D is intentionally excluded from this release; the architecture leaves room
for a future separate 3D subsystem without changing the 2D API.
"""
from .app import AleraGUI, Application, Window
from .canvas import Canvas, Layer, Brush, Path, Shape
from .types import *
from .widgets import Widget, Label, Button, TextInput, Image, ScrollView, Container
from .containers import *
from .views import View, WebView, TreeView, TreeNode, CollectionView, ListView, GridView, TableView, DataGrid, StackView, MarkdownView, RichTextView, CodeView, ImageView, PDFView, MapView, CameraView, AudioPlayer, VideoView
from .overlays import *
from .events import Event, EventDispatcher, EVENTS
from .decorators import *
from .animation import Animation, Timeline, Easing

__all__ = [name for name in globals() if not name.startswith('_')]
__version__ = "0.1.0-alpha"
