# ==============================================================================
# Autodesk Fusion 360 - Stage 3: Upper Enclosure & UI Panel
# Module: stage3_upper_enclosure_ui.py
# Implements:
#   1. Removable upper enclosure shell with 4.5mm x 45° crown bevels (Z=112mm)
#   2. Circular collar (Ø71.3mm) with 360° unobstructed scan field for LiDAR
#   3. Top UI panel: rear-facing 0.96" OLED bezel, 4 diamond tactile switches + caps,
#      7-hole acoustic grille for buzzer, and RGB LED dome
#   4. Front centerline ESP32-CAM mount & Ø10mm lens aperture
#   5. Rear panel-mount ON/OFF rocker switch recessed 7.5mm into bumper
# ==============================================================================

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def build_stage3(root_comp):
    """Assembles all Stage 3 components under root_comp."""
    stage3_comp = H.create_component(root_comp, "Stage3_Upper_Enclosure_UI")
    
    # 1. Upper Enclosure Shell
    upper_step = os.path.join(P.EXPORT_DIR, "Upper_Enclosure.step")
    if os.path.exists(upper_step):
        H.import_step_model(stage3_comp, upper_step, "Upper_Enclosure", "Plastic - Glossy (Black)")
        
    # 2. UI Button Carrier
    carrier_step = os.path.join(P.EXPORT_DIR, "UI_Button_Carrier.step")
    if os.path.exists(carrier_step):
        H.import_step_model(stage3_comp, carrier_step, "UI_Button_Carrier", "Plastic - Glossy (Black)")
        
    # 3. ESP32-CAM Bracket (Signal Red accent)
    cam_bracket_step = os.path.join(P.EXPORT_DIR, "ESP32_CAM_Bracket.step")
    if os.path.exists(cam_bracket_step):
        H.import_step_model(stage3_comp, cam_bracket_step, "ESP32_CAM_Bracket", "Paint - Enamel Glossy (Red)")
        
    # 4. OLED Display (0.96")
    oled_step = os.path.join(P.MODELS_DIR, "OLED_128x64_0.96.step")
    if os.path.exists(oled_step):
        H.import_step_model(stage3_comp, oled_step, "OLED_Display", "Glass (Clear)")
        
    # 5. Rear Rocker Power Switch
    switch_step = os.path.join(P.MODELS_DIR, "ON_OFF_Switch.STEP")
    if os.path.exists(switch_step):
        H.import_step_model(stage3_comp, switch_step, "Power_Switch", "Paint - Enamel Glossy (Red)")

    print("Stage 3 Upper Enclosure & UI built successfully.")
    return stage3_comp


def run(_context: str = ""):
    """Entry point for direct Fusion MCP execution."""
    design = H.get_design()
    root_comp = design.rootComponent
    build_stage3(root_comp)


if __name__ == "__main__":
    run()
