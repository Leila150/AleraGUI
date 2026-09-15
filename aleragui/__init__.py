"""AleraGUI - universal, reactive, backend-neutral 2D GUI framework."""
from .app import AleraGUI, Application, Window
from .runtime import DuplicateIDError, IDRegistry, HitResult, hit_test, EventRouter, WidgetTree, FrameScheduler, InvalidationQueue
from .canvas import Canvas, Layer, Brush, Path, Shape
from .types import *
from .geometry import *
from .geometry2d import *
from .geometry_advanced import *
from .rendering import Paint, DrawCommand, RenderList, Renderer, SoftwareRenderer, RenderNode, RenderEngine
from .rendering2d import RenderBatch, Renderer2D, RecordingRenderer, Gradient, Stroke, Fill, Clip, RenderState, RenderCache
from .rendering_advanced import Shader, Effect, RenderTarget, RenderPass, Batch, RenderGraph, RendererFeatures, RenderContext
from .layout_engine import resolve, box, distribute, flex_layout, grid_layout
from .properties import Property, Binding, ObservableMixin, observable, computed
from .properties_advanced import PropertySpec, AdvancedProperty, enum, number, one_of, positive, transaction
from .property_catalog import *
from .widgets import Widget, Label, Button, TextInput, Image, ScrollView, Container, Reactive
from .widgets_extra import Icon, Link, CheckBox, RadioButton, Switch, Slider, ProgressBar, Spinner, Stepper, List, Menu, NavigationBar, Sidebar, Breadcrumb, CodeEditor, RichText, Chart
from .widgets_catalog import *
from .containers import *
from .views import View, WebView, TreeView, TreeNode, CollectionView, ListView, GridView, TableView, DataGrid, StackView, MarkdownView, RichTextView, CodeView, ImageView, PDFView, MapView, CameraView, AudioPlayer, VideoView
from .overlays import *
from .events import Event, EventDispatcher, EVENTS
from .input import Pointer, Key, Touch, GestureRecognizer, FocusManager
from .input2 import InputEvent, MouseEvent, TouchEvent, PenEvent, KeyEvent, GamepadEvent, InputRouter, GestureEngine
from .input_advanced import DeviceKind, InputEvent as AdvancedInputEvent, PointerState, InputManager, ShortcutManager, Gesture, GestureManager
from .accessibility import AccessibilityNode, AccessibilityManager
from .backend import Backend, HeadlessBackend, BackendRegistry, PlatformInfo, backends
from .platforms import PlatformCapabilities, CAPABILITIES, current_platform, capabilities, supports, available_platforms
from .tasks import Task, TaskManager
from .asyncio_gui import CancelScope, async_handler, debounce, throttle, gather, sleep, yield_control
from .async_advanced import AsyncScope, Progress, AsyncSignal, run_in_executor, iterate, timeout, next_frame, sleep_frame
from .theme import Theme as BaseTheme, Palette, StyleSheet, LIGHT, DARK
from .themes import AdvancedTheme, ThemeTokens as LegacyThemeTokens, LIGHT_MODERN, DARK_MODERN, HIGH_CONTRAST
from .theme_advanced import Theme, ThemeTokens, StyleRule, Cascade, LIGHT_PRO, DARK_PRO
from .decorators import *
from .animation import Animation, Timeline, Easing

__all__=[name for name in globals() if not name.startswith("_")]
__version__="0.1.0-alpha"
