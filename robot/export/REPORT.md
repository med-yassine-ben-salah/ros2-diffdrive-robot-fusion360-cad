# Engineering Design & Verification Report — ROS 2 Differential-Drive Robot

- **FreeCAD Document**: `C:\Users\yassine\Desktop\antigravity_ws_2\FreeCAD_ws\robot\ROS2_DiffDrive_Robot.FCStd` (also copied to `export/ROS2_DiffDrive_Robot.FCStd`)
- **Full Assembly STEP**: `C:\Users\yassine\Desktop\antigravity_ws_2\FreeCAD_ws\robot\export\ROS2_DiffDrive_Robot_Assembly.step`
- **Consolidated Verification Status**: **`26 / 26` Brief Requirements Passed (`+1` Meta Parity Check)**

---

## 1. Headline Dimensions & Parametric Derivation Chain

All geometry is driven from a single source of truth (`parameters.py`), with zero magic numbers in the build stages (`stage1_chassis_drivetrain.py`, `stage2_deck_lidar_imu.py`, `stage3_upper_enclosure_ui.py`).

### 1.1 Coordinate System Convention (ROS 2 Standard, REP-103)
- **Origin `(0, 0, 0)`**: Projected on the ground plane (`Z = 0`) directly beneath the midpoint of the rear drive-wheel axle.
- **`+X`**: Forward (toward front ball caster and `ESP32-CAM`).
- **`+Y`**: Left (toward left drive wheel).
- **`+Z`**: Upward (perpendicular to ground plane `Z = 0`).

### 1.2 Chosen vs. Derived Parameters

| Parameter | Value | Type | Derivation / Justification |
|---|---:|---|---|
| `CHASSIS_L × CHASSIS_W` | `250.0 × 150.0 mm` | **Brief (Fixed)** | Exact enclosure footprint (`X ∈ [-55.0, +195.0] mm`, `Y ∈ [-75.0, +75.0] mm`); fits inside `256 × 256 × 256 mm` Bambu Lab A1 build volume. |
| `WHEEL_R` (`Z_AXLE`) | `32.50 mm` | **Measured + Derived** | Measured from `65mm_Wheel.step` (`OD = 64.928 mm`, width `26.588 mm`). Sets rear axle height `Z_AXLE = 32.50 mm` for coplanar ground contact at `Z = 0.00 mm`. |
| `X_AXLE` | `0.00 mm` | **Chosen** | Rear axle placed `55.0 mm` forward of the rear bumper (`X_MIN = -55.0 mm`), giving `22.5 mm` rear body overhang behind the `Ø65 mm` tire (`X_tire_min = -32.46 mm`). |
| `CASTER_X, CASTER_Y` | `(165.00, 0.00) mm` | **Chosen** | Front ball caster on `Y = 0` centerline, `30.0 mm` inside front bumper (`X_MAX = +195.0 mm`), creating a `165.0 mm` wheelbase triangle with the rear axle. |
| `IMU_X, IMU_Y` | `(55.00, 0.00) mm` | **Derived** | Exact centroid of the 3-point support triangle formed by Left Wheel `(0, +82.25)`, Right Wheel `(0, -82.25)`, and Front Caster `(165.0, 0)`: `X = (0 + 0 + 165.0)/3 = 55.00 mm`, `Y = 0.00 mm`. |
| `GROUND_CLEARANCE` (`Z_CHASSIS_BOT`) | `14.00 mm` | **Derived** | Achieved by mounting the supplied `JGA25-371_Bracket.stl` brackets **inverted** (hanging downward from an internal `6.0 mm` structural motor bridge at `Z ∈ [55.0, 61.0] mm`), placing the motor/encoder vertices in `Z ∈ [18.59, 50.99] mm` (`0.59 mm` above the `Z = 18.00 mm` floor top). |
| `BOTTOM_PLATE_T` | `4.00 mm` | **Brief (`4 mm`)** | Floor spans `Z ∈ [14.00, 18.00] mm`. |
| `WALL_T` | `3.00 mm` | **Brief (`2.5–3 mm`)** | Perimeter walls of `Lower_Chassis` and `Upper_Enclosure`. |
| `MOTOR_MOUNT_T` / `CASTER_MOUNT_T` | `6.00 mm` | **Brief (`5–6 mm`)** | Internal structural motor bridge (`Z ∈ [55.0, 61.0] mm`) and reinforced front caster boss pad (`Z ∈ [14.0, 20.0] mm`). |
| `DECK_T` | `4.00 mm` | **Brief (`3–4 mm`)** | `Electronics_Deck` plate spans `Z ∈ [61.00, 65.00] mm`. |
| `TOP_COVER_T` | `3.50 mm` | **Brief (`3–4 mm`)** | `Upper_Enclosure` roof spans `Z ∈ [108.50, 112.00] mm`. |
| `Z_LIDAR_ORIGIN` | `108.00 mm` | **Derived** | `LDS02RR` base datum placed `0.50 mm` below `Z_ROOF_BOT = 108.50 mm`. Stationary body (`z_local ∈ [-21.1, 0.0]`) is `100%` hidden inside the enclosure (`Z ∈ [86.9, 108.0] mm`), while the `Ø69.7 mm` rotating turret head protrudes to `Z = 126.50 mm` (`14.5 mm` above the `112.00 mm` roof) through a `Ø71.30 mm` circular opening. |
| `Z_LIDAR_PLATE_BOT` | `77.80 mm` | **Derived** | `LDS02RR_Plate.stl` (`4.00 mm` base thickness) sits on `4×` stepped deck pillars at `Z ∈ [77.80, 81.80] mm`, supporting the LiDAR's 4 mounting feet at `Z = 86.90 mm` (`9.10 mm` above the plate base) while clearing `MPU9250_IMU` (`ZMax = 71.02 mm`) by `6.78 mm`. |
| `Z_ROOF_TOP` | `112.00 mm` | **Derived** | Non-LiDAR enclosure height is `112.00 mm` (`112.40 mm` to top of tactile switch caps), well below the `< 150.0 mm` requirement. Total height with LiDAR turret is `126.50 mm`. |

---

## 2. Complete Bill of Materials (BOM)

### 2.1 Local Reference CAD Components (`14 / 14` Used)

| # | Local CAD Filename | Format | FreeCAD Object Name | FreeCAD Group | Measured Envelope (`mm`) | Placement / Role |
|---:|---|---|---|---|---|---|
| 1 | `JGA25-371.stl` | STL (`mm`) | `Left_Drive_Motor`, `Right_Drive_Motor` | `Grp_Left_Motor_Assembly`, `Grp_Right_Motor_Assembly` | `Ø26.5 × 79.33` | Rear axle `X = 0.0, Z = 32.5 mm`, `Y = ±69.0 mm`, spun `30°`/`150°` to align gearbox M3 holes with inverted brackets. |
| 2 | `JGA25-371_Bracket.stl` | STL → B-rep (`bracket_solid.brep`) | `Left_Motor_Bracket`, `Right_Motor_Bracket` | `Grp_Left_Motor_Assembly`, `Grp_Right_Motor_Assembly` | `31.0 × 50.25 × 28.0` | Mounted inverted under internal `6.0 mm` motor bridge (`Z = 55.0 mm`), `Y_face = ±69.0 mm`. |
| 3 | `65mm_Wheel.step` | STEP (`1` solid) | `Left_Drive_Wheel`, `Right_Drive_Wheel` | `Grp_Wheels` | `Ø64.93 × 26.59` | Collinear on `X = 0.0, Z = 32.5 mm`, centered at `Y = ±91.3 mm` (`3.0 mm` tire clearance outside `Y = ±75.0 mm` walls). |
| 4 | `lds02rr.step` | STEP (`5` solids) | `LDS02RR_LiDAR` | `Grp_LiDAR_Mount` | `102.79 × 76.59 × 39.60` | Turret center at `(0.00, 0.00)`, datum `Z = 108.00 mm`; stationary body buried inside, rotating head at `Z ∈ [112.0, 126.5] mm`. |
| 5 | `LDS02RR_Plate.stl` | STL (`mm`) | `LDS02RR_Mount_Plate` | `Grp_LiDAR_Mount` | `100.65 × 65.60 × 20.60` | Unmodified adapter plate seated on `4×` stepped deck pillars at `Z ∈ [73.80, 94.40] mm`, retained by `4×` M3 clamp caps. |
| 6 | `MPU9250.STEP` | STEP (`1` solid) | `MPU9250_IMU` | `Grp_MPU9250` | `25.91 × 15.65 × 10.22` | Bolted horizontally at exact support-triangle centroid `(55.00, 0.00, 69.00) mm`, quaternion `(0, 0, 0, 1)` (`+X` fwd, `+Y` left, `+Z` up). |
| 7 | `3x18650_Battery_Holder.STEP` | STEP (`1` solid) | `Battery_Holder_3x18650` | `Grp_Battery_Compartment` | `59.63 × 77.98 × 21.31` | Seated on low-CG tray rails (`X = 75.0, Y = 0.0, Z = 21.5 mm`) over `Ø24 mm` floor thumb hole; retained by `3.0 mm` lip + hinged snap-latch door. |
| 8 | `OLED_128x64_0.96.step` | STEP (`1` solid) | `OLED_Display_096` | `Grp_OLED_UI_Panel` | `26.70 × 27.86 × 3.80` | Mounted in a `1.50 mm` recessed underside bezel pocket at `(94.0, 0.0, 109.65) mm`, rotated `-90°` so screen faces rearward (`-X`) through a `13 × 24 mm` bezel window (`2.0 mm` top web). |
| 9 | `Tactal_Switch_THRU(12mmx12mmx8mm)_Blue.stp` | STEP (`1` solid) | `Button_Switch_UP/DOWN/RETURN/ENTER` | `Grp_OLED_UI_Panel` | `13.40 × 12.00 × 11.42` | `4×` switches seated in `UI_Button_Carrier` at `Z = 100.20 mm` in diamond layout around `(140.0, 0.0) mm` (`R = 19.0 mm`). |
| 10 | `switch_cap_black.stp` | STEP (`1` solid) | `Button_Cap_UP/DOWN/RETURN/ENTER` | `Grp_OLED_UI_Panel` | `Ø12.75 × 8.20` | `4×` caps seated on switches; `Ø11.82 mm` crowns protrude through `Ø12.40 mm` roof holes to `Z = 112.40 mm` (`0.40 mm` proud). |
| 11 | `5mm_LED_RGB.stp` | STEP (`1` solid) | `RGB_Status_LED` | `Grp_RGB_LED` | `Ø5.90 × 16.10` (trimmed leads) | Seated in roof underside collar at `(94.0, 26.0, 104.75) mm`; `Ø5.0 mm` dome emerges through `Ø5.3 mm` bore to `Z = 112.35 mm` (`8.5 mm` soldered leads below flange). |
| 12 | `Passive_Buzzer.step` | STEP (`1` solid) | `Acoustic_Buzzer` | `Grp_Buzzer` | `Ø12.88 × 14.00` | Cradled in roof underside retaining ring at `(94.0, 44.0) mm` (`0.20 mm` below `7× Ø2.2 mm` hexagonal acoustic grille). |
| 13 | `esp32cam_with_MB.stl` | STL (`m` → `×1000 mm`) | `ESP32_CAM_Module` | `Grp_ESP32_CAM` | `23.05 × 29.10 × 40.06` | Held by custom `ESP32_CAM_Bracket` inside front wall; lens centered at `(194.50, 0.00, 98.50) mm` behind `Ø10.0 mm` window. |
| 14 | `ON_OFF_Switch.STEP` | STEP (`1` solid) | `Rear_Power_Switch` | `Grp_Power_Switch` | `20.95 × 14.95 × 24.49` | Snap-fit in `19.8 × 12.8 mm` cutout on rear wall (`X = -55.0, Y = 0.0, Z = 76.0 mm`); rocker faces rearward (`-X` to `-61.95 mm`). |

---

### 2.2 Custom 3D-Printable Structural Parts (`8` Parts)

| # | FreeCAD Object | Group | Exported STL / STEP | B-Rep Volume (`mm³`) | Facets | Watertight (`isSolid`) | Bed Bounding Box (`mm`) | Est. PLA (`g`) |
|---:|---|---|---|---:|---:|:---:|---:|---:|
| 1 | `Lower_Chassis` | `Grp_Main_Chassis` | `Lower_Chassis.stl` / `.step` | `329,961.6` | `5,036` | `True` | `250.0 × 150.0 × 47.0` | `171.8` |
| 2 | `Electronics_Deck` | `Grp_Electronics_Deck` | `Electronics_Deck.stl` / `.step` | `154,694.2` | `4,400` | `True` | `250.0 × 150.0 × 16.8` | `80.6` |
| 3 | `Upper_Enclosure` | `Grp_Main_Chassis` | `Upper_Enclosure.stl` / `.step` | `222,808.4` | `10,240` | `True` | `250.0 × 150.0 × 47.0` | `116.0` |
| 4 | `UI_Button_Carrier` | `Grp_OLED_UI_Panel` | `UI_Button_Carrier.stl` / `.step` | `8,182.7` | `1,044` | `True` | `52.0 × 52.0 × 4.15` | `4.3` |
| 5 | `Battery_Door` | `Grp_Battery_Compartment` | `Battery_Door.stl` / `.step` | `5,274.9` | `612` | `True` | `63.7 × 36.8 × 3.0` | `2.7` |
| 6 | `Caster_Socket_Housing` | `Grp_Front_Ball_Caster` | `Caster_Socket_Housing.stl` / `.step` | `5,451.0` | `1,708` | `True` | `38.0 × 38.0 × 11.0` | `2.8` |
| 7 | `ESP32_CAM_Bracket` | `Grp_ESP32_CAM` | `ESP32_CAM_Bracket.stl` / `.step` | `4,625.5` | `436` | `True` | `18.25 × 50.0 × 11.0` | `2.4` |
| 8 | `LiDAR_Pillar_Clamps` | `Grp_LiDAR_Mount` | `LiDAR_Pillar_Clamps.stl` / `.step` | `1,769.4` | `448` | `True` | `88.0 × 84.0 × 3.0` | `0.9` |

---

### 2.3 Hardware & Fastener Schedule

| Subsystem | Fastener / Hardware | Qty | Notes |
|---|---|---:|---|
| Front Ball Caster | `5/8"` (`15.875 mm`) Hardened Steel Ball (`Caster_Steel_Ball`) | `1` | Snaps into `Caster_Socket_Housing` (`Ø14.40 mm` bottom aperture with `3×` flex slots). |
| Front Ball Caster Mount | `M3 × 10 mm` SHCS + `M3` Heat-Set Inserts (`Ø4.2 × 5.5 mm`) | `3` | Accessible directly from underneath the robot at `R = 14.0 mm` (`0°, 120°, 240°`). |
| Rear Motor Brackets to Chassis Bridge | `M3 × 10 mm` SHCS + `M3` Hex Nuts / Inserts | `8` | `4` per bracket (`X = ±12.5 mm, Y = ±26.8, ±42.8 mm`); accessible from above via `8× Ø6.4 mm` pass-through holes in `Electronics_Deck`. |
| Motors to Brackets | `M3 × 6 mm` Screws | `4` | `2` per `JGA25-371` motor face (`R = 8.55 mm` at `30°/150°`). |
| `Electronics_Deck` to `Lower_Chassis` | `M3 × 10 mm` SHCS + `M3` Heat-Set Inserts | `6` | Perimeter columns at `X ∈ {-43, +65, +183} mm, Y = ±65.5 mm`. |
| `Upper_Enclosure` to `Electronics_Deck` | `M3 × 12 mm` SHCS + `M3` Heat-Set Inserts | `4` | Recessed top corner screw wells at `(-42, ±52)` and `(+164, ±56) mm`. |
| `LiDAR_Pillar_Clamps` to Deck Pillars | `M3 × 8 mm` SHCS + `M3` Heat-Set Inserts | `4` | Clamps unmodified `LDS02RR_Plate` onto the 4 stepped pillars at `(-18, ±37.5)` and `(+58, ±37.5) mm`. |
| `LDS02RR` LiDAR to `LDS02RR_Plate` | `M3 × 8 mm` SHCS | `4` | Bolts through the 4 counterbored bosses of `LDS02RR_Plate.stl`. |
| `MPU9250` IMU to Deck Standoffs | `M3 × 6 mm` Self-Tapping / SHCS | `2` | At `(55.0 ± 10.57, -5.30) mm` (`Ø2.55 mm` pilot bores). |
| `UI_Button_Carrier` & `ESP32_CAM_Bracket` | `M3 × 8 mm` Self-Tapping / SHCS | `6` | `4` on button carrier (`140 ± 21, ±21 mm`) + `2` on camera bracket (`Y = ±20, Z = 86.5 mm`). |
| `0.96"` OLED to Roof Bosses | `M2 × 5 mm` Self-Tapping Screws | `4` | `Ø1.70 mm` pilot holes in `4×` underside roof bosses. |

---

## 3. Consolidated Verification Matrix (Brief §16 — `26 / 26` Passed)

All 26 requirements from Section 16 of `robot_description.txt` are verified programmatically by `verify_all.py` (log in `verify_log.txt`, structured JSON in `export/build_done.json`):

| # | Brief §16 Requirement | Status | Measured Evidence (`verify_all.py`) |
|---:|---|:---:|---|
| 01 | Exact local CAD files used for all applicable reference components | **PASS** | `14/14` local files in `FreeCAD_ws/models` referenced (`missing=[]`). |
| 02 | No internet-downloaded component models used | **PASS** | Zero network imports (`[]`); all 14 local models verified by SHA-1 in `measure/recon.json`. |
| 03 | All imported component dimensions measured before designing mounts | **PASS** | `measure/recon.json` (`14` files), `measure/census.json`, and `measure/DATASHEET.md` (`12,776 B`) generated prior to layout. |
| 04 | Chassis/enclosure footprint is `250 × 150 mm` | **PASS** | Combined enclosure `X = 250.000 mm` (`[-55.00, +195.00]`), `Y = 150.000 mm` (`[-75.00, +75.00]`). |
| 05 | Maximum height without LiDAR is `< 150 mm` | **PASS** | Non-LiDAR `ZMax = 112.40 mm` (`Upper_Enclosure` roof `112.00 mm`, switch caps `112.40 mm < 150.0 mm`). |
| 06 | All printable parts fit within `256 × 256 × 256 mm` Bambu Lab A1 volume | **PASS** | Largest parts (`Lower_Chassis`, `Electronics_Deck`, `Upper_Enclosure`) are `250.0 × 150.0 × 47.0 mm` (`<= 256 mm`). |
| 07 | Motors and wheels located at the rear (not centered in `250 mm` length) | **PASS** | Axle at `X = 0.00 mm` (`55.0 mm` from rear edge `X_MIN = -55.0 mm`, vs. chassis midpoint `X = +70.0 mm`). |
| 08 | Ball caster at front, centered on `Y = 0`, stable 3-point ground contact | **PASS** | Caster at `(164.99, 0.00) mm`, ball `ZMin = 0.000 mm`, wheels `ZMin = 0.036 mm`, chassis ground clearance `= 14.00 mm`. |
| 09 | Wheels rotate freely and side-wall opening clears wheel hub | **PASS** | `360°` swept wheel clearance volume `L = 0.000, R = 0.000 mm³`; `Ø22.0 mm` wall opening clears `Ø13.2 mm` hub (`0.000 mm³`). |
| 10 | Motor shafts collinear and brackets symmetric left-to-right | **PASS** | Wheel L/R Z-centers `(32.50, 32.50) mm`, bracket Y spans `+[21.8, 72.0]` and `[-72.0, -21.8] mm`. |
| 11 | LiDAR center aligned with motor axle midpoint `(0, 0)` and buried inside | **PASS** | Turret center `(0.000, 0.000) mm`; stationary body `ZMax = 108.00 mm < Z_ROOF_BOT = 108.50 mm`; rotating head `ZMax = 126.50 mm`. |
| 12 | LiDAR has an unobstructed `360°` horizontal scanning field | **PASS** | `360°` scan annulus `Z ∈ [112.5, 126.5] mm` (`R = 35.4..220 mm`) intersection with all non-LiDAR parts `= 0.000 mm³`. |
| 13 | `MPU9250` mounted horizontally in ROS 2 orientation (`X=fwd, Y=left, Z=up`) | **PASS** | Placement rotation quaternion `= (0.0, 0.0, 0.0, 1.0)` (identity). |
| 14 | `MPU9250` located at exact centroid of wheel/caster support triangle | **PASS** | IMU center `= (55.00, 0.00) mm` vs. `((0 + 0 + 165)/3 = 55.00, 0.00) mm`. |
| 15 | `3×18650` cells + holder independently removable without dismantling robot | **PASS** | Door `+5 mm` lift vol `= 0.000`, `-Y` pull vol `= 0.000`, `Ø24 mm` thumb-hole vol `= 0.000`, holder extraction corridor vol `= 0.000 mm³`. |
| 16 | OLED on top surface facing rearward with screen window masking PCB | **PASS** | `13.0 × 24.0 mm` window `100%` clear (`0.000 mm³`), masking the `27.9 × 26.7 mm` PCB below `Z_ROOF_BOT = 108.50 mm`. |
| 17 | Four `12 mm` tactile switches + caps accessible in `UP/DOWN/RETURN/ENTER` layout | **PASS** | `UP X = 159.0`, `DOWN X = 121.0`, `RETURN Y = +19.0`, `ENTER Y = -19.0 mm`, cap crowns at `Z = 112.40 mm` + engraved legends. |
| 18 | RGB LED (dome facing up through panel) and buzzer mounted near display | **PASS** | LED dome `ZMax = 112.35 mm > 112.0 mm` roof; LED-to-Buzzer center distance `= 18.0 mm` adjacent to OLED at `X = 94.0 mm`. |
| 19 | Buzzer uses multi-hole acoustic grille (`7` small holes) aligned with buzzer | **PASS** | `7/7` holes (`Ø2.2 mm` hex pattern) verified open through roof directly above buzzer at `(94.0, 44.0) mm`. |
| 20 | `ESP32-CAM` centered on front side (`Y = 0`) with unobstructed forward FOV | **PASS** | Lens at `(194.50, 0.00, 98.50) mm`; `Ø10.0 mm` forward FOV cylinder obstruction `= 0.000 mm³`. |
| 21 | `ON/OFF` switch externally accessible on rear wall with actuator facing `-X` | **PASS** | Rocker protrudes to `X = -61.95 mm` (`6.95 mm` proud of rear wall `X = -55.0 mm`) at `(Y = 0.0, Z = 76.0) mm`. |
| 22 | All structural fasteners remain accessible after assembly | **PASS** | `15/15` screwdriver/hex-key access cylinders (`Upper_Enclosure`, `Electronics_Deck`, `Caster_Socket_Housing`) clear (`0.000 mm³`). |
| 23 | Zero unexpected collisions across all 24 B-rep solids and 4 mesh components | **PASS** | `44` bbox-overlapping B-rep pairs checked (`unexpected_hits = []`) + vertex/slice envelope checks on all 4 meshes. |
| 24 | No component trapped against maintenance (`Upper_Enclosure` vertical lift check) | **PASS** | `Upper_Enclosure` `+25 mm` vertical lift interference with `LDS02RR_LiDAR` & `Electronics_Deck` `= 0.000 mm³`. |
| 25 | Major printed parts have flat bed faces and require minimal/no supports | **PASS** | `Lower_Chassis ZMin = 14.00`, `Electronics_Deck ZMin = 61.00`, `Upper_Enclosure ZMax = 112.00 mm` (`7/8` parts print support-free). |
| 26 | Completed assembly organized into all `14` required FreeCAD groups | **PASS** | `14/14` groups present and populated (`28` total objects). |

---

## 4. Assembly & Serviceability Sequence

1. **Lower Drivetrain & Battery Bay (`Stage 1`)**:
   - Press `6× M3` heat-set inserts into the top of the `Lower_Chassis` perimeter columns and `3× M3` heat-set inserts into the underside front caster pad.
   - Bolt each `JGA25-371` motor to its `JGA25-371_Bracket` (`2× M3×6`), then bolt both brackets upward against the `6.0 mm` internal motor bridge (`8× M3×10`). Press the two `65mm_Wheel` hubs onto the D-shafts through the `Ø22 mm` side wall openings.
   - Snap the `5/8"` steel ball into `Caster_Socket_Housing` and bolt the housing to the underside of the front floor pad with `3× M3×10` screws (serviceable at any time from underneath without opening the robot).
   - Slide `Battery_Holder_3x18650` onto the tray rails (`X = 75, Y = 0, Z = 21.5 mm`), snap the top and bottom pivot pins of `Battery_Door` into the chassis hinge sockets at `(107.0, -73.5) mm`, and press the aft latch arm closed until the 35° retention tooth snaps securely behind the doorway jamb. To remove the battery at any time without tools: press the flush thumb release grip in the exterior jamb pocket to deflect the cantilever latch arm, swing the door open 90° outwards, push up on the battery holder through the `Ø24 mm` floor thumb hole to clear the `3 mm` retention lip, and slide the holder out sideways along `-Y`.
2. **Electronics Deck, LiDAR & Centroid IMU (`Stage 2`)**:
   - Bolt `Electronics_Deck` onto `Lower_Chassis` using `6× M3×10` socket-head screws. (The `8× Ø6.4 mm` access holes in the deck allow a hex key to reach all 8 motor-bracket screws even with the deck installed.)
   - Bolt `MPU9250_IMU` onto the two deck standoffs at `(55.00, 0.00) mm` (`2× M3×6`), routing its header jumper through the adjacent deck slot.
   - Seat `LDS02RR_Plate` onto the `4×` stepped deck pillars (`Z = 77.80 mm`) and secure its edges with `LiDAR_Pillar_Clamps` (`4× M3×8`). Bolt `LDS02RR_LiDAR` onto the 4 plate bosses (`4× M3×8`).
3. **Upper Enclosure, UI Panel, Camera & Power Switch (`Stage 3`)**:
   - Fasten `OLED_Display_096` (`4× M2×5`), `UI_Button_Carrier` with `4×` tactile switches + caps (`4× M3×8`), `RGB_Status_LED`, `Acoustic_Buzzer`, `ESP32_CAM_Module` + `ESP32_CAM_Bracket` (`2× M3×8`), and snap `Rear_Power_Switch` into the rear wall cutout.
   - Lower `Upper_Enclosure` straight down (`-Z`) over the `LDS02RR` rotating turret head (`Ø71.3 mm` opening clears `Ø69.7 mm` turret with `0.8 mm` radial clearance) and secure with `4× M3×12` screws in the recessed corner wells.

---

## 5. Verification Scope & Explicit Limitations

- **B-Rep vs. Mesh Collision Verification**:
  - `10` of the `14` local reference files are native STEP B-rep models, and `JGA25-371_Bracket.stl` (`316` facets) was converted into a verified watertight B-rep solid (`measure/bracket_solid.brep`, `isValid() == True`, `7,465.3 mm³`). Together with the `8` printed B-rep parts and `Caster_Steel_Ball`, all `24` B-rep objects were verified pairwise via exact OpenCASCADE `Shape.common().Volume`.
  - The remaining `3` reference files (`JGA25-371.stl` with `16,582` facets, `LDS02RR_Plate.stl` with `12,172` facets and open boundary edges, and `esp32cam_with_MB.stl` with `36,242` facets and non-manifold edges) cannot be converted to single B-rep solids via sewing without mesh repair. Per `freecad-mcp-field-lessons.md` §3 & §19, their clearances against surrounding printed parts (`Lower_Chassis`, `Electronics_Deck`, `LiDAR_Pillar_Clamps`, `Upper_Enclosure`, `ESP32_CAM_Bracket`, `MPU9250_IMU`) were verified using exact transformed mesh vertex envelopes (`m.Topology[0]`) and cylindrical/box B-rep clearance probes rather than direct mesh-to-B-rep boolean `common()`.
