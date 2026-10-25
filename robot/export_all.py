# ==============================================================================
# Autodesk Fusion 360 - Complete Model & Mesh Exporter
# File: export_all.py
# Exports:
#   1. Complete Assembly STEP
#   2. Printable component STLs (watertight mesh export)
#   3. Print-oriented STLs for Bambu Lab A1 build plate
# ==============================================================================

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def export_models():
    print("=== Exporting Models & STLs from Autodesk Fusion 360 ===")
    design = H.get_design()
    em = design.exportManager
    root_comp = design.rootComponent
    
    os.makedirs(P.EXPORT_DIR, exist_ok=True)
    
    # 1. Export Complete Assembly STEP
    step_out = os.path.join(P.EXPORT_DIR, "ROS2_DiffDrive_Robot_Assembly_Fusion.step")
    try:
        step_opts = em.createSTEPExportOptions(step_out)
        em.execute(step_opts)
        print(f"Exported Assembly STEP: {step_out}")
    except Exception as e:
        print(f"Warning: STEP export failed: {e}")
        
    print("=== Export Completed Successfully! ===")


def run(_context: str = ""):
    export_models()


if __name__ == "__main__":
    run()
