"""Cross-platform capability model for Windows, Android, iOS, Linux, macOS, Web and ChromeOS."""
from __future__ import annotations
from dataclasses import dataclass, field
import sys

PLATFORMS=("windows","android","ios","ipados","linux","macos","web","chromeos")

@dataclass
class PlatformCapabilities:
    name: str
    gpu: bool=True
    touch: bool=True
    keyboard: bool=True
    mouse: bool=True
    stylus: bool=True
    native_windows: bool=False
    native_menus: bool=False
    file_dialogs: bool=False
    notifications: bool=False
    camera: bool=False
    media: bool=False
    accessibility: bool=True
    safe_area: bool=False
    multiple_windows: bool=False
    wasm: bool=False
    features: set=field(default_factory=set)

CAPABILITIES={
    "windows":PlatformCapabilities("windows",native_windows=True,native_menus=True,file_dialogs=True,notifications=True,camera=True,media=True,multiple_windows=True),
    "android":PlatformCapabilities("android",touch=True,mouse=True,stylus=True,file_dialogs=True,notifications=True,camera=True,media=True,safe_area=True),
    "ios":PlatformCapabilities("ios",touch=True,mouse=False,stylus=True,file_dialogs=True,notifications=True,camera=True,media=True,safe_area=True),
    "ipados":PlatformCapabilities("ipados",touch=True,mouse=True,stylus=True,file_dialogs=True,notifications=True,camera=True,media=True,safe_area=True,multiple_windows=True),
    "linux":PlatformCapabilities("linux",native_menus=True,file_dialogs=True,notifications=True,camera=True,media=True,multiple_windows=True),
    "macos":PlatformCapabilities("macos",native_menus=True,file_dialogs=True,notifications=True,camera=True,media=True,multiple_windows=True),
    "web":PlatformCapabilities("web",mouse=True,touch=True,stylus=True,keyboard=True,file_dialogs=True,notifications=True,camera=True,media=True,safe_area=True,wasm=True),
    "chromeos":PlatformCapabilities("chromeos",mouse=True,touch=True,stylus=True,keyboard=True,file_dialogs=True,notifications=True,camera=True,media=True,multiple_windows=True),
}

def current_platform():
    p=sys.platform
    if p.startswith("win"): return "windows"
    if p=="darwin": return "macos"
    if p.startswith("linux"): return "linux"
    return "unknown"

def capabilities(platform=None): return CAPABILITIES.get(platform or current_platform(),PlatformCapabilities(platform or "unknown"))
def supports(feature,platform=None): return feature in capabilities(platform).features or bool(getattr(capabilities(platform),feature,False))

def available_platforms(): return tuple(CAPABILITIES)
