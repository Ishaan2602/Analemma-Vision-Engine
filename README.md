# Analemma Vision Engine

I built a dynamic python-based toolkit to calculate and visualize the Sun's analemma - the figure-8 path traced when the Sun is photographed at the same time each day throughout a year - for **real sky photos**.

## Overview

This is both a **mathematical** and **computer vision** problem. The analemma's figure-8 shape comes from Earth's axial tilt and elliptical orbit. This project calculates the theoretical path (orbital mechanics, coordinate transforms) and overlays it onto real sky photos using automatic sun detection (scipy blob detection, brightness analysis).

## Installation

```bash
git clone https://github.com/yourusername/analemma_project.git
cd analemma_project
pip install -r requirements.txt
```

## Usage

**Process a sky photo:**
```bash
python create_input.py myimage --image path/to/photo.jpg
# Edit input_images/myimage/metadata.txt with location, datetime, camera specs
python demo_scripts/process_image.py myimage
```

**Python API:**
```python
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter

calculator = AnalemmaCalculator(mode='approximate')
sky_mapper = SkyMapper(latitude=40.1, longitude=-88.2)
plotter = AnalemmaPlotter()

calc_data = calculator.calculate_year(hour=12, minute=0)
sky_data = sky_mapper.map_to_horizon(calc_data)
plotter.plot_analemma(sky_data)
plotter.show()
```

## Files

- `analemma/` - Core calculation/visualization modules
- `create_input.py` - Setup new input folders
- `demo_scripts/process_image.py` - Main processing script
- `analemma_cli.py` - Command line interface
- `examples/` - Example usage scripts

## Notes

The image overlay uses a simplified pinhole camera model. Real smartphone cameras have lens distortion that causes slight inaccuracies near image edges. See [USAGE_GUIDE.md](USAGE_GUIDE.md) for details.



