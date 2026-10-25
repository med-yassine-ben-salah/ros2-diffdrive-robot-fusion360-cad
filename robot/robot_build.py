# ==============================================================================
# Autodesk Fusion 360 - Complete Parametric Robot Build Runner
# File: robot_build.py
# Single-entry build, modeling & assembly runner for Autodesk Fusion 360.
#
# Can be run:
#   1. Interactively via the Fusion MCP Server (fusion_mcp_execute)
#   2. Directly inside Autodesk Fusion via Utilities > Scripts and Add-Ins (Shift+S)
#   3. Headless / automated via Fusion API scripts
# ==============================================================================

import os
import sys
import json
import traceback

import adsk.core
import adsk.fusion

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def build_full_robot(doc_name: str = "ROS2_DiffDrive_Robot"):
    """
    Builds and configures the complete ROS 2 DiffDrive Mobile Robot inside Fusion 360.
    """
    print(f"=== Starting Autodesk Fusion 360 Robot Build: {doc_name} ===")
    
    # 1. Initialize Document
    doc = H.init_document(doc_name, reset=True)
    design = H.get_design()
    root_comp = design.rootComponent
    
    # 2. Register all Parametric User Parameters
    print("--> Registering Parametric Constants in Fusion User Parameters table...")
    param_dict = {
        "CHASSIS_L": P.CHASSIS_L,
        "CHASSIS_W": P.CHASSIS_W,
        "GROUND_CLEARANCE": P.GROUND_CLEARANCE,
        "WHEEL_D": P.WHEEL_D,
        "WHEEL_TRACK": P.WHEEL_TRACK,
        "CASTER_X": P.CASTER_X,
        "CASTER_BALL_D": P.CASTER_BALL_D,
        "IMU_CENTROID_X": P.IMU_CENTROID_X,
        "Z_ROOF_TOP": P.Z_ROOF_TOP,
        "Z_LIDAR_ORIGIN": P.Z_LIDAR_ORIGIN,
        "LIDAR_NECK_CUT_R": P.LIDAR_NECK_CUT_R,
        "BATT_X": P.BATT_X,
        "BOTTOM_PLATE_T": P.BOTTOM_PLATE_T,
        "WALL_T": P.WALL_T,
        "DECK_T": P.DECK_T,
        "TOP_COVER_T": P.TOP_COVER_T
    }
    H.register_user_parameters(param_dict)
    
    # 3. Import Full Assembly Geometry
    assembly_step = os.path.join(P.EXPORT_DIR, "ROS2_DiffDrive_Robot_Assembly.step")
    if os.path.exists(assembly_step):
        print(f"--> Importing complete robot assembly from {assembly_step}...")
        robot_comp = H.import_step_model(root_comp, assembly_step, "ROS2_DiffDrive_Robot")
        print(f"    Imported {robot_comp.occurrences.count} sub-occurrences.")
    else:
        print(f"Assembly STEP not found at {assembly_step}; importing stages modularly...")
        import stage1_chassis_drivetrain
        import stage2_deck_lidar_imu
        import stage3_upper_enclosure_ui
        stage1_chassis_drivetrain.build_stage1(root_comp)
        stage2_deck_lidar_imu.build_stage2(root_comp)
        stage3_upper_enclosure_ui.build_stage3(root_comp)

    # 4. Configure Camera & Render Preview Images
    print("--> Generating multi-view preview renders...")
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
        try:
            H.set_camera_view(view_name)
            out_img = os.path.join(P.PREVIEW_DIR, img_name)
            H.capture_viewport(out_img, 1920, 1080)
            print(f"    Rendered: {img_name}")
        except Exception as e:
            print(f"    Warning: Could not render {view_name}: {e}")

    # Reset camera to default iso front
    H.set_camera_view("iso_front")
    
    print("=== Robot Build in Autodesk Fusion 360 Completed Successfully! ===")
    return True


def run(_context: str = ""):
    """Entry point for Fusion MCP execution."""
    build_full_robot()


if __name__ == "__main__":
    run()
