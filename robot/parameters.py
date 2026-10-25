# Phase 3 â€” Single-source parametric constants and derivation chains.
# No magic numbers in build scripts: every stage imports this module (and reloads it via importlib.reload).
# Coordinate system (ROS 2 mobile robot standard, origin on ground under motor/wheel axle midpoint):
#   X : forward (+X front, -X rear)
#   Y : left    (+Y left wheel side, -Y right wheel side)
#   Z : up      (Z = 0.0 is ground plane)

import math

MODELS_DIR  = r"C:\Users\yassine\Desktop\antigravity_ws_2\Fusion_ws\models"
PROJECT_DIR = r"C:\Users\yassine\Desktop\antigravity_ws_2\Fusion_ws\robot"
EXPORT_DIR  = PROJECT_DIR + r"\export"
PREVIEW_DIR = PROJECT_DIR + r"\previews"
MEASURE_DIR = PROJECT_DIR + r"\measure"
DOC_NAME    = "ROS2_DiffDrive_Robot"
FONT_PATH   = r"C:\Windows\Fonts\arialbd.ttf"

# ==============================================================================
# 1. PRINTER & FDM CLEARANCE PARAMETERS (Bambu Lab A1, PLA, 0.4 mm nozzle)
# ==============================================================================
BED_X = 256.0
BED_Y = 256.0
BED_Z = 256.0

NOZZLE_D          = 0.4
LAYER_H           = 0.2
CLEAR_TIGHT       = 0.15   # snug locating seat
CLEAR_MATING      = 0.25   # general mating clearance (brief: 0.2-0.4 mm)
CLEAR_SLIDE       = 0.30   # sliding battery door rail clearance per side
CLEAR_COVER       = 0.35   # removable upper shell clearance (brief: 0.3-0.5 mm)
CLEAR_LIDAR_NECK  = 1.80   # radial gap around rotating LiDAR head (widened by 1.0 mm radial / 2.0 mm diameter: Ø71.3 -> Ø73.3 mm)

# ==============================================================================
# 2. FASTENER PARAMETERS (M3 primary, M2 for OLED)
# ==============================================================================
M3_CLEAR_D        = 3.30   # M3 through-hole clearance (brief: 3.2-3.4 mm)
M3_PILOT_D        = 2.55   # M3 self-tapping pilot in PLA
M3_INSERT_D       = 4.00   # M3 heat-set insert bore (for 4.2-4.5 mm OD knurl)
M3_INSERT_DEPTH   = 5.50   # M3x4 or M3x5 heat-set insert pocket depth
M3_HEAD_D         = 5.80   # M3 socket head cap screw counterbore diameter
M3_HEAD_H         = 3.20   # M3 socket head height
M3_BOSS_OD        = 8.50   # standard M3 heat-set boss OD (>2x insert D)
M3_HEAVY_BOSS_OD  = 10.00  # heavy structural joint boss OD

M2_PILOT_D        = 1.70   # M2 self-tap pilot for OLED mount bosses
M2_BOSS_OD        = 4.80   # OLED standoff OD

# ==============================================================================
# 3. CHASSIS ENVELOPE & STRUCTURAL WALL PARAMETERS (Brief Â§2, Â§11, Â§14)
# ==============================================================================
CHASSIS_L         = 250.0  # exact overall X length (brief: 250 mm)
CHASSIS_W         = 150.0  # exact overall Y width  (brief: 150 mm)
MAX_NON_LIDAR_H   = 150.0  # ceiling for non-LiDAR structure (<150 mm)

# Rear-drive axle longitudinal position:
# Axle is at X = 0.0; rear wall at X_MIN = -55.0 (55 mm behind axle),
# front wall at X_MAX = +195.0 (195 mm ahead of axle).
REAR_OVERHANG     = 55.0   # CHOSEN: places axle 55 mm from rear bumper (rear 22% of 250 mm length)
X_AXLE            = 0.0    # datum origin X
Y_CENTER          = 0.0    # datum origin Y
X_MIN             = X_AXLE - REAR_OVERHANG          # -55.0 mm (DERIVED)
X_MAX             = X_MIN + CHASSIS_L               # +195.0 mm (DERIVED)
Y_MIN             = -CHASSIS_W / 2.0                # -75.0 mm (DERIVED)
Y_MAX             = +CHASSIS_W / 2.0                # +75.0 mm (DERIVED)

# Structural thicknesses (Brief Â§11):
BOTTOM_PLATE_T    = 4.0    # bottom chassis plate: 4 mm
WALL_T            = 3.0    # enclosure side/end walls: 2.5-3 mm -> 3.0 mm
DECK_T            = 4.0    # middle electronics deck plate: 3-4 mm -> 4.0 mm
TOP_COVER_T       = 3.5    # upper enclosure top roof thickness: 3-4 mm -> 3.5 mm
MOTOR_MOUNT_T     = 6.0    # motor mounting region / bridge thickness: 5-6 mm -> 6.0 mm
CASTER_MOUNT_T    = 6.0    # front caster mounting pad thickness: 5-6 mm -> 6.0 mm
RIB_T             = 2.5    # reinforcement ribs/gussets: 2-3 mm, preferably 2.5 mm

# Outer aesthetic radii & chamfers (Brief Â§11 "Form and character"):
CORNER_R          = 18.0   # chunky 45-deg industrial corner chamfer in XY plan (18 x 18 mm)
CORNER_CHAMFER    = 18.0   # 45-deg octagonal corner chamfer size
BED_CHAMFER       = 0.6    # elephant-foot / bed-edge chamfer
ROOF_CHAMFER_Y    = 6.0    # upper body side crown chamfer width
ROOF_CHAMFER_Z    = 6.0    # upper body side crown chamfer height

# ==============================================================================
# 4. VERTICAL (Z) ARCHITECTURE & DRIVETRAIN GEOMETRY (Measured + Derived)
# ==============================================================================
# Measured from JGA25-371_Wheel__65mm.STEP:
WHEEL_D           = 65.0
WHEEL_R           = WHEEL_D / 2.0                   # 32.50 mm
WHEEL_TIRE_W      = 25.98                           # x in [-12.99, +12.99] in wheel frame
WHEEL_HUB_PROTRUDE= 17.426                          # hub boss extends to -17.426 mm toward motor

# Axle height above ground Z=0:
Z_AXLE            = WHEEL_R                         # 32.50 mm (DERIVED: wheel touches Z=0)

# Ground clearance (Brief Â§3, Â§14; user choice: inverted bracket hanging from motor bridge):
GROUND_CLEARANCE  = 14.0                            # CHOSEN: 14.0 mm below bottom plate
Z_CHASSIS_BOT     = GROUND_CLEARANCE                # 14.00 mm (DERIVED)
Z_FLOOR_TOP       = Z_CHASSIS_BOT + BOTTOM_PLATE_T  # 18.00 mm (DERIVED)

# Measured from JGA25-371_Bracket.stl:
BRACKET_FACE_T    = 2.20                            # local y in [-2.2, 0.0]
BRACKET_BASE_T    = 2.00                            # local z in [-22.5, -20.5]
BRACKET_BASE_Z_OFF= 22.50                           # distance from motor bore axis to base outer face
BRACKET_W         = 32.00                           # local x in [-16, 16]
BRACKET_L         = 50.20                           # local y in [-2.2, 48.0]
BRACKET_HOLE_DX   = 12.50                           # 4 base holes at x = +-12.5
BRACKET_HOLE_Y1   = 5.00                            # first hole row from inner face
BRACKET_HOLE_Y2   = 43.00                           # second hole row from inner face

# Inverted bracket placement:
# Face outer surface touches inner side wall at |Y| = Y_MAX - WALL_T = 72.0 mm.
Y_INNER_WALL      = Y_MAX - WALL_T                  # 72.00 mm (DERIVED)
Y_BRACKET_INNER   = Y_INNER_WALL - BRACKET_FACE_T   # 69.80 mm (DERIVED: motor gearbox front face plane)
Z_BRACKET_BASE_BOT= Z_AXLE + (BRACKET_BASE_Z_OFF - BRACKET_BASE_T)  # 53.00 mm (DERIVED)
Z_BRACKET_BASE_TOP= Z_AXLE + BRACKET_BASE_Z_OFF     # 55.00 mm (DERIVED: bracket top touches motor bridge underside)

# Motor mounting bridge & Electronics Deck vertical station:
# Make the electronics deck underside at Z = 55.0 mm so the motor mounting bridge (Z = 55..61 mm, 6 mm thick)
# is integral with the lower chassis / deck structure!
Z_MOTOR_BRIDGE_BOT= Z_BRACKET_BASE_TOP              # 55.00 mm (DERIVED: butts against inverted bracket base)
Z_MOTOR_BRIDGE_TOP= Z_MOTOR_BRIDGE_BOT + MOTOR_MOUNT_T # 61.00 mm (DERIVED: 6 mm thick motor mount region)
Z_LOWER_TOP       = Z_MOTOR_BRIDGE_TOP              # 61.00 mm (top of lower chassis walls)
Z_DECK_BOT        = Z_LOWER_TOP                     # 61.00 mm (electronics deck bottom face butts on lower chassis)
Z_DECK_TOP        = Z_DECK_BOT + DECK_T             # 65.00 mm (electronics deck top surface)

# Measured from JGA25-371_with_encoder_ASM.STL:
MOTOR_LOCAL_AX_X  = -7.76
MOTOR_LOCAL_AX_Y  = 18.68
MOTOR_LOCAL_FACE_Z= 43.54
MOTOR_LEN         = 75.00                           # extends 63.50 mm inward from gearbox face, 11.50 mm shaft outward
# With gearbox face at |Y| = 69.80 mm:
#   - shaft tip reaches |Y| = 69.80 + 11.50 = 81.30 mm (6.30 mm outside outer wall Y=75.0)
#   - encoder rear reaches |Y| = 69.80 - 63.50 = 6.30 mm (leaves 12.60 mm center gap between L and R motors)
#   - With L motor spin = -150 deg and R motor spin = -30 deg around Y:
#     motor body + encoder stays within Z in [14.0, 46.4] and X in [-25.5, +15.5].
#     Notice at |Y| in [7.5, 20.0], X in [-17.0, -3.5], the encoder board dips to Z = 14.0..18.5 mm:
#     we provide a 2.5 mm deep encoder clearance pocket in the 4 mm floor (floor remains 2.0 mm thick locally,
#     or Z_FLOOR_TOP has a local pocket down to Z = 15.5 mm? Wait: if encoder ZMin is 14.00 mm and Z_CHASSIS_BOT
#     is 14.00 mm, a pocket to 13.5 mm would pierce the floor!
#     Waitâ€”let's check that! Why did encoder dip to Z = 14.0 mm in (-150/-30), whereas in (+30/+150) encoder
#     ZMin was 18.60 mm (0.6 mm ABOVE Z_FLOOR_TOP = 18.0 mm!) and ZMax was 51.0 mm (4.0 mm BELOW Z_MOTOR_BRIDGE_BOT = 55.0 mm!)?)
# BINGO! Look at check_transforms7.py:
#   In L deg=+30 and R deg=+150:
#     - Motor + encoder Z-range is [18.6, 51.0] mm!
#     - That is 0.6 mm ABOVE the flat 4 mm floor top (Z = 18.0 mm) AND 4.0 mm BELOW the motor bridge bottom (Z = 55.0 mm)!
#     - It touches NOTHINGâ€”neither the floor (Z=14..18) nor the bracket/bridge (Z=53..61), because the encoder is at
#       |Y| in [6.3, 21.8] mm, which is INBOARD of the bracket base (|Y| in [21.8, 72.0] mm)!
MOTOR_L_SPIN_DEG  = 30.0                            # DERIVED: keeps Z in [18.6, 51.0], clear of floor (18.0) & bridge (55.0)
MOTOR_R_SPIN_DEG  = 150.0                           # DERIVED: keeps Z in [18.6, 51.0], clear of floor (18.0) & bridge (55.0)

# Wheel placement & wall opening (Brief Â§3 "Wheel-to-wall clearance"):
# Wheel center at Y = +-90.50 mm -> wheel inner tire face at 90.50 - 13.0 = 77.50 mm (2.5 mm clear of outer wall Y=75.0),
# hub boss tip at 90.50 - 17.426 = 73.074 mm (1.074 mm healthy clearance from bracket face at 72.0 mm, engages shaft tip at 81.3 mm by 8.23 mm!).
WHEEL_Y_OFFSET    = 90.50                           # CHOSEN: 2.5 mm tire clearance outside Y=75 wall; 1.074 mm clear of bracket face
WHEEL_TRACK       = 2.0 * WHEEL_Y_OFFSET            # 181.00 mm (DERIVED center-to-center wheel track)
# Side-wall opening around axle (X=0, Z=32.5) must clear the wheel mounting hub (OD 13.2 mm -> r=6.6 mm) plus M3 motor screws (r=10.2 mm):
WHEEL_HUB_HOLE_R  = 11.00                           # Ã˜22.0 mm opening in side wall clears Ã˜13.2 mm wheel hub + motor screws

# ==============================================================================
# 5. UPPER ENCLOSURE & BURIED LiDAR PARAMETERS (Brief Â§4)
# ==============================================================================
# Measured from lds02rr.step and LDS02RR_Plate.stl:
LIDAR_HEAD_R      = 34.85                           # lower collar r=34.85 (z in [-7.3, 1.5]), upper r=34.35 (z in [1.5, 18.5])
LIDAR_NECK_CUT_R  = LIDAR_HEAD_R + CLEAR_LIDAR_NECK # 36.65 mm (Ø73.3 mm circular opening around rotating turret)
LIDAR_PLATE_Z_LOCAL_BOT = 88.60
LIDAR_PLATE_Z_LOCAL_TOP = 92.60
# In untransformed LDS02RR_Plate.stl, the 4 mounting posts have their locating pin tips at Z = 109.20 mm
# and counterbore mating steps at Z = 107.70 mm.
# In untransformed lds02rr.step, the 4 mounting ears have their counterbore shoulder at Z = -11.50 mm
# and top face / through-hole top at Z = -10.00 mm.
# When the plate's locating pins enter the mounting holes of the laser scanner:
#   Z_plate_pin_tip (109.20) aligns with Z_lidar_ear_top (-10.00):
#   LIDAR_IN_PLATE_Z = 109.20 - (-10.00) = 119.20 mm (and 107.70 - (-11.50) = 119.20 mm).
LIDAR_IN_PLATE_Z  = 119.20                          # LiDAR origin Z in plate frame (locating pins at z=109.2 enter mounting holes to z=-10.0)

# Upper enclosure roof top surface Z_ROOF_TOP meets the rotating head at its base (LiDAR local z = +1.50 mm):
# Look at lds02rr.step:
#   - Stationary base body is z_local in [-21.1, 0.0] (r = 38.0 around turret, teardrop nose out to x = -69.65).
#   - Lower turret transition collar is z_local in [-7.3, +1.50] (r = 34.85).
#   - Upper rotating laser head is z_local in [+1.50, +18.50] (r = 34.35).
# Placing LiDAR origin (z_local = 0.0) at Z_LIDAR_ORIGIN = Z_ROOF_BOT - 0.50 = 108.00 mm puts:
#   - The entire stationary base & teardrop nose (z_local <= 0.0) at Z <= 108.00 mm (0.50 mm BELOW roof underside Z_ROOF_BOT = 108.50 mm â€” 100% hidden inside the enclosure!)
#   - The turret collar (z_local in [-7.3, +1.50], r = 34.85) inside the circular roof opening (Z in [108.5, 112.0], R = 35.65)!
#   - The rotating head (z_local in [+1.50, +18.50]) emerging right through Z_ROOF_TOP = 112.00 mm up to Z = 126.50 mm!
Z_ROOF_TOP        = 112.0                           # CHOSEN: 112.0 mm (< 150 mm max non-LiDAR height; leaves 47 mm upper bay)
Z_ROOF_BOT        = Z_ROOF_TOP - TOP_COVER_T        # 108.50 mm (DERIVED)
Z_LIDAR_ORIGIN    = Z_ROOF_BOT - 0.50               # 108.00 mm (DERIVED: stationary base z_local<=0 sits 0.5 mm below roof underside!)
# Therefore:
#   - LiDAR rotating head top is at Z = 108.0 + 18.5 = 126.50 mm (stands 14.5 mm proud of roof, 100% unobstructed)
#   - LiDAR stationary body & motor (z_local in [-35.6, 0.0]) sit at Z in [72.40, 108.00] mm (100% hidden inside!)
#   - LDS02RR_Plate shift in Z: Z_PLATE_SHIFT = Z_LIDAR_ORIGIN - LIDAR_IN_PLATE_Z = 108.0 - 119.20 = -11.20 mm
Z_PLATE_SHIFT     = Z_LIDAR_ORIGIN - LIDAR_IN_PLATE_Z             # -11.20 mm (DERIVED: plate locating pins fully engaged in LiDAR holes)
Z_LIDAR_PLATE_BOT = LIDAR_PLATE_Z_LOCAL_BOT + Z_PLATE_SHIFT       # 77.40 mm (DERIVED: 12.40 mm above deck top Z=65.0)
Z_LIDAR_PLATE_TOP = LIDAR_PLATE_Z_LOCAL_TOP + Z_PLATE_SHIFT       # 81.40 mm (DERIVED)
LIDAR_PILLAR_H    = Z_LIDAR_PLATE_BOT - Z_DECK_TOP                # 12.40 mm (DERIVED pillar height from deck top to plate bottom)

# Orientation of Plate + LiDAR in robot XY so the tail overhangs +X (forward, where chassis has 195 mm)
# rather than -X (rear, where chassis only has 55 mm):
# In plate local frame, the plate spans x in [-32.8, 32.8], y in [-72.85, +27.80] (tail is at -Y_plate).
# Rotating Plate by -90 deg about Z maps (x_p, y_p) -> (y_p, -x_p) Wait: (-90 deg: x' = y, y' = -x -> y_p=-72.85 maps to x'=-72.85!).
# Rotating Plate by +90 deg about Z maps (x_p, y_p) -> (-y_p, x_p), so y_p in [-72.85, +27.80] maps to X_world in [-27.80, +72.85]!
# Let's check: with Plate rotated +90 deg about Z:
#   - Plate spans X_world in [-27.80, +72.85] mm (well inside X in [-55, +195]!)
#   - Plate spans Y_world in [-32.80, +32.80] mm (symmetric, well inside Y in [-72, +72]!)
#   - And since LiDAR is rotated -90 deg relative to Plate, (+90 deg) + (-90 deg) = 0 deg net rotation for `lds02rr.step`!
#     Wait: in `lds02rr.step` (0 deg rotation), the drive motor is at x_local = -52.85 -> after Plate(+90) + LiDAR_rel(-90) = 0 deg,
#     Wait: in `census.py` we found Plate holes at:
#       (-33.56, 24.50), (38.65, 20.50), (-27.18, -47.00), (28.51, -44.00)
#     and LiDAR bosses at:
#       (24.50, 33.56), (20.50, -38.65), (-47.00, 27.18), (-28.51, -44.00 -> wait: (-44.00, -28.51)).
#     Mapping LiDAR (x_L, y_L) -> Plate (-y_L, +x_L) (+90 deg around Z!) sends:
#       (24.50, 33.56)  -> (-33.56, 24.50)
#       (20.50, -38.65) -> (+38.65, 20.50)
#       (-47.00, 27.18) -> (-27.18, -47.00)
#       (-44.00, -28.51)-> (+28.51, -44.00)!
#     Aha! LiDAR -> Plate is +90 deg about Z! And when Plate -> World is ALSO +90 deg about Z,
#     then LiDAR -> World is +180 deg about Z: (x_L, y_L) -> (-x_L, -y_L), which puts the LiDAR drive motor
#     (x_L = -52.85) at X_world = +52.85 mm (into the spacious +X front half of the robot)!
LIDAR_PLATE_ROT_Z = 90.0                            # DERIVED: places plate tail toward +X (X in [-27.80, +72.85], Y in [-32.80, +32.80])
LIDAR_BODY_ROT_Z  = 180.0                           # DERIVED: (+90 rel to plate) + (+90 plate) = 180 deg in world

# ==============================================================================
# 6. FRONT BALL CASTER & SUPPORT TRIANGLE / IMU CENTROID (Brief Â§3, Â§5, Â§14)
# ==============================================================================
CASTER_BALL_D     = 15.875                          # 5/8 inch steel ball (user choice)
CASTER_BALL_R     = CASTER_BALL_D / 2.0             # 7.9375 mm
CASTER_CLEAR      = 0.30                            # socket radial clearance around ball (FDM printable free-rolling fit)
CASTER_X          = 165.0                           # CHOSEN: 30 mm behind front bumper (X_MAX = 195.0), on centerline Y=0
CASTER_Y          = 0.0                             # exact centerline
# Ball center Z so bottom of ball touches ground Z = 0.0:
Z_CASTER_BALL     = CASTER_BALL_R                   # 7.9375 mm (DERIVED: ball bottom at Z = 0.0, level with wheels)
CASTER_FLANGE_OD  = 38.0                            # mounting flange OD (bolts from underneath into 6 mm floor pad)
CASTER_BODY_OD    = 24.0                            # cylindrical socket housing OD
CASTER_BOLT_R     = 14.0                            # 3 x M3 mounting screws on R=14 mm bolt circle
CASTER_CUP_BOT_Z  = 6.20                            # CHOSEN: raises real ground clearance from 3.0 mm to 6.20 mm (Issue 08)

# Support triangle contact points (Left wheel, Right wheel, Front caster):
#   P_L = (X_AXLE, +WHEEL_Y_OFFSET, 0) = (0.0, +88.5, 0.0)
#   P_R = (X_AXLE, -WHEEL_Y_OFFSET, 0) = (0.0, -88.5, 0.0)
#   P_C = (CASTER_X, 0.0, 0.0)         = (165.0, 0.0, 0.0)
IMU_CENTROID_X    = (2.0 * X_AXLE + CASTER_X) / 3.0 # 55.00 mm (DERIVED exact support-triangle centroid X)
IMU_CENTROID_Y    = 0.0                             # 0.00 mm  (DERIVED exact support-triangle centroid Y)
# Check vertical clearance at (X = 55.0, Y = 0.0) on the electronics deck (Z_DECK_TOP = 65.0):
#   - The LiDAR plate bottom is at Z = 77.80 mm (12.80 mm above Z_DECK_TOP = 65.0 mm).
#   - MPU9250 mounted on 4.0 mm standoffs above Z_DECK_TOP = 65.0 mm has PCB at Z in [69.0, 70.64] mm
#     and top SMD components at Z = 72.52 mm â€” which is 5.28 mm BELOW the LiDAR plate bottom (77.80 mm)!
#   - And its through-hole pins extend 8.2 mm below the PCB (to Z = 69.0 - 8.2 = 60.8 mm) into a clearance
#     slot in the deck!
#   - Therefore, the MPU9250 sits at the EXACT support-triangle centroid (55.0, 0.0) with zero interference!
IMU_X             = IMU_CENTROID_X                  # 55.00 mm (EXACT centroid â€” no offset needed!)
IMU_Y             = IMU_CENTROID_Y                  # 0.00 mm
IMU_BOSS_H        = 2.50                            # 2.5 mm standoffs on deck top -> PCB top at 69.14 mm, ZMax at 71.02 mm (< 73.80 mm plate!)
Z_IMU_PCB_TOP     = Z_DECK_TOP + IMU_BOSS_H + 1.64  # 69.14 mm (DERIVED)

# ==============================================================================
# 7. BATTERY COMPARTMENT, SLIDING DOOR & THUMB HOLE (Brief Â§6)
# ==============================================================================
# Measured from 3x_Battery_Holder_With_Batteries.step:
BATT_HOLDER_L     = 77.98                           # along cells (local X)
BATT_HOLDER_W     = 59.63                           # across 3 cells (local Y in [56.185, 115.815], center 86.0)
BATT_HOLDER_H     = 21.54                           # tray height above tray bottom z=0
BATT_TAB_DROP     = 3.20                            # solder tabs hang to z = -3.20 at cell ends (|local X| in [30.89, 37.48])

# Placement: low in the lower chassis, close to the motor axle, cells parallel to Y (axle) so the holder
# slides straight out through the RIGHT (-Y) side wall!
# Wait: let's check both orientations of the battery holder (77.98 x 59.63 mm):
#   Option A: 77.98 mm along Y (parallel to axle), 59.63 mm along X:
#     - Center at X_BATT = 75.0 mm ( spans X in [45.185, 104.815], clear of motors X <= 25.5 and caster X >= 143)
#     - Centered on Y = 0 (spans Y in [-38.99, +38.99], well inside walls at Y = +-72.0)
#     - Slides out sideways along -Y through a 62 mm wide x 26 mm tall opening in the right (-Y) side wall!
#     - Why is Option A (77.98 along Y, 59.63 along X) so clean?
#       Because the side-wall opening in X only needs to be 59.63 + 2.4 = 62.0 mm wide (X in [44.0, 106.0]),
#       leaving solid lower side wall over the motors (X in [-55, 40]) AND toward the front (X in [110, 195])!
BATT_X            = 75.0                            # CHOSEN: just forward of motors, low in lower chassis
BATT_Y            = 0.0                             # centered left-to-right
BATT_TRAY_Z_BOT   = Z_FLOOR_TOP + 3.5               # 21.50 mm (raised 3.5 mm on tray rails so -3.2 mm solder tabs clear floor!)
BATT_LIP_H        = 1.00                            # 1.0 mm sill stop lip retention; lifted +1.4 mm via thumb hole to slide out
# Vertical room in lower bay: Z_LOWER_TOP = 61.0 mm.
# Holder top is at 21.50 + 21.54 = 43.04 mm. When lifted +4.0 mm to clear the 3.0 mm retaining lip,
# holder top is at 47.04 mm â€” leaving 14.0 mm of vertical clearance below the deck (61.0 mm)!
BATT_BAY_X_MIN    = BATT_X - BATT_HOLDER_W / 2.0 - 1.2  # 43.985 mm
BATT_BAY_X_MAX    = BATT_X + BATT_HOLDER_W / 2.0 + 1.2  # 106.015 mm
BATT_DOOR_X_PIVOT = 107.0                           # vertical pivot hinge axis X
BATT_DOOR_Y_PIVOT = -73.5                           # vertical pivot hinge axis Y (tangent to Y=-75.0 and Y=-72.0)
BATT_DOOR_X_LATCH = 44.8                            # cantilever snap latch hook X
BATT_DOOR_PIN_R   = 1.5                             # Ã˜3.0 mm pivot trunnion pin radius (fits flush in 3.0 mm wall)
BATT_DOOR_SOCKET_R = 1.75                           # Ã˜3.5 mm pivot socket bore (0.25 mm radial clearance, eliminates slop)
BATT_DOOR_SNAP_ENTRY_W = 2.70                       # 2.7 mm constriction for positive snap retention of Ã˜3.0 mm pin
BATT_LATCH_HOOK_UNDERCUT = 1.40                     # 1.4 mm positive undercut hook engagement behind chassis jamb
BATT_HOLDDOWN_Z_BOT = 45.00                         # underside of hold-down rails
BATT_HOLDDOWN_T   = 2.00                            # rail thickness
BATT_HOLDDOWN_OVERHANG = 1.50                       # how far rails overhang the holder edge in X
BATT_DOOR_THICK   = WALL_T                          # 3.0 mm flush with outer wall Y = -75.0 mm
BATT_THUMB_D      = 24.0                            # Ã˜24.0 mm thumb hole through bottom floor at (BATT_X, BATT_Y)

# ==============================================================================
# 8. TOP UI PANEL: REAR-FACING OLED, 4 BUTTONS, RGB LED, BUZZER GRILLE (Brief Â§7, Â§8)
# ==============================================================================
# Placed on the upper enclosure top surface (Z_ROOF_TOP = 112.0 mm), forward of the LiDAR turret
# (LiDAR turret is at X in [-35.65, +35.65]; LiDAR plate extends to X = +72.85 at Z <= 81.8).
# Upper roof forward of X = +45.0 to +185.0 is completely free at Z = 108.5..112.0 mm!
UI_X_CENTER       = 125.0                           # CHOSEN: centered on forward upper deck roof
OLED_X            = 94.0                            # OLED screen center X (spans X in [80, 108], clears LiDAR plate X<=72.8 & buttons X>=113)
OLED_Y            = 0.0                             # centered on Y=0; screen faces rearward (-X) for operator standing behind robot
OLED_WIN_W        = 24.0                            # Y width of screen opening (clears 21.56 mm active area, hides 26.7 mm PCB)
OLED_WIN_L        = 13.0                            # X length of screen opening (clears 11.22 mm active area, hides 27.86 mm PCB & header)

# 4 Tactile switches + caps in diamond layout (UP, DOWN, LEFT=RETURN, RIGHT=ENTER):
BTN_CENTER_X      = 140.0                           # center of 4-button diamond (spans X in [113, 167], clears OLED X<=108 & Camera X>=171.4!)
BTN_CENTER_Y      = 0.0
BTN_PITCH_R       = 19.0                            # radius from diamond center to each button center (38 mm span)
BTN_CAP_HOLE_D    = 12.40                           # Ã˜12.40 mm panel hole: clears Ã˜11.5 mm cap barrel, retains Ã˜13.86 mm cap skirt!
# Switch body seat Z so cap skirt top (switch z = 8.14 mm) sits 0.6 mm below Z_ROOF_BOT (108.5 mm),
# and cap top (switch z = 12.20 mm) protrudes +1.5 mm proud of Z_ROOF_TOP (112.0 mm):
Z_SW_SEAT         = Z_ROOF_BOT - 8.30               # 100.20 mm (DERIVED: cap skirt top at 108.34 < 108.50; cap top at 112.40 mm!)

# RGB LED & Buzzer adjacent to OLED (at X = OLED_X = 94.0 mm, on the +Y / left side of OLED):
LED_X             = OLED_X
LED_Y             = 26.0                            # next to OLED (OLED PCB ends at Y = +13.35)
LED_HOLE_D        = 5.30                            # Ã˜5.30 mm hole for Ã˜5.0 mm LED dome; Ã˜5.9 mm flange retained below roof

BUZZER_X          = OLED_X
BUZZER_Y          = 44.0                            # next to RGB LED (18 mm center-to-center)
BUZZER_GRILLE_R   = 1.10                            # Ã˜2.2 mm acoustic grille holes (7-hole hex pattern: 1 center + 6 on R=3.6 mm)
BUZZER_GRILLE_RING= 3.60

# ==============================================================================
# 9. FRONT ESP32-CAM & REAR ON/OFF SWITCH (Brief Â§9, Â§10)
# ==============================================================================
# ESP32-CAM at center of front wall (X = X_MAX = 195.0 mm, Y = 0.0 mm):
CAM_X_LENS        = X_MAX - 0.5                     # 194.50 mm: lens glass 0.5 mm recessed inside front wall face
CAM_Y             = 0.0                             # exact centerline
CAM_Z_LENS        = 98.5                            # in upper front wall: stack Z in [66.4, 106.5] fits 100% inside upper bay [65.0, 108.5]!
CAM_WIN_D         = 10.0                            # Ã˜10.0 mm lens window through front wall (clears Ã˜8.0 mm lens barrel)

# ON/OFF Switch on rear-facing back side (X = X_MIN = -55.0 mm):
# Recessed by 7.5 mm into protective bumper well so rocker tip (-54.45 mm) stays behind X_MIN bumper plane:
SW_POWER_RECESS   = 7.50                            # recess depth behind rear bumper plane
SW_POWER_X        = X_MIN + SW_POWER_RECESS         # -47.50 mm (mounting bezel face)
SW_POWER_Y        = 0.0                             # centered on rear wall!
SW_POWER_Z        = 76.0                            # Z in [68.6, 83.4]: below LiDAR rear cylinder bottom (Z = 86.9) and above deck (Z = 65.0)!
SW_CUTOUT_W       = 19.8                            # Y width of rectangular cutout for switch body (19.8 x 12.8 mm)
SW_CUTOUT_H       = 12.8                            # Z height of rectangular cutout

# ==============================================================================
# 10. MAIN STRUCTURAL JOINTS (Brief Â§12 â€” Lower Chassis <-> Deck <-> Upper Shell)
# ==============================================================================
# 6 x M3 heat-set insert bosses at the perimeter corners/mid-walls joining Lower Chassis and Deck:
JOINT_XY = [
    (-38.0, +60.0), (-38.0, -60.0),   # rear pair (inboard of 18x18 mm 45-deg corner chamfer)
    (+36.0, +64.0), (+36.0, -64.0),   # mid-rear pair (clears motor X<=12.5 at Y=64 AND battery bay X>=44)
    (+176.0, +60.0), (+176.0, -60.0), # front pair (inboard of 18x18 mm 45-deg corner chamfer)
]
UPPER_JOINT_XY = [
    (-42.0, +48.0), (-42.0, -48.0),   # rear upper-shell screw wells
    (+164.0, +52.0), (+164.0, -52.0), # front upper-shell screw wells
]

# ==============================================================================
# 11. EMBEDDED COMPUTING & MOTOR DRIVER MOUNTING (Brief Â§15 / Review Issues 04 & 05)
# ==============================================================================
# Raspberry Pi 4 / 5 standard 58 x 49 mm mounting pattern on Electronics_Deck:
SBC_HOLE_DX       = 58.00                           # along X
SBC_HOLE_DY       = 49.00                           # along Y
SBC_CENTER_X      = 135.00                          # centered forward of LiDAR, below UI carrier
SBC_CENTER_Y      = 0.00
SBC_BOSS_H        = 4.00                            # boss height on deck top (Z in [65.0, 69.0])
SBC_BOSS_OD       = 6.20
SBC_PILOT_D       = 2.10                            # for M2.5 screws

# Dual H-Bridge Motor Driver (Cytron MDD10A / TB6612 module) mounting pattern:
# Relocated to +X, +Y free deck area (Issue 05 fix)
DRIVER_HOLE_DX    = 45.00                           # along X
DRIVER_HOLE_DY    = 35.00                           # along Y
DRIVER_CENTER_X   = 92.00
DRIVER_CENTER_Y   = 48.00
DRIVER_BOSS_H     = 4.00
DRIVER_BOSS_OD    = 7.00
DRIVER_PILOT_D    = 2.50                            # for M3 screws


