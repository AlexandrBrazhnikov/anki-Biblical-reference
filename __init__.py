from aqt import gui_hooks

import os
import sys

addon_path = os.path.dirname(__file__)
vendor_path = os.path.join(addon_path, "vendor_BiblicalReference")

if vendor_path not in sys.path:
    sys.path.insert(0, vendor_path)

try:
    from .core import add_button_BiblicalReference
finally:
    if vendor_path in sys.path:
        sys.path.remove(vendor_path)

gui_hooks.editor_did_init_buttons.append(add_button_BiblicalReference)
