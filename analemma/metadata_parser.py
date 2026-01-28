"""Utility to parse metadata.txt files for automatic processing."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def parse_metadata(metadata_path: str) -> Dict[str, Any]:
    """
    Parse a metadata.txt file and return structured data.
    
    Only parses KEY=VALUE pairs before the separator line.
    Stops at: # --- REFERENCE DATA (NOT PARSED) ---
    
    Parameters
    ----------
    metadata_path : str
        Path to metadata.txt file
        
    Returns
    -------
    dict
        Parsed metadata with keys:
        - image_file, datetime, latitude, longitude
        - focal_length_mm, sensor_width_mm, sensor_height_mm
        - Optional: altitude_m, camera_make, camera_model, location_name
    """
    metadata = {}
    
    with open(metadata_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Stop at separator - don't parse reference data
            if '--- REFERENCE DATA' in line or '--- ADDITIONAL METADATA' in line:
                break
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                
                # Type conversion
                if key in ['latitude', 'longitude', 'altitude_m', 
                          'focal_length_mm', 'sensor_width_mm', 'sensor_height_mm']:
                    metadata[key] = float(value)
                elif key == 'datetime':
                    metadata[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                else:
                    metadata[key] = value
    
    return metadata


def load_input_image(image_name: str) -> Dict[str, Any]:
    """
    Load an input image and its metadata.
    
    Automatically detects image file in the directory if not specified in metadata.
    
    Parameters
    ----------
    image_name : str
        Name of the image folder (e.g., 'hongkong', 'nigeria')
        
    Returns
    -------
    dict
        Complete metadata including full image path
    """
    base_path = Path('input_images') / image_name
    metadata_file = base_path / 'metadata.txt'
    
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    
    metadata = parse_metadata(str(metadata_file))
    
    # Auto-detect image file if not specified in metadata
    image_file = metadata.get('image_file')
    
    if not image_file:
        # Look for image files in the directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(list(base_path.glob(f'*{ext}')))
            image_files.extend(list(base_path.glob(f'*{ext.upper()}')))
        
        if len(image_files) == 0:
            raise FileNotFoundError(f"No image file found in {base_path}")
        elif len(image_files) > 1:
            # Use the first one but warn
            print(f"Warning: Multiple image files found in {base_path}, using {image_files[0].name}")
            image_file = image_files[0].name
        else:
            image_file = image_files[0].name
        
        metadata['image_file'] = image_file
    
    # Add full image path
    metadata['image_path'] = str(base_path / image_file)
    
    return metadata


if __name__ == '__main__':
    # Test the parser
    import sys
    
    if len(sys.argv) > 1:
        image_name = sys.argv[1]
    else:
        image_name = 'hongkong'
    
    print(f"Loading metadata for: {image_name}")
    print("-" * 60)
    
    try:
        data = load_input_image(image_name)
        for key, value in data.items():
            print(f"{key:20s}: {value}")
    except Exception as e:
        print(f"Error: {e}")
