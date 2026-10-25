# Autodesk Fusion 360 MCP Automation & Porting Workflow

> [!NOTE]
> **Porting Reference**: This suite represents a complete parametric port to **Autodesk Fusion 360** from the FreeCAD project [`ros2-diffdrive-robot-cad`](https://github.com/med-yassine-ben-salah/ros2-diffdrive-robot-cad). It demonstrates how to drive native CAD geometry, user parameters, B-Rep bodies, and assembly exports via the official Fusion MCP Server.

This guide documents the architecture, automation flow, and development guidelines for driving **Autodesk Fusion 360** directly via the **official Fusion Model Context Protocol (MCP) Server**.

---

## 1. Fusion MCP Server Architecture

Autodesk Fusion includes a native MCP server adapter that exposes a thread-safe execution endpoint over **Streamable HTTP**.

```
+-------------------------------------------------------------+
|                 AI Coding Agent / Client                     |
|           (Antigravity / Cursor / Claude Desktop)            |
+-------------------------------------------------------------+
                              |
                     Streamable HTTP POST
                 http://127.0.0.1:27182/mcp
                              |
+-------------------------------------------------------------+
|               Autodesk Fusion 360 (PID 3352)                |
|  +-------------------------------------------------------+  |
|  |           Native MCP Server Adapter                   |  |
|  |     (Session Management via MCP-Session-Id)           |  |
|  +-------------------------------------------------------+  |
|                             |                               |
|                     Main Thread Task                         |
|                             v                               |
|  +-------------------------------------------------------+  |
|  |                 Fusion 360 Python API                 |  |
|  |        adsk.core, adsk.fusion, B-Rep Modeling         |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### Exposed MCP Tools

1. **`fusion_mcp_execute`**:
   - `featureType: "script"`: Executes arbitrary Python scripts dynamically inside the active Fusion session using `adsk.core` and `adsk.fusion`. Requires a `def run(_context: str):` entry point.
   - `document`: Handles opening, closing, and saving documents.
2. **`fusion_mcp_read`**:
   - `queryType: "screenshot"`: Captures real-time PNG screenshots of the Fusion 360 viewport.
   - `queryType: "document"`: Queries active/recent documents and cloud project structures.
   - `queryType: "activeCommand"`: Detects if any interactive command dialog is currently blocking the main thread.
   - `queryType: "apiDocumentation"`: Searches built-in Fusion API reference.
3. **`fusion_mcp_update`**:
   - `featureType: "undo"` / `"redo"`: Undoes or redoes operations in the active design.
4. **`fusion_mcp_electronics_read`**:
   - Inspects schematics, PCB board designs, components, and electrical nets.

---

## 2. Key Differences: FreeCAD vs. Autodesk Fusion 360 API

| Concept | FreeCAD (`FreeCAD`, `Part`, `Mesh`) | Autodesk Fusion 360 (`adsk.core`, `adsk.fusion`) |
| :--- | :--- | :--- |
| **Units** | Millimeters (`mm`) everywhere | Database internal units are **Centimeters (`cm`)**. Values must use `0.1` scaling or `ValueInput.createByString("... mm")`. |
| **Document Hierarchy** | `App.Document` > `FeaturePython` / `Part::Feature` | `Document` > `Design` (`adsk.fusion.Design`) > `rootComponent` > `Occurrences` > `Components`. |
| **Parameters** | Spreadsheet or dynamic Python properties | **User Parameters Table** (`design.userParameters.add(...)`), visible under *Modify > Change Parameters*. |
| **Visual Materials** | `ViewObject.ShapeColor` RGBA tuple | **Appearance Library** (`Fusion Appearance Library`) mapped to bodies or components. |
| **View Navigation** | `Gui.ActiveDocument.ActiveView` | `app.activeViewport.camera` (`CameraTypes.OrthographicCameraType`), `vp.saveAsImageFile(...)`. |
| **Assembly Structure** | App::Part or FreeCAD Assembly4 groups | Native multi-component assembly with occurrences and rigid / kinematic joints. |

---

## 3. Script Execution Lifecycle in Fusion

Any automated script executed via `fusion_mcp_execute` must adhere to the following contract:

```python
import adsk.core
import adsk.fusion

def run(_context: str):
    app = adsk.core.Application.get()
    design = app.activeProduct
    root_comp = design.rootComponent
    
    # 1. Inspect or modify design
    # 2. Add sketches, extrusions, fillets, or import STEP solids
    # 3. Print output to stdout (captured and returned by MCP tool)
    print("Execution complete!")
```

### Safety Rules:
- **Do NOT catch exceptions in `run()`**: Uncaught exceptions yield exact stack traces back to the MCP client for automated self-healing.
- **Dialog Concurrency**: Non-readonly scripts cannot run while a native modal dialog is open in Fusion. Close any open dialogs before initiating automation runs.
