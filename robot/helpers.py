# ==============================================================================
# Autodesk Fusion 360 - Robot Assembly & Modeling Helpers
# Module: helpers.py
# Provides high-level Fusion API utilities for:
#   - Document initialization & user parameter registration
#   - Component creation, occurrence management & B-Rep assembly
#   - Material & Appearance assignment (PLA Matte Black, Signal Red, Steel, etc.)
#   - Camera manipulation (orthographic, isometric, custom view angles)
#   - Multi-view high-res image rendering
#   - STEP / STL import and export
# ==============================================================================

import os
import sys
import math
import traceback

import adsk.core
import adsk.fusion

# Unit conversion factor: Fusion internal length unit is Centimeter (cm)
# Robot parameters are specified in Millimeters (mm).
MM_TO_CM = 0.1
CM_TO_MM = 10.0


def get_app() -> adsk.core.Application:
    """Returns the running Fusion 360 Application instance."""
    app = adsk.core.Application.get()
    if not app:
        raise RuntimeError("Unable to connect to Autodesk Fusion Application.")
    return app


def get_design() -> adsk.fusion.Design:
    """Returns the active Fusion 360 Design product."""
    app = get_app()
    design = app.activeProduct
    if not isinstance(design, adsk.fusion.Design):
        raise RuntimeError("Active product in Fusion is not a Design document.")
    return design


def init_document(doc_name: str = "ROS2_DiffDrive_Robot", reset: bool = False) -> adsk.core.Document:
    """
    Ensures an active document is ready. If reset is True, clears existing
    occurrences in the root component.
    """
    app = get_app()
    doc = app.activeDocument
    if doc is None or (reset and not doc.isSaved):
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    
    design = get_design()
    root_comp = design.rootComponent

    if reset:
        # Delete existing occurrences
        while root_comp.occurrences.count > 0:
            root_comp.occurrences.item(0).deleteMe()

    return doc


def register_user_parameters(params_dict: dict):
    """
    Registers a dictionary of numeric parameters into Fusion's User Parameter table
    so they appear under Modify > Change Parameters.
    """
    design = get_design()
    user_params = design.userParameters

    for name, val in params_dict.items():
        if isinstance(val, (int, float)):
            existing = user_params.itemByName(name)
            expr = f"{val} mm"
            if existing is None:
                try:
                    user_params.add(name, adsk.core.ValueInput.createByString(expr), "mm", f"Parametric constant {name}")
                except Exception:
                    pass
            else:
                try:
                    existing.expression = expr
                except Exception:
                    pass


def get_or_create_appearance(appearance_name: str, base_color: tuple = None) -> adsk.core.Appearance:
    """
    Searches for an appearance by name in the active design or Fusion Appearance Library.
    If not found, optionally creates a custom color appearance.
    """
    app = get_app()
    design = get_design()

    # 1. Check active design appearances
    appr = design.appearances.itemByName(appearance_name)
    if appr:
        return appr

    # 2. Check Fusion Appearance Library
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    if lib:
        lib_appr = lib.appearances.itemByName(appearance_name)
        if lib_appr:
            try:
                copied = design.appearances.addByCopy(lib_appr, appearance_name)
                return copied
            except Exception:
                return lib_appr

    return None


def apply_appearance(entity, appearance_name: str):
    """Applies a named appearance to a component or B-Rep body."""
    try:
        appr = get_or_create_appearance(appearance_name)
        if appr and hasattr(entity, "appearance"):
            entity.appearance = appr
    except Exception as e:
        print(f"Warning: Could not apply appearance '{appearance_name}': {e}")


def create_component(parent_comp: adsk.fusion.Component, name: str) -> adsk.fusion.Component:
    """Creates a new child component under parent_comp with the specified name."""
    transform = adsk.core.Matrix3D.create()
    occ = parent_comp.occurrences.addNewComponent(transform)
    comp = occ.component
    comp.name = name
    return comp


def import_step_model(target_comp: adsk.fusion.Component, step_path: str, comp_name: str = None, appearance: str = None):
    """
    Imports a STEP model file into target_comp, optionally naming it and applying an appearance.
    """
    if not os.path.exists(step_path):
        raise FileNotFoundError(f"STEP file not found: {step_path}")

    app = get_app()
    im = app.importManager
    opts = im.createSTEPImportOptions(step_path)
    
    sub_comp = create_component(target_comp, comp_name if comp_name else os.path.splitext(os.path.basename(step_path))[0])
    im.importToTarget(opts, sub_comp)

    if appearance:
        apply_appearance(sub_comp, appearance)

    return sub_comp


def set_camera_view(view_name: str):
    """
    Positions the active viewport camera for standardized robot inspection angles:
    - 'iso_front', 'iso_rear', 'top', 'bottom', 'front', 'rear', 'left', 'right'
    """
    app = get_app()
    vp = app.activeViewport
    camera = vp.camera
    camera.cameraType = adsk.core.CameraTypes.OrthographicCameraType

    # Robot bounding center in cm: X = 7.0 cm, Y = 0.0 cm, Z = 5.5 cm
    target = adsk.core.Point3D.create(7.0, 0.0, 5.5)

    if view_name == "iso_front":
        eye = adsk.core.Point3D.create(40.0, -35.0, 30.0)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    elif view_name == "iso_rear":
        eye = adsk.core.Point3D.create(-30.0, 35.0, 25.0)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    elif view_name == "top":
        eye = adsk.core.Point3D.create(7.0, 0.0, 60.0)
        up = adsk.core.Vector3D.create(1.0, 0.0, 0.0)
    elif view_name == "bottom":
        eye = adsk.core.Point3D.create(7.0, 0.0, -60.0)
        up = adsk.core.Vector3D.create(1.0, 0.0, 0.0)
    elif view_name == "front":
        eye = adsk.core.Point3D.create(60.0, 0.0, 5.5)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    elif view_name == "rear":
        eye = adsk.core.Point3D.create(-45.0, 0.0, 5.5)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    elif view_name == "left":
        eye = adsk.core.Point3D.create(7.0, 50.0, 5.5)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    elif view_name == "right":
        eye = adsk.core.Point3D.create(7.0, -50.0, 5.5)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    else:
        # Default iso
        eye = adsk.core.Point3D.create(35.0, -35.0, 25.0)
        up = adsk.core.Vector3D.create(0.0, 0.0, 1.0)

    camera.eye = eye
    camera.target = target
    camera.upVector = up
    camera.isFitView = True
    vp.camera = camera
    vp.refresh()


def capture_viewport(output_path: str, width: int = 1920, height: int = 1080) -> bool:
    """Exports the current viewport render to an image file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    app = get_app()
    vp = app.activeViewport
    return vp.saveAsImageFile(output_path, width, height)
