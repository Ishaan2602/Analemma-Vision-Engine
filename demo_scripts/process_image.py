"""
General Analemma Image Processing Script

Automatically loads image metadata and generates analemma overlay + composite.
Usage: python process_image.py <image_name>
Example: python process_image.py hongkong
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter
from analemma.image_anchor import ImageAnchorer
from analemma.metadata_parser import load_input_image
from PIL import Image
import matplotlib.pyplot as plt


def process_image(image_name: str):
    """Process an input image with automatic metadata loading."""
    
    print("=" * 70)
    print(f"ANALEMMA PROCESSING: {image_name.upper()}")
    print("=" * 70)
    
    # Load metadata
    print("\nStep 1: Loading metadata...")
    try:
        metadata = load_input_image(image_name)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"\nAvailable images:")
        input_dir = Path('input_images')
        if input_dir.exists():
            for subdir in input_dir.iterdir():
                if subdir.is_dir() and (subdir / 'metadata.txt').exists():
                    print(f"  - {subdir.name}")
        return
    
    print(f"  ✓ Image: {metadata['image_file']}")
    print(f"  ✓ Location: {metadata['latitude']:.4f}°, {metadata['longitude']:.4f}°")
    print(f"  ✓ Date/Time: {metadata['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  ✓ Camera: {metadata.get('camera_make', 'Unknown')} {metadata.get('camera_model', '')}")
    
    # Step 2: Create anchorer
    print("\nStep 2: Loading image and detecting sun...")
    anchorer = ImageAnchorer(
        image_path=metadata['image_path'],
        anchor_datetime=metadata['datetime'],
        latitude=metadata['latitude'],
        longitude=metadata['longitude'],
        auto_detect_sun=True
    )
    
    # Calibrate camera
    anchorer.calibrate_from_focal_length(
        focal_length_mm=metadata['focal_length_mm'],
        sensor_width_mm=metadata['sensor_width_mm'],
        sensor_height_mm=metadata['sensor_height_mm']
    )
    
    # Generate overlay
    print("\nStep 3: Generating analemma overlay...")
    output_dir = Path('output') / f'{image_name}_output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    overlay_path = output_dir / f'{image_name}_overlay.png'
    result = anchorer.overlay_analemma(output_path=str(overlay_path))
    
    print(f"  ✓ Sun detected at pixel: {anchorer.sun_pixel}")
    print(f"  ✓ Sun position: Alt={anchorer.anchor_data['altitude']:.1f}°, Az={anchorer.anchor_data['azimuth']:.1f}°")
    print(f"  ✓ Points drawn: {result['points_drawn']} visible, {result['points_filtered']} below horizon")
    
    # Step 4: Generate sky chart
    print("\nStep 4: Generating sky chart...")
    calc = AnalemmaCalculator(mode='approximate', year=metadata['datetime'].year)
    mapper = SkyMapper(latitude=metadata['latitude'], longitude=metadata['longitude'])
    plotter = AnalemmaPlotter()
    
    calc_data = calc.calculate_year(
        hour=metadata['datetime'].hour,
        minute=metadata['datetime'].minute
    )
    sky_data = mapper.map_to_horizon(calc_data)
    
    location_name = metadata.get('location_name', f"{metadata['latitude']:.2f}°, {metadata['longitude']:.2f}°")
    time_str = metadata['datetime'].strftime('%H:%M')
    
    fig = plotter.plot_analemma(sky_data, title=f'Analemma at {location_name} - {time_str}')
    chart_path = output_dir / f'{image_name}_sky_chart.png'
    fig.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ Sky chart saved")
    
    # Step 5: Create composite
    print("\nStep 5: Creating side-by-side composite...")
    overlay_img = Image.open(overlay_path)
    chart_img = Image.open(chart_path)
    
    # Resize chart to match overlay height
    chart_img = chart_img.resize(
        (int(chart_img.width * overlay_img.height / chart_img.height), overlay_img.height),
        Image.Resampling.LANCZOS
    )
    
    # Create composite
    composite = Image.new('RGB', (overlay_img.width + chart_img.width, overlay_img.height), 'white')
    composite.paste(overlay_img, (0, 0))
    composite.paste(chart_img, (overlay_img.width, 0))
    
    composite_path = output_dir / f'{image_name}_composite.png'
    composite.save(composite_path)
    
    print(f"\n{'=' * 70}")
    print("✓ COMPLETE!")
    print(f"{'=' * 70}")
    print(f"\nOutput directory: {output_dir}/")
    print(f"  • {overlay_path.name} - Photo with analemma overlay")
    print(f"  • {chart_path.name} - Sky chart visualization")
    print(f"  • {composite_path.name} - Side-by-side composite")
    print(f"\nComposite size: {composite.size[0]}x{composite.size[1]} pixels\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python process_image.py <image_name>")
        print("\nExample: python process_image.py hongkong")
        print("\nAvailable images:")
        input_dir = Path('input_images')
        if input_dir.exists():
            for subdir in input_dir.iterdir():
                if subdir.is_dir() and (subdir / 'metadata.txt').exists():
                    print(f"  - {subdir.name}")
        sys.exit(1)
    
    image_name = sys.argv[1]
    process_image(image_name)
