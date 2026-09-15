"""AleraGUI - universal, backend-neutral 2D GUI framework foundation.

The current release focuses on the complete 2D architecture. 3D is deliberately
not imported yet so its future renderer can be added without destabilizing 2D.
"""
from .app import AleraGUI, Application, Window
from .canvas import Canvas, Layer, Brush, Path, Shape
from .types import *
from .geometry import *
from .rendering import Paint, DrawCommand, RenderList, Renderer, SoftwareRenderer, RenderNode, RenderEngine
from .layout_engine import resolve, box, distribute, flex_layout, grid_layout
from .properties import Property, Binding, ObservableMixin, observable, computed
from .widgets import Widget, Label, Button, TextInput, Image, ScrollView, Container
from .widgets_extra import Icon, Link, CheckBox, RadioButton, Switch, Slider, ProgressBar, Spinner, Stepper, List, Menu, NavigationBar, Sidebar, Breadcrumb, CodeEditor, RichText, Chart
from .containers import *
from .views import View, WebView, TreeView, TreeNode, CollectionView, ListView, GridView, TableView, DataGrid, StackView, MarkdownView, RichTextView, CodeView, ImageView, PDFView, MapView, CameraView, AudioPlayer, VideoView
from .overlays import *
from .events import Event, EventDispatcher, EVENTS
from .input import Pointer, Key, Touch, GestureRecognizer, FocusManager
from .accessibility import AccessibilityNode, AccessibilityManager
from .backend import Backend, HeadlessBackend, BackendRegistry, PlatformInfo, backends
from .tasks import Task, TaskManager
from .theme import Theme, Palette, StyleSheet, LIGHT, DARK
from .decorators import *
from .animation import Animation, Timeline, Easing

__all__ = [name for name in globals() if not name.startswith('_')]
__version__ = "0.1.0-alpha"
