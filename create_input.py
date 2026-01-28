#!/usr/bin/env python3
"""
Create New Input Image Directory

Creates a new input directory with template metadata.txt file.
Optionally copies an image file to the directory.

Usage:
    python create_input.py <name>
    python create_input.py <name> --image path/to/photo.jpg
"""

import sys
import argparse
from pathlib import Path
import shutil


METADATA_TEMPLATE = """# {name} Sky Photo - Metadata
# Format: KEY=VALUE (parser reads only this section)

# === REQUIRED METADATA ===
# IMAGE_FILE is optional - will auto-detect image in folder
# IMAGE_FILE=photo.jpg
DATETIME=2024-06-15 14:30:00
LATITUDE=40.1
LONGITUDE=-88.2
FOCAL_LENGTH_MM=5.7
SENSOR_WIDTH_MM=7.8
SENSOR_HEIGHT_MM=5.8

# === OPTIONAL METADATA ===
ALTITUDE_M=200.0
CAMERA_MAKE=
CAMERA_MODEL=
LOCATION_NAME=

# --- REFERENCE DATA (NOT PARSED) ---
# Additional notes, EXIF data, etc.
# Everything below this line is ignored by the parser
#
# Common sensor sizes for reference:
# - iPhone 14/15/16 main: 7.8mm x 5.8mm
# - iPhone 14/15/16 ultrawide: 5.6mm x 4.2mm
# - Full frame DSLR: 36mm x 24mm
# - APS-C DSLR: 23.5mm x 15.6mm
# - Micro 4/3: 17.3mm x 13mm
"""


def create_input_directory(name: str, image_path: str = None):
    """Create a new input directory with template metadata."""
    
    # Create directory
    input_dir = Path('input_images') / name
    
    if input_dir.exists():
        print(f"Error: Directory already exists: {input_dir}")
        return False
    
    input_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created directory: {input_dir}/")
    
    # Create metadata template
    metadata_content = METADATA_TEMPLATE.format(name=name.title())
    metadata_file = input_dir / 'metadata.txt'
    metadata_file.write_text(metadata_content)
    print(f"✓ Created template: {metadata_file}")
    
    # Copy image if provided
    if image_path:
        source = Path(image_path)
        if not source.exists():
            print(f"Warning: Image file not found: {image_path}")
            print("  Skipping image copy")
        else:
            dest = input_dir / source.name
            shutil.copy2(source, dest)
            print(f"✓ Copied image: {dest.name}")
    
    print(f"\nNext steps:")
    print(f"1. Edit {metadata_file} with your photo's metadata")
    if not image_path:
        print(f"2. Copy your image file to {input_dir}/")
        print(f"3. Run: python demo_scripts/process_image.py {name}")
    else:
        print(f"2. Run: python demo_scripts/process_image.py {name}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Create a new input image directory with template metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_input.py myimage
  python create_input.py sunset --image ~/Photos/sunset.jpg
  python create_input.py campus_photo --image /path/to/photo.png
        """
    )
    
    parser.add_argument('name', 
                       help='Name for the new input directory')
    parser.add_argument('--image', '-i',
                       help='Optional: path to image file to copy',
                       default=None)
    
    args = parser.parse_args()
    
    # Validate name
    if not args.name.replace('_', '').replace('-', '').isalnum():
        print(f"Error: Name must contain only letters, numbers, underscores, and hyphens")
        return 1
    
    if not create_input_directory(args.name, args.image):
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
