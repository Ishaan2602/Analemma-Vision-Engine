# Analemma Engine - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Usage Examples](#usage-examples)
6. [Command Line Interface](#command-line-interface)
7. [API Reference](#api-reference)
8. [Advanced Features](#advanced-features)

## Introduction

The Analemma Engine is a Python toolkit for calculating and visualizing the **analemma** - the figure-8 shaped path the Sun traces in the sky when photographed at the same time each day throughout a year.

### What is an Analemma?

The analemma's distinctive shape results from two astronomical phenomena:

1. **Solar Declination (δ)**: The vertical component, caused by Earth's 23.45° axial tilt
2. **Equation of Time (EoT)**: The horizontal component, caused by:
   - Earth's axial tilt (obliquity)
   - Earth's elliptical orbit (eccentricity)

## Installation

### Requirements
- Python 3.8 or higher
- pip package manager

### Setup

```bash
cd analemma_project
pip install -r requirements.txt

# Run demo
python demo_scripts/quickstart.py
```

### Basic Installation

```bash
# Clone or download the project
cd analemma_project

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- **numpy**: Numerical calculations
- **matplotlib**: Static visualizations
- **pandas**: Data handling
- **astropy** (optional): High-precision calculations
- **plotly** (optional): Interactive visualizations
- **Pillow**: Image processing for anchoring feature

## Quick Start

### Process Images with Automatic Metadata

The easiest way to generate analemma overlays:

```bash
# Process any input image (automatically reads metadata.txt)
python demo_scripts/process_image.py <image_name>

# Examples:
python demo_scripts/process_image.py hongkong
python demo_scripts/process_image.py nigeria
```

This automatically:
- Loads image metadata from `input_images/<name>/metadata.txt`
- Detects sun position using computer vision
- Generates overlay, sky chart, and composite
- Saves to `output/<name>_output/`

### Python API

```python
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter

# Set your location
latitude = 40.1   # Champaign, IL
longitude = -88.2

# Initialize components
calculator = AnalemmaCalculator(mode='approximate')
sky_mapper = SkyMapper(latitude, longitude)
plotter = AnalemmaPlotter()

# Calculate analemma for noon throughout the year
calc_data = calculator.calculate_year(hour=12, minute=0)
sky_data = sky_mapper.map_to_horizon(calc_data)

# Visualize
plotter.plot_analemma(sky_data)
plotter.show()
```

### Command Line

```bash
# Calculate and plot analemma
python analemma_cli.py calculate --lat 40.1 --lon -88.2 --hour 12 --plot --show

# Compare calculation modes
python analemma_cli.py compare --lat 40.1 --lon -88.2 --plot
```

## Core Concepts

### Three-Layer Architecture

The system is organized into three modular layers:

#### Layer 1: AnalemmaCalculator (Physics Engine)
- Pure numerical calculations
- Input: Date/Time
- Output: Declination and Equation of Time
- Dual precision modes:
  - **Approximate**: Fast, educational formulas
  - **High-Precision**: NASA-grade via Astropy

#### Layer 2: SkyMapper (Coordinate Transformation)
- Transforms celestial → horizon coordinates
- Input: (Declination, EoT) + Observer location
- Output: (Altitude, Azimuth) in local sky

#### Layer 3: AnalemmaPlotter (Visualization)
- Multiple visualization types
- Static (matplotlib) and interactive (plotly) plots
- Publication-quality output

### Key Formulas

**Solar Declination (Approximate)**:
```
δ ≈ 23.45° × sin[(360/365)(284+N)]
```
where N is the day of year.

**Altitude Calculation**:
```
sin(a) = sin(φ)sin(δ) + cos(φ)cos(δ)cos(H)
```
where:
- a = altitude
- φ = observer's latitude
- δ = solar declination
- H = hour angle

## Usage Examples

### Example 1: Basic Analemma Plot

```python
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter

# Your location
lat, lon = 40.1, -88.2

# Initialize
calc = AnalemmaCalculator()
mapper = SkyMapper(lat, lon)
plotter = AnalemmaPlotter()

# Calculate for 3 PM throughout the year
data = calc.calculate_year(hour=15, minute=0)
sky_data = mapper.map_to_horizon(data)

# Plot
plotter.plot_analemma(sky_data, save_path="my_analemma.png")
plotter.show()
```

### Example 2: Figure-8 Plot

```python
# Shows the pure astronomical components (EoT vs Declination)
calc = AnalemmaCalculator()
data = calc.calculate_year(hour=12, minute=0)

plotter = AnalemmaPlotter()
plotter.plot_figure8(data)
plotter.show()
```

### Example 3: Mode Comparison

```python
# Compare approximate vs high-precision modes
calc_approx = AnalemmaCalculator(mode='approximate')
calc_precise = AnalemmaCalculator(mode='high-precision')

approx_data = calc_approx.calculate_year(hour=12, minute=0)
precise_data = calc_precise.calculate_year(hour=12, minute=0)

plotter = AnalemmaPlotter()
plotter.plot_comparison(approx_data, precise_data)
plotter.show()
```

### Example 4: Image Anchoring

```python
from datetime import datetime
from analemma.image_anchor import ImageAnchorer

# Initialize with photo metadata
anchorer = ImageAnchorer(
    image_path="sky_photo.jpg",
    anchor_datetime=datetime(2026, 6, 21, 12, 0),
    latitude=40.1,
    longitude=-88.2
)

# Calibrate camera
anchorer.calibrate_from_focal_length(
    focal_length_mm=24,
    sensor_width_mm=36,
    sensor_height_mm=24
)

# Create overlay
anchorer.overlay_analemma(
    output_path="photo_with_analemma.png",
    show_dates=True
)
```

## Command Line Interface

### Calculate Command

Generate analemma calculations and visualizations:

```bash
python analemma_cli.py calculate \
    --lat 40.1 \
    --lon -88.2 \
    --hour 12 \
    --minute 0 \
    --year 2026 \
    --mode approximate \
    --plot \
    --show \
    --output ./outputs
```

**Options**:
- `--lat, --latitude`: Observer's latitude (required)
- `--lon, --longitude`: Observer's longitude (required)
- `--hour`: Hour of observation (0-23, default: 12)
- `--minute`: Minute of observation (0-59, default: 0)
- `--year`: Year for calculation (default: current year)
- `--mode`: `approximate` or `high-precision` (default: approximate)
- `--plot`: Generate plots
- `--show`: Display plots interactively
- `--output, -o`: Output directory for plots

### Compare Command

Compare approximate and high-precision modes:

```bash
python analemma_cli.py compare \
    --lat 40.1 \
    --lon -88.2 \
    --plot \
    --show
```

### Anchor Command

Overlay analemma onto a photograph:

```bash
python analemma_cli.py anchor \
    --image sky_photo.jpg \
    --datetime "2026-06-21 12:00" \
    --lat 40.1 \
    --lon -88.2 \
    --focal-length 24 \
    --output photo_overlay.png
```

**Options**:
- `--image`: Path to sky photograph (required)
- `--datetime`: Photo timestamp in ISO format (required)
- `--lat, --lon`: Photo location coordinates (required)
- `--focal-length`: Camera focal length in mm
- `--fov`: Alternative to focal length: "horizontal,vertical" FOV in degrees
- `--sensor-width`: Sensor width in mm (default: 36)
- `--sensor-height`: Sensor height in mm (default: 24)
- `--no-dates`: Suppress date labels
- `--output, -o`: Output file path

## API Reference

### AnalemmaCalculator

```python
AnalemmaCalculator(mode='approximate', year=None)
```

**Methods**:
- `calculate(date)`: Calculate for specific datetime
- `calculate_year(hour=12, minute=0, days=365)`: Calculate for entire year
- `calculate_declination_approximate(day_of_year)`: Get declination
- `calculate_equation_of_time_approximate(day_of_year)`: Get EoT
- `compare_modes(date)`: Compare both modes

### SkyMapper

```python
SkyMapper(latitude, longitude, timezone_offset=None)
```

**Methods**:
- `map_single_point(calc_result)`: Map one calculation to horizon coords
- `map_to_horizon(calc_results)`: Map list of calculations
- `calculate_altitude(declination, hour_angle)`: Compute altitude
- `calculate_azimuth(declination, hour_angle, altitude)`: Compute azimuth
- `get_solar_noon_time(eot_minutes)`: Find solar noon

### AnalemmaPlotter

```python
AnalemmaPlotter(style='seaborn-v0_8-darkgrid', figure_size=(10, 8))
```

**Methods**:
- `plot_analemma(sky_data, ...)`: Sky chart (alt/az)
- `plot_figure8(calc_data, ...)`: Figure-8 plot (EoT/dec)
- `plot_time_series(calc_data, ...)`: Time series plots
- `plot_sky_dome(sky_data, ...)`: Polar sky projection
- `plot_interactive(sky_data, ...)`: Interactive Plotly plot
- `plot_comparison(approx_data, precise_data, ...)`: Mode comparison

### ImageAnchorer

```python
ImageAnchorer(image_path, anchor_datetime, latitude, longitude, sun_pixel=None)
```

**Methods**:
- `calibrate_from_focal_length(focal_length_mm, ...)`: Calibrate from camera specs
- `calibrate_from_field_of_view(h_fov, v_fov)`: Calibrate from FOV
- `overlay_analemma(output_path, ...)`: Create overlay image
- `get_statistics()`: Get analemma statistics

## Advanced Features

### Image Anchoring with Auto Sun Detection

**Recommended: Use the automated script**

```bash
# Automatically processes image with metadata
python demo_scripts/process_image.py <image_name>
```

**Manual approach for custom workflows:**

```python
from analemma import ImageAnchorer
from analemma.metadata_parser import load_input_image

# Load metadata automatically
metadata = load_input_image('example_name')

# Create anchorer with automatic sun detection
anchorer = ImageAnchorer(
    image_path=metadata['image_path'],
    anchor_datetime=metadata['datetime'],
    latitude=metadata['latitude'],
    longitude=metadata['longitude'],
    auto_detect_sun=True  # Computer vision sun detection
)

# Calibrate camera
anchorer.calibrate_from_focal_length(
    focal_length_mm=metadata['focal_length_mm'],
    sensor_width_mm=metadata['sensor_width_mm'],
    sensor_height_mm=metadata['sensor_height_mm']
)

# Generate overlay
result = anchorer.overlay_analemma(output_path="output/overlay.png")
print(f"Points drawn: {result['points_drawn']}")
```

**Adding your own images:**

1. Create directory: `input_images/yourname/`
2. Add your photo
3. Create `metadata.txt`:
```
IMAGE_FILE=yourphoto.jpg
DATETIME=2024-06-15 14:30:00
LATITUDE=40.1
LONGITUDE=-88.2
FOCAL_LENGTH_MM=5.7
SENSOR_WIDTH_MM=7.8
SENSOR_HEIGHT_MM=5.8
CAMERA_MAKE=Apple
CAMERA_MODEL=iPhone 14
LOCATION_NAME=Your Location
```
4. Run: `python demo_scripts/process_image.py yourname`

#### Technical Limitations: Lens Distortion

**Current Implementation**  
The image anchoring feature uses a **simplified pinhole camera model** that converts sky coordinates to pixel coordinates:

```python
# Simplified projection model
delta_x = delta_az * pixels_per_degree_az
delta_y = -delta_alt * pixels_per_degree_alt
```

This assumes:
- **Rectilinear projection** (straight lines remain straight)
- **No lens distortion** (barrel, pincushion, or fisheye effects)
- **Linear field of view** (same degrees per pixel everywhere)

**Real-World Camera Optics**  
Smartphone cameras (especially wide-angle lenses) exhibit:
- **Barrel distortion**: Straight lines curve outward, especially near edges
- **Non-linear FOV**: Degrees per pixel varies from center to edges
- **Vignetting**: Brightness falloff at edges

**Impact on Accuracy**  
When the sun is near the **image edges** (where distortion is strongest), the overlaid analemma may appear slightly warped or compressed compared to theoretical sky charts. The anchor point (detected sun position) is accurate, but the analemma shape deviates slightly from the pure mathematical model.

**Workarounds and Future Improvements**

*Option 1: Pre-process the image*
```python
from PIL import Image
import numpy as np

# Apply lens distortion correction before anchoring
# Requires camera calibration matrix (OpenCV cv2.undistort)
corrected_image = cv2.undistort(image, camera_matrix, dist_coeffs)
```

*Option 2: Use distortion-aware projection*
```python
# Replace linear projection with radial distortion model
r = np.sqrt(delta_x**2 + delta_y**2)  # Distance from center
distortion_factor = 1 + k1*r**2 + k2*r**4  # Brown-Conrady model
delta_x_corrected = delta_x * distortion_factor
delta_y_corrected = delta_y * distortion_factor
```

*Option 3: Non-rectilinear projections*
- **Equirectangular**: Linear in azimuth/altitude (better for wide FOV)
- **Stereographic**: Preserves angles, common in fisheye lenses
- **Gnomonic**: True rectilinear, requires undistorted images

**Practical Recommendations**
- For **demonstration purposes**: Current model is sufficient
- For **scientific accuracy**: Apply lens correction or use calibrated cameras
- For **casual use**: Keep sun near image center where distortion is minimal
- For **research**: Use cameras with known distortion coefficients

### Custom Time of Day

Observe the analemma at any time:

```python
# Morning analemma (8 AM)
data = calculator.calculate_year(hour=8, minute=0)

# Evening analemma (5:30 PM)
data = calculator.calculate_year(hour=17, minute=30)
```

### Different Locations

Compare analemmas at different latitudes:

```python
locations = [
    (65, -20, "Iceland"),
    (40, -88, "Illinois"),
    (0, -78, "Ecuador"),
    (-34, 18, "Cape Town")
]

for lat, lon, name in locations:
    mapper = SkyMapper(lat, lon)
    sky_data = mapper.map_to_horizon(calc_data)
    plotter.plot_analemma(sky_data, title=f"Analemma at {name}")
```

### Interactive Visualization

```python
# Requires plotly
plotter = AnalemmaPlotter()
fig = plotter.plot_interactive(sky_data)
fig.show()  # Opens in browser
```

### Export Data

```python
import pandas as pd

# Convert to DataFrame for analysis
df = pd.DataFrame(sky_data)
df.to_csv("analemma_data.csv", index=False)

# Access specific fields
print(df[['date', 'altitude', 'azimuth', 'declination', 'eot']])
```

## Troubleshooting

### Astropy Not Found

If you see warnings about astropy:
```bash
pip install astropy
```

### Plotly Not Available

For interactive plots:
```bash
pip install plotly
```

### Import Errors

Make sure you're in the project directory or have installed the package:
```bash
cd analemma_project
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Further Reading

- **examples/**: Runnable example scripts
- **tests/**: Unit tests and validation
- OpenCV Camera Calibration: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
- Brown-Conrady Distortion Model: https://en.wikipedia.org/wiki/Distortion_(optics)

## Contributing

This is an educational/research project. Contributions welcome!

---

**Note**: This project does not currently have a license. All rights reserved.
