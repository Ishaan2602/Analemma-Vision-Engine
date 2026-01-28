# Metadata Requirements - Technical Reference

## What Metadata Does the Analemma Engine Actually Use?

### REQUIRED (7 fields - Core Functionality)

These fields are **absolutely necessary** for the analemma overlay to work:

1. **IMAGE_FILE** - Filename of the photo
   - Used to: Load the image
   
2. **DATETIME** - When the photo was taken
   - Format: `YYYY-MM-DD HH:MM:SS`
   - Used to: Calculate solar position at that specific moment
   
3. **LATITUDE** - GPS latitude in decimal degrees
   - Used to: Calculate sun's altitude/azimuth for observer's location
   
4. **LONGITUDE** - GPS longitude in decimal degrees  
   - Used to: Calculate sun's altitude/azimuth for observer's location
   
5. **FOCAL_LENGTH_MM** - Camera lens focal length (mm)
   - Used to: Calculate field of view (FOV)
   
6. **SENSOR_WIDTH_MM** - Camera sensor width (mm)
   - Used to: Calculate horizontal FOV via: `FOV = 2 × arctan(sensor/2focal)`
   
7. **SENSOR_HEIGHT_MM** - Camera sensor height (mm)
   - Used to: Calculate vertical FOV

**Math:** 
```python
h_fov = 2 * arctan(sensor_width / (2 * focal_length))
v_fov = 2 * arctan(sensor_height / (2 * focal_length))
pixels_per_degree_h = image_width / h_fov
pixels_per_degree_v = image_height / v_fov
```

### OPTIONAL (Enhances but not required)

4. **ALTITUDE_M** - Elevation above sea level (meters)
   - Currently: Not used
   - Future use: Atmospheric refraction corrections, pressure calculations
   
5. **CAMERA_MAKE**, **CAMERA_MODEL** - Camera identification
   - Used to: Display in output, debugging, sensor size lookup tables
   
6. **LOCATION_NAME** - Human-readable location
   - Used to: Display in plot titles and output

### NOT USED (Reference Only)

The following EXIF data is commonly available but **NOT used** by our calculations:

❌ **Exposure Settings:**
- Exposure time (shutter speed)
- F-number (aperture)
- ISO speed rating
- APEX values (brightness, exposure bias, etc.)

❌ **Image Processing:**
- Color space (sRGB, etc.)
- White balance
- Scene capture type
- Metering mode

❌ **Resolution:**
- DPI (horizontal/vertical resolution)
- Focal plane resolution

❌ **Camera Features:**
- Flash settings
- Digital zoom ratio
- Custom image processing
- Software version

❌ **Orientation:**
- Orientation tag (we handle this automatically via `ImageOps.exif_transpose()`)

## Why So Little?

The analemma overlay is a **geometric problem**, not a photographic one:

1. **Where** was the photo taken? → GPS coordinates
2. **When** was it taken? → Datetime
3. **What angle** does the camera see? → Focal length + sensor size

Everything else (exposure, color, processing) affects how the photo *looks*, not where the sun appears in the sky.

## Sensor Size: Why We Need It

**Common misconception:** "Focal length tells you the FOV"

**Reality:** Focal length ALONE is meaningless without sensor size.

**Example - Same 50mm lens:**
- Full frame camera (36mm sensor): 40° FOV
- APS-C camera (23.5mm sensor): 27° FOV
- Smartphone (6mm sensor): 66° FOV

The focal length is the distance from lens to sensor. The sensor size determines how much of the projected image you capture.

## Future Enhancements (Would Use More Metadata)

If we wanted to add these features, we'd need:

1. **Atmospheric refraction** → Altitude, temperature, pressure
2. **Lens distortion correction** → Distortion coefficients (k1, k2, p1, p2)
3. **Camera calibration matrix** → Intrinsic parameters from OpenCV calibration
4. **Horizon detection** → Possibly orientation, tilt sensors
5. **Precise timing** → GPS timestamp with subseconds

But for our current **demonstration/educational tool**, the core 7 fields are sufficient.

## Metadata File Format

```
# === REQUIRED METADATA ===
IMAGE_FILE=photo.jpg
DATETIME=2024-06-15 14:30:00
LATITUDE=40.1
LONGITUDE=-88.2
FOCAL_LENGTH_MM=5.7
SENSOR_WIDTH_MM=7.8
SENSOR_HEIGHT_MM=5.8

# === OPTIONAL METADATA ===
CAMERA_MAKE=Apple
CAMERA_MODEL=iPhone 14
LOCATION_NAME=Campus

# --- REFERENCE DATA (NOT PARSED) ---
# Everything below this line is ignored
# Use for notes, full EXIF dumps, etc.
```

The parser reads KEY=VALUE pairs until it hits the separator, then stops.
