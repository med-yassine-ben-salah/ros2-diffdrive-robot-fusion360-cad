# ==============================================================================
# Autodesk Fusion 360 - Stage 2: Electronics Deck, LiDAR & IMU
# Module: stage2_deck_lidar_imu.py
# Implements:
#   1. Middle structural electronics deck plate (Z = 61..65mm)
#   2. Four stepped LiDAR mounting pillars & clamp caps
#   3. LDS02RR 360° laser scanner & plate subassembly
#   4. MPU9250 9-DOF IMU at exact support-triangle centroid (X=55, Y=0mm)
#   5. Raspberry Pi & dual H-bridge motor driver mounting standoffs
# ==============================================================================

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parameters as P
import helpers as H


def build_stage2(root_comp):
    """Assembles all Stage 2 components under root_comp."""
    stage2_comp = H.create_component(root_comp, "Stage2_Deck_LiDAR_IMU")
    
    # 1. Electronics Deck
    deck_step = os.path.join(P.EXPORT_DIR, "Electronics_Deck.step")
    if os.path.exists(deck_step):
        H.import_step_model(stage2_comp, deck_step, "Electronics_Deck", "Plastic - Glossy (Black)")
        
    # 2. LiDAR Pillar Clamps (Signal Red accents)
    clamps_step = os.path.join(P.EXPORT_DIR, "LiDAR_Pillar_Clamps.step")
    if os.path.exists(clamps_step):
        H.import_step_model(stage2_comp, clamps_step, "LiDAR_Pillar_Clamps", "Paint - Enamel Glossy (Red)")
        
    # 3. LDS02RR LiDAR reference model
    lidar_step = os.path.join(P.MODELS_DIR, "lds02rr.step")
    if os.path.exists(lidar_step):
        H.import_step_model(stage2_comp, lidar_step, "LDS02RR_LiDAR", "Plastic - Glossy (Black)")
        
    # 4. MPU9250 IMU reference model
    imu_step = os.path.join(P.MODELS_DIR, "mpu9250_step.step")
    if os.path.exists(imu_step):
        H.import_step_model(stage2_comp, imu_step, "MPU9250_IMU", "Plastic - Glossy (Blue)")

    print("Stage 2 Electronics Deck, LiDAR & IMU built successfully.")
    return stage2_comp


def run(_context: str = ""):
    """Entry point for direct Fusion MCP execution."""
    design = H.get_design()
    root_comp = design.rootComponent
    build_stage2(root_comp)


if __name__ == "__main__":
    run()
