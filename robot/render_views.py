# ==============================================================================
# Autodesk Fusion 360 - Viewport Multi-Angle Renderer
# File: render_views.py
# Captures standard orthographic and isometric PNG renderings to previews/
# ==============================================================================

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def render_all_views():
    print("=== Rendering Autodesk Fusion 360 Multi-View Image Suite ===")
    os.makedirs(P.PREVIEW_DIR, exist_ok=True)
    
    views = [
        ("iso_front", "iso_front.png"),
        ("iso_rear", "iso_rear.png"),
        ("top", "top.png"),
        ("bottom", "bottom.png"),
        ("front", "front.png"),
        ("rear", "rear.png"),
        ("left", "left.png"),
        ("right", "right.png")
    ]
    
    for view_name, img_name in views:
        H.set_camera_view(view_name)
        out_img = os.path.join(P.PREVIEW_DIR, img_name)
        ok = H.capture_viewport(out_img, 1920, 1080)
        print(f"Rendered {view_name} -> {img_name} ({'SUCCESS' if ok else 'FAILED'})")

    H.set_camera_view("iso_front")
    print("=== Rendering Completed! ===")


def run(_context: str = ""):
    render_all_views()


if __name__ == "__main__":
    run()
