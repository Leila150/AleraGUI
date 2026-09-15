"""Large, reusable property vocabulary for AleraGUI widgets.

These names are intentionally backend-neutral. Widgets can opt into any of them
without forcing a platform implementation into the public API.
"""
from __future__ import annotations

COMMON_PROPERTIES = (
    "id", "key", "name", "tag", "position", "size", "width", "height",
    "min_width", "min_height", "max_width", "max_height", "x", "y",
    "visible", "enabled", "opacity", "rotation", "scale", "z_index",
    "anchor", "origin", "transform", "layout", "layout_order", "margin",
    "padding", "background", "foreground", "border_width", "border_color",
    "border_radius", "border_style", "outline_width", "outline_color",
    "shadow", "shadow_color", "shadow_offset", "shadow_blur", "shadow_spread",
    "clip", "clip_radius", "overflow", "cursor", "tooltip", "style_class",
    "theme", "theme_variant", "data", "focusable", "tab_index", "draggable",
    "droppable", "selectable", "accessibility_label", "accessibility_hint",
    "accessibility_role", "accessibility_value", "high_contrast", "reduced_motion",
)
TEXT_PROPERTIES = (
    "text", "font_family", "font_size", "font_weight", "font_style", "font_stretch",
    "text_color", "text_align", "vertical_align", "line_height", "line_spacing",
    "letter_spacing", "word_spacing", "wrap", "max_lines", "ellipsis", "direction",
    "locale", "language", "text_transform", "decoration", "decoration_color",
    "decoration_style", "selectable", "copyable", "editable", "spellcheck",
)
MEDIA_PROPERTIES = (
    "source", "placeholder", "error_source", "fit", "alignment", "aspect_ratio",
    "keep_aspect_ratio", "crop", "crop_position", "flip_horizontal", "flip_vertical",
    "tint", "brightness", "contrast", "saturation", "gamma", "blur", "sharpen",
    "interpolation", "antialiasing", "cache", "preload", "loading", "progress",
)
INPUT_PROPERTIES = (
    "value", "default_value", "placeholder", "read_only", "required", "invalid",
    "validation_message", "max_length", "min_length", "pattern", "keyboard_type",
    "return_key", "auto_complete", "cursor_position", "selection_start",
    "selection_end", "cursor_color", "cursor_width", "selection_color", "undo_enabled",
    "redo_enabled", "multiline", "password", "input_mode", "capture_keys",
)
LAYOUT_PROPERTIES = (
    "direction", "spacing", "row_spacing", "column_spacing", "gap", "wrap",
    "justify", "align", "align_items", "align_content", "grid_columns", "grid_rows",
    "grid_gap", "grid_column", "grid_row", "flex_grow", "flex_shrink", "flex_basis",
    "order", "dock", "fill", "stretch", "distribution", "constraints", "breakpoints",
)
EFFECT_PROPERTIES = (
    "blur", "brightness", "contrast", "saturation", "hue", "grayscale", "invert",
    "sepia", "drop_shadow", "backdrop_blur", "blend_mode", "mask", "mask_source",
    "gradient", "noise", "pixelate", "glow", "inner_shadow", "outer_shadow",
)
ALL_PROPERTIES = tuple(dict.fromkeys(COMMON_PROPERTIES + TEXT_PROPERTIES + MEDIA_PROPERTIES + INPUT_PROPERTIES + LAYOUT_PROPERTIES + EFFECT_PROPERTIES))

def property_names(*groups):
    return tuple(dict.fromkeys(name for group in groups for name in group))
