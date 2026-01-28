# Analemma Engine - Technical Description

**Python computational system for solar position calculation and astronomical visualization with automated computer vision-based image anchoring**

**Period**: 2026 | **Language**: Python 3.8+ | **Architecture**: 4-layer modular design

## Mathematical Foundations

**Analemma Physics** (figure-8 shape from two phenomena):
- **Solar Declination (δ)**: Earth's 23.45° axial tilt → vertical displacement
- **Equation of Time (EoT)**: Orbital eccentricity + obliquity → horizontal displacement (Kepler's 2nd law)

**Key Equations**:
```
δ ≈ 23.45° × sin[(360°/365)(284 + N)]
sin(a) = sin(φ)sin(δ) + cos(φ)cos(δ)cos(H)
H = (t_obs - 12h) × 15°/h + EoT/4 + (λ - λ_tz)
```

**Dual-Mode Calculations**:
1. **Approximate**: Sine-wave formulas (fast, educational)
2. **High-Precision**: NASA SPICE kernels via Astropy (JPL ephemeris DE440/DE441)

## Architecture

**Layer 1 - Physics Engine** (`AnalemmaCalculator`):
- Numerical solar ephemeris: (Date, Time) → (Declination, EoT)
- Vectorized NumPy operations (365 points in <10ms)
- Strategy pattern for mode switching

**Layer 2 - Coordinate Mapper** (`SkyMapper`):
- Celestial → horizon frame: (δ, EoT, lat, lon) → (Altitude, Azimuth)
- Spherical trigonometry transformations
- Automatic timezone detection (15°/hour)

**Layer 3 - Visualization** (`AnalemmaPlotter`):
- 5 plot types: sky charts, figure-8, time series, polar, comparisons
- matplotlib (static), plotly (interactive)
- Vector (SVG/PDF) and raster (PNG/JPG) export

**Layer 4 - Computer Vision** (`ImageAnchorer`):
- Automated sun detection + analemma overlay on photographs
- scipy blob detection with brightness weighting
- Camera calibration from EXIF metadata

## Computer Vision Pipeline

**Sun Detection**:
1. EXIF orientation correction → RGB to grayscale (max-channel)
2. Adaptive thresholding (99.9th percentile) → binary mask
3. Connected component labeling (`scipy.ndimage.label()`)
4. Brightness-weighted center-of-mass → sub-pixel accuracy (<5px error)

**Camera Calibration**:
```
FOV = 2 × arctan(sensor_size / (2 × focal_length))
pixels_per_degree = image_size / FOV
```
Required: focal length (mm), sensor dimensions (mm), image resolution (px)

**Overlay Process**:
- Calculate anchor sun position → generate year-long analemma
- Filter horizon (alt < 0°) → transform sky → pixel coordinates
- Render with altitude-modulated markers + alpha blending

## Metadata Automation

**KEY=VALUE Parser**:
- Required (7): IMAGE_FILE, DATETIME, LAT, LON, FOCAL_LENGTH_MM, SENSOR_WIDTH_MM, SENSOR_HEIGHT_MM
- Optional: ALTITUDE_M, CAMERA_MAKE/MODEL, LOCATION_NAME
- Type inference: float, datetime, string
- Stops at separator (machine-readable vs. reference sections)

**End-to-End Pipeline** (`process_image.py`):
```
metadata.txt → parse → ImageAnchorer → detect sun → calibrate → 
overlay + sky chart + composite → organized output/
```

## Technologies

**Core**: NumPy, Matplotlib, Pandas, Pillow  
**Optional**: Astropy (ephemeris), SciPy (blob detection), Plotly (interactive)  
**Tools**: argparse (CLI), pathlib, datetime

## Validation & Testing

**Unit Tests**: Solstice/equinox declinations, EoT extrema, singularity handling  
**Datasets**: Hong Kong (22.3°N), Nigeria (9.8°N), UIUC (40.1°N)  
**Validation**: Published ephemeris comparison, >95% sun detection success

## Performance

- Full-year calc: ~5-10ms (approximate), <1ms (single timestamp)
- Image overlay: ~100-200ms | Sun detection: ~50-100ms (scipy)
- Memory: <100MB (images), ~50KB (year data)
- Vectorized → parallelizable across locations/times

## Technical Challenges Solved

1. **FOV ambiguity**: Focal length insufficient → mandatory sensor dimensions
2. **Detection robustness**: Multi-stage pipeline with fallback strategies
3. **EXIF rotation**: Automatic transpose before processing
4. **Timezone corrections**: Hour angle = f(time, longitude, timezone meridian)
5. **Horizon filtering**: Altitude thresholding with user feedback

## Key Competencies Demonstrated

- Spherical trigonometry, celestial mechanics, coordinate transformations
- Computer vision: blob detection, image processing, camera calibration
- Software architecture: modular design, separation of concerns, testability
- Scientific computing: NumPy vectorization, Astropy ephemeris, scipy algorithms
- Automation: metadata-driven workflows, zero-manual-intervention pipelines
- Documentation: multi-level (README, guides, technical specs, code comments)

## Project Scope

**Code**: ~1,500 lines Python | 4 core + 3 utility modules  
**Docs**: 5 markdown files (~500 lines)  
**Features**: 2 calc modes, 5+ viz types, automated CV pipeline, CLI with 4 subcommands  
**Validation**: 3 real-world datasets, comprehensive test suite
