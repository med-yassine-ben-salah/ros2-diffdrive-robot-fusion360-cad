# FDM Printability & Slicer Review — ROS 2 Differential-Drive Robot

- **Target Printer**: Bambu Lab A1 (`256 × 256 × 256 mm` build volume, PEI textured plate)
- **Material**: PLA (`1.24 g/cm³`)
- **Nozzle / Layer Height**: `0.4 mm` nozzle, `0.20 mm` standard layer height (`0.16 mm` optional on `Upper_Enclosure` for crisp top-panel text and crown chamfer steps)

---

## 1. Per-Part Print Orientation & Support Strategy

| Part Name | Print-Oriented File | Bed Footprint (`X × Y × Z` mm) | Bed Contact Area (`mm²`) | Steep Overhang Area (`mm²`) | Support Strategy | Est. PLA Mass (`g`) |
|---|---|---:|---:|---:|---|---:|
| `Lower_Chassis` | `Lower_Chassis_print_oriented.stl` | `250.0 × 150.0 × 47.0` | `35,787.1` | `5,411.8` | **Normal / Tree supports (build-plate / local only)** under the internal `6.0 mm` motor bridge span (`Z = 41.0 mm` above bed) and side wheel-hub openings (`Ø22 mm`). Flat `250 × 150 mm` octagonal bottom plate (`18 × 18 mm` 45° corners + `0.6 mm` elephant-foot relief chamfer) lies directly on the bed; all exterior recessed bays and corner flutes have `45°` beveled overhangs, the battery door window has a `45°` beveled lintel and `45°` gable groove ceiling, and the `8×` vertical intake louvers (`2.6 mm` wide) have `45°` gable tips. | `171.8 g` |
| `Electronics_Deck` | `Electronics_Deck_print_oriented.stl` | `250.0 × 150.0 × 16.8` | `34,894.2` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. `100%` flat `250 × 150 mm` octagonal underside with `0.8 mm` perimeter chamfer lies on the build plate; all stiffening ribs, zip-tie anchor slots, IMU standoffs, and stepped LiDAR pillars grow straight upward (`+Z`). | `80.6 g` |
| `Upper_Enclosure` | `Upper_Enclosure_print_oriented.stl` | `250.0 × 150.0 × 47.0` | `27,050.9` | `3,194.5` | **Zero roof supports (`SUPPORTS = NO` or local build-plate brim only)**. Flipped `180°` upside-down so the flat `Z = 112.0 mm` top roof prints directly against the PEI build plate; the `5.5 mm × 45°` octagonal crown chamfer, `45°` beveled exterior rib bays, `45°` corner bumper flutes, `45°` conical corner screw counterbores, and `32×` `45°` gable-tipped cooling louvers (`2.6 mm` wide) print cleanly without supports. | `116.0 g` |
| `Battery_Door` | `Battery_Door_print_oriented.stl` | `63.7 × 36.8 × 3.0` | `1,876.2` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. Rotated `-90°` about `X` so its `100%` flat inner face (`Y = -72.0 mm`) lies directly on the build plate (`1,876.2 mm²` bed contact, `0.0 mm²` overhang); all exterior ribs, pivot trunnion pins, latch tooth lead-in ramp, and thumb grip serrations face upward. | `2.7 g` |
| `Caster_Socket_Housing` | `Caster_Socket_Housing_print_oriented.stl` | `38.0 × 38.0 × 11.0` | `1,010.7` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. Flipped `180°` so the `100%` flat `Ø38.0 mm` top flange face (`Z = 14.0 mm`, `1,010.7 mm²`) lies directly on the build plate; the spherical ball socket (`0.30 mm` radial clearance, max overhang `< 30°` from vertical) and `45°` conical M3 counterbores have `0.0 mm²` steep overhang. | `2.8 g` |
| `UI_Button_Carrier` | `UI_Button_Carrier_print_oriented.stl` | `52.0 × 52.0 × 4.15` | `2,168.5` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. Flat `52 × 52 mm` bottom face on build plate; switch cradle pockets face upward. | `4.3 g` |
| `ESP32_CAM_Bracket` | `ESP32_CAM_Bracket_print_oriented.stl` | `18.25 × 50.0 × 11.0` | `470.0` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. Flat U-frame bottom face on build plate. | `2.4 g` |
| `LiDAR_Pillar_Clamps` | `LiDAR_Pillar_Clamps_print_oriented.stl` | `88.0 × 84.0 × 3.0` | `589.8` | `0.0` | **Zero supports (`SUPPORTS = NO`)**. Four flat `12 × 13 × 3 mm` clamp caps on build plate. | `0.9 g` |
| **Total Printed Set** | — | Max `250.0 × 150.0 × 47.0` | — | — | **7 of 8 parts print support-free** (`6` parts have `0.0 mm²` steep overhang; `Lower_Chassis` uses local support under the internal motor bridge) | **`381.9 g`** |

---

## 2. Slicer Settings Recipe (Bambu Studio — Bambu Lab A1)

1. **Wall Loops (Perimeters)**:
   - `4 walls` (`1.6 mm` shell thickness) for `Lower_Chassis`, `Electronics_Deck`, `Caster_Socket_Housing`, and `ESP32_CAM_Bracket` to maximize hoop strength around M3 heat-set insert bores (`Ø4.2 mm`) and motor bracket fasteners.
   - `3 walls` (`1.2 mm`) for `Upper_Enclosure`, `Battery_Door`, `UI_Button_Carrier`, and `LiDAR_Pillar_Clamps`.
2. **Top / Bottom Shell Layers**:
   - `5 top / 5 bottom` layers (`1.0 mm` solid skin at `0.20 mm` layer height).
3. **Infill**:
   - `20% Gyroid` on `Lower_Chassis`, `Electronics_Deck`, and `Upper_Enclosure`.
   - `35% Gyroid` on `Caster_Socket_Housing`, `ESP32_CAM_Bracket`, and `LiDAR_Pillar_Clamps`.
4. **Bed Adhesion**:
   - Textured PEI plate at `60 °C`, nozzle at `220 °C`.
   - Use a `5 mm` outer brim on `Lower_Chassis`, `Electronics_Deck`, and `Upper_Enclosure` (`250 × 150 mm` footprint leaves `3.0 mm` per side on the `256 mm` X-axis; disable skirt loops so the `250.0 mm` part + `2.5 mm` brim fits well inside the `256.0 mm` printable X span).
