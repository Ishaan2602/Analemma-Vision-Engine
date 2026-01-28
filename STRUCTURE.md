# Analemma Project - Directory Organization

## Clean Project Structure

```
analemma_project/
├── README.md                  # Main documentation
├── USAGE_GUIDE.md            # User guide
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── analemma_cli.py          # Command-line interface
│
├── analemma/                # Core engine modules
│   ├── __init__.py
│   ├── calculator.py        # Solar position calculations
│   ├── sky_mapper.py        # Coordinate transformations
│   ├── plotter.py           # Visualization engine
│   ├── image_anchor.py      # Image overlay (CV-based)
│   └── metadata_parser.py   # Auto-parse metadata files
│
├── input_images/            # Organized input photos
│   ├── hongkong/
│   │   ├── hongkong_img.jpeg
│   │   └── metadata.txt     # Auto-parseable KEY=VALUE format
│   ├── nigeria/
│   │   ├── nigeria_img.jpg
│   │   └── metadata.txt
│   └── dummy/
│       ├── dummy_sky.png
│       └── metadata.txt
│
├── examples/                # Example scripts
│   ├── basic_plot.py
│   ├── uiuc_noon.py
│   ├── image_overlay.py
│   └── mode_comparison.py
│
├── demo_scripts/            # Quick demos
│   ├── README.md
│   ├── process_image.py     # MAIN: Auto-process any image
│   ├── quickstart.py        # Basic demo
│   ├── test_hongkong.py     # Legacy
│   ├── test_nigeria.py      # Legacy
│   └── show_detection.py    # Sun detection viz
│
├── tests/                   # Unit tests
│   └── test_calculator.py
│
└── output/                  # Generated files (organized)
    ├── README.md
    ├── hongkong_output/     # All hongkong outputs
    ├── nigeria_output/      # All nigeria outputs
    ├── quickstart_output/   # Quickstart outputs
    └── visualizations/      # General visualizations
```

## Key Files

### Documentation
- **README.md** - Quick start and overview
- **USAGE_GUIDE.md** - Comprehensive usage examples

### Core Engine
- **calculator.py** - Solar declination and equation of time
- **sky_mapper.py** - Celestial to horizon coordinate transformation
- **plotter.py** - All visualization types
- **image_anchor.py** - Photo overlay with computer vision sun detection

### Getting Started
1. Run `python demo_scripts/quickstart.py` - Basic demo
2. Run `python demo_scripts/process_image.py hongkong` - Image anchoring demo
3. Add your own images to `input_images/yourname/` with metadata.txt
4. Check `examples/` for more detailed examples
5. Use `python analemma_cli.py --help` for CLI usage

## Features Implemented

✅ Dual precision modes (approximate & high-precision)
✅ Multiple visualization types (6+ plot styles)
✅ Image anchoring with automatic sun detection
✅ Computer vision using scipy blob detection
✅ Command-line interface
✅ Comprehensive documentation
✅ Unit tests
✅ Example scripts

## Recent Updates

- Organized output files into `output/` directory
- Moved demo scripts to `demo_scripts/` directory
- Added `.gitignore` for clean version control
- Updated all paths in scripts
- Added README files to subdirectories
- Improved sun detection algorithm (scipy-based)
