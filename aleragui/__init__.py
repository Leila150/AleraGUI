"""AleraGUI - universal, backend-neutral 2D GUI framework foundation.

2D is the current core. The architecture is designed for native desktop,
mobile and web backends while keeping the Python widget API consistent.
"""
from .app import AleraGUI, Application, Window
from .canvas import Canvas, Layer, Brush, Path, Shape
from .types import *
from .geometry import *
from .geometry2d import *
from .rendering import Paint, DrawCommand, RenderList, Renderer, SoftwareRenderer, RenderNode, RenderEngine
from .rendering2d import RenderBatch, Renderer2D, RecordingRenderer, Gradient, Stroke, Fill, Clip, RenderState, RenderCache
from .layout_engine import resolve, box, distribute, flex_layout, grid_layout
from .properties import Property, Binding, ObservableMixin, observable, computed
from .property_catalog import *
from .widgets import Widget, Label, Button, TextInput, Image, ScrollView, Container
from .widgets_extra import Icon, Link, CheckBox, RadioButton, Switch, Slider, ProgressBar, Spinner, Stepper, List, Menu, NavigationBar, Sidebar, Breadcrumb, CodeEditor, RichText, Chart
from .widgets_catalog import *
from .containers import *
from .views import View, WebView, TreeView, TreeNode, CollectionView, ListView, GridView, TableView, DataGrid, StackView, MarkdownView, RichTextView, CodeView, ImageView, PDFView, MapView, CameraView, AudioPlayer, VideoView
from .overlays import *
from .events import Event, EventDispatcher, EVENTS
from .input import Pointer, Key, Touch, GestureRecognizer, FocusManager
from .input2 import InputEvent, MouseEvent, TouchEvent, PenEvent, KeyEvent, GamepadEvent, InputRouter, GestureEngine
from .accessibility import AccessibilityNode, AccessibilityManager
from .backend import Backend, HeadlessBackend, BackendRegistry, PlatformInfo, backends
from .platforms import PlatformCapabilities, CAPABILITIES, current_platform, capabilities, supports, available_platforms
from .tasks import Task, TaskManager
from .asyncio_gui import CancelScope, async_handler, debounce, throttle, gather, sleep, yield_control
from .theme import Theme, Palette, StyleSheet, LIGHT, DARK
from .themes import AdvancedTheme, ThemeTokens, LIGHT_MODERN, DARK_MODERN, HIGH_CONTRAST
from .decorators import *
from .animation import Animation, Timeline, Easing

__all__ = [name for name in globals() if not name.startswith('_')]
__version__ = "0.1.0-alpha"
