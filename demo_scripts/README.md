# Demo Scripts

Quick demonstration and testing scripts for the Analemma Engine.

## Scripts

### process_image.py (Recommended)
**General-purpose image processor** - automatically loads metadata and generates all outputs.

```bash
python demo_scripts/process_image.py <image_name>

# Examples:
python demo_scripts/process_image.py hongkong
python demo_scripts/process_image.py nigeria
```

### quickstart.py
Basic demo showing analemma calculation and visualization for UIUC campus.

```bash
python demo_scripts/quickstart.py
```

### show_detection.py
Visualizes the computer vision sun detection algorithm.

```bash
python demo_scripts/show_detection.py <image_name>
```

## Legacy Scripts

### test_hongkong.py, test_nigeria.py
Image-specific processing scripts (use `process_image.py` instead for new images).

## Output

All scripts save their output to organized subdirectories in `output/`.
