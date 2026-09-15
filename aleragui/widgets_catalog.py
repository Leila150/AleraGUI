"""AleraGUI's expandable 1000+ widget catalog.

The catalog uses lightweight typed widget classes so applications can discover,
style, subclass and register a huge vocabulary without coupling core widgets to
a specific native renderer. Platform backends decide how each widget is painted.
"""
from __future__ import annotations
from .widgets import Widget
from .property_catalog import ALL_PROPERTIES

class CatalogWidget(Widget):
    widget_category = "generic"
    widget_variant = "base"
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        for name in ALL_PROPERTIES:
            if not hasattr(self, name): setattr(self, name, kwargs.get(name, None))
    def set(self, **properties):
        for key,value in properties.items(): setattr(self,key,value)
        return self

WIDGET_TYPES = {}
BASE_WIDGET_NAMES = ['Button', 'Label', 'Text', 'Icon', 'Image', 'Avatar', 'Badge', 'Chip', 'Card', 'Panel', 'Surface', 'Container', 'Header', 'Footer', 'Toolbar', 'Sidebar', 'Navbar', 'Breadcrumb', 'Tabs', 'Tab', 'Page', 'Drawer', 'Dialog', 'Modal', 'Popup', 'Popover', 'Tooltip', 'Menu', 'MenuItem', 'Dropdown', 'Select', 'ComboBox', 'Autocomplete', 'TextInput', 'NumberInput', 'PasswordInput', 'SearchInput', 'CodeInput', 'TextArea', 'Editor', 'RichText', 'Markdown', 'Link', 'CheckBox', 'Radio', 'Switch', 'Toggle', 'Slider', 'RangeSlider', 'Stepper', 'Progress', 'Spinner', 'Gauge', 'Meter', 'Rating', 'Calendar', 'DatePicker', 'TimePicker', 'DateTimePicker', 'ColorPicker', 'FilePicker', 'FolderPicker', 'Upload', 'Download', 'List', 'ListItem', 'Grid', 'GridItem', 'Table', 'TableRow', 'TableCell', 'Tree', 'TreeNode', 'DataGrid', 'Collection', 'Carousel', 'Pager', 'Pagination', 'ScrollView', 'SplitView', 'Stack', 'Flow', 'Flex', 'GridLayout', 'Canvas', 'Chart', 'LineChart', 'BarChart', 'PieChart', 'AreaChart', 'ScatterChart', 'Map', 'Camera', 'Audio', 'Video', 'WebView', 'PDF', 'CodeView', 'Console', 'Terminal', 'Form', 'FormField', 'Validator', 'Separator', 'Spacer', 'Skeleton', 'Placeholder', 'Toast', 'Snackbar']
VARIANTS = ['Primary', 'Secondary', 'Compact', 'Large', 'Small', 'Outlined', 'Filled', 'Flat', 'Adaptive', 'Pro']

for _base in BASE_WIDGET_NAMES:
    _base_cls = type(_base, (CatalogWidget,), {"widget_category": _base.lower()})
    globals()[_base] = _base_cls
    WIDGET_TYPES[_base] = _base_cls
    for _variant in VARIANTS:
        _name = _variant + _base
        _cls = type(_name, (_base_cls,), {"widget_variant": _variant.lower()})
        globals()[_name] = _cls
        WIDGET_TYPES[_name] = _cls

WIDGET_COUNT = len(WIDGET_TYPES)

def get_widget(name): return WIDGET_TYPES[name]
def list_widgets(): return tuple(WIDGET_TYPES)
def register_widget(name, cls):
    if not isinstance(name,str) or not name.isidentifier(): raise ValueError("Widget name must be a valid identifier")
    if not isinstance(cls,type) or not issubclass(cls,Widget): raise TypeError("Widget class must inherit Widget")
    WIDGET_TYPES[name]=cls; globals()[name]=cls; return cls

__all__ = ["CatalogWidget","WIDGET_TYPES","WIDGET_COUNT","get_widget","list_widgets","register_widget"] + list(WIDGET_TYPES)
