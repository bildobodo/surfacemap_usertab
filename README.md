# LinuxCNC Probe Basic Surface Compensation User Tab

This is a user tab to simplify surface mapping and compensation for Probe Basic (a LinuxCNC GUI).

## Installation

1. Install compensation component by scottalford75: https://github.com/scottalford75/LinuxCNC-3D-Printing/tree/master/compensation
2. Copy the `surfacemap` directory into `~/linuxcnc/configs/yourconfig/user_tabs/`
3. Copy contents of `subroutines` folder into `~/linuxcnc/configs/yourconfig/subroutines/`

## Usage

### Grid Parameters

Define the rectangular grid area to be probed:

- **x0**: Lower X coordinate of the grid (start position)
- **x1**: Upper X coordinate of the grid (end position, must be > x0)
- **y0**: Lower Y coordinate of the grid (start position)
- **y1**: Upper Y coordinate of the grid (end position, must be > y0)
- **Num Probes X**: Number of probe points along the X axis (minimum 2, must be an integer)
- **Num Probes Y**: Number of probe points along the Y axis (minimum 2, must be an integer)

The system automatically calculates the spacing between probe points:
- X spacing = (x1 - x0) / (Num Probes X - 1)
- Y spacing = (y1 - y0) / (Num Probes Y - 1)

### Probing Settings

- **Probe Fast Feedrate**: Fast probe feedrate for initial contact (e.g., 100 mm/min, must be > 0)
- **Probe Slow Feedrate**: Slow probe feedrate for accurate measurement (e.g., 20 mm/min, must be ≥ 0). Set to 0 to disable slow probe pass.
- **Safe Z**: Safe Z height in current work coordinate system for traversal between probe points
- **Search Depth**: Maximum downward search distance (must be negative, e.g., -10)

### Operation

1. **Home all axes** before starting
2. **Set your work coordinate system** (the scan operates in the currently active WCS)
3. **Fill in all parameters** - they will be automatically stored when changed
4. Click **"Scan Surface"** to start the probing operation
5. The scan will:
   - Disable compensation
   - Move to machine Z0 for safety
   - Move to the starting position (x0, y0)
   - Probe in a snaking pattern (left-to-right, then right-to-left alternating)
   - Store results in `probe-results.txt`
6. Click **"Compensation Enable"** to enable/disable compensation
   - Button turns **green** when compensation is enabled
   - Button is **gray** when compensation is disabled

## Technical Details

### Probing Pattern

The system uses a snaking pattern to minimize travel time:
```
Row 0: x0 → x1 (left to right)
Row 1: x1 → x0 (right to left)
Row 2: x0 → x1 (left to right)
...
```

### Probe Results File

Results are stored in `probe-results.txt` with:
- Work Coordinate Offsets (WCO) in the header
- Each probed point in machine coordinates (X, Y, Z)

### Parameter Storage

Parameters are stored in LinuxCNC userspace variables:
- #3050 = x0
- #3051 = x1
- #3052 = y0
- #3053 = y1
- #3054 = xprobes (number of probes in X)
- #3055 = yprobes (number of probes in Y)
- #3056 = fast_fr (fast feedrate)
- #3057 = slow_fr (slow feedrate)
- #3058 = safez (safe Z height)
- #3059 = depthz (search depth)

## Safety Notes

⚠️ **Always verify parameters before scanning:**
- Ensure the probe will not crash into fixtures or the part
- Verify safe Z is high enough to clear all obstacles
- Ensure search depth won't cause collisions
- Test with a small grid first

⚠️ **The machine will move in G53 (machine coordinates) for Z-axis safety moves**
