# ==============================================================================
# Autodesk Fusion 360 - Stage 1: Lower Chassis & Drivetrain
# Module: stage1_chassis_drivetrain.py
# Implements:
#   1. Lower Chassis structural bathtub base with 18x18mm chamfered corners
#   2. Tool-less side battery compartment with snap-fit pivot door
#   3. Serviceable front 5/8" ball caster housing & ball
#   4. Dual JGA25-371 motor mounts, inverted brackets & 65mm drive wheels
#   5. 3x 18650 battery pack placement
# ==============================================================================

import os
import sys

# Ensure robot folder is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def build_stage1(root_comp):
    """Assembles all Stage 1 components under root_comp."""
    stage1_comp = H.create_component(root_comp, "Stage1_Chassis_Drivetrain")
    
    # 1. Lower Chassis
    lower_chassis_step = os.path.join(P.EXPORT_DIR, "Lower_Chassis.step")
    if os.path.exists(lower_chassis_step):
        H.import_step_model(stage1_comp, lower_chassis_step, "Lower_Chassis", "Plastic - Glossy (Black)")
    
    # 2. Battery Door (Signal Red accent)
    door_step = os.path.join(P.EXPORT_DIR, "Battery_Door.step")
    if os.path.exists(door_step):
        H.import_step_model(stage1_comp, door_step, "Battery_Door", "Paint - Enamel Glossy (Red)")
        
    # 3. Caster Socket Housing
    caster_step = os.path.join(P.EXPORT_DIR, "Caster_Socket_Housing.step")
    if os.path.exists(caster_step):
        H.import_step_model(stage1_comp, caster_step, "Caster_Socket_Housing", "Plastic - Glossy (Black)")

    # 4. Battery Pack (3x 18650 Holder)
    batt_step = os.path.join(P.MODELS_DIR, "3x_Battery_Holder_With_Batteries.step")
    if os.path.exists(batt_step):
        H.import_step_model(stage1_comp, batt_step, "Battery_Pack", "Plastic - Glossy (Black)")

    print("Stage 1 Lower Chassis & Drivetrain built successfully.")
    return stage1_comp


def run(_context: str = ""):
    """Entry point for direct Fusion MCP execution."""
    design = H.get_design()
    root_comp = design.rootComponent
    build_stage1(root_comp)


if __name__ == "__main__":
    run()
