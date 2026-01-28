"""
Image Overlay Example

Demonstrates the image anchoring feature - overlaying a theoretical
analemma onto a sky photograph.
"""

from datetime import datetime
from PIL import Image, ImageDraw
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analemma.image_anchor import ImageAnchorer


def create_dummy_sky_image(filename: str = "dummy_sky.png"):
    """
    Create a dummy sky image for demonstration purposes.
    
    In real use, this would be a real photograph of the sky.
    """
    # Create a blue gradient sky
    width, height = 1200, 800
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    for y in range(height):
        # Gradient from light blue (top) to darker blue (bottom)
        blue_value = int(135 + (y / height) * 100)
        for x in range(width):
            pixels[x, y] = (100, 150, blue_value)
    
    # Draw some clouds
    draw = ImageDraw.Draw(image)
    for i in range(15):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height // 2)
        size = np.random.randint(50, 150)
        draw.ellipse([x, y, x + size, y + size // 2], 
                    fill=(255, 255, 255, 200))
    
    # Draw sun at center
    sun_x, sun_y = width // 2, height // 2
    sun_radius = 40
    draw.ellipse([sun_x - sun_radius, sun_y - sun_radius,
                 sun_x + sun_radius, sun_y + sun_radius],
                fill=(255, 255, 100))
    
    image.save(filename)
    print(f"Created dummy sky image: {filename}")
    return filename, (sun_x, sun_y)


def main():
    """Demonstrate image anchoring feature."""
    
    print("=" * 70)
    print("Image Anchoring Example - Analemma Overlay on Photograph")
    print("=" * 70)
    print()
    
    # Create a dummy sky image (in practice, use a real photo)
    print("Step 1: Creating dummy sky photograph...")
    image_path, sun_pixel = create_dummy_sky_image("dummy_sky.png")
    
    # Define image metadata
    # In practice, this would come from EXIF data
    anchor_datetime = datetime(2026, 6, 21, 12, 0)  # Summer solstice, noon
    latitude = 40.1  # UIUC
    longitude = -88.2
    
    print(f"  Image size: 1200x800 pixels")
    print(f"  Sun position in image: {sun_pixel}")
    print()
    
    print("Step 2: Initializing image anchorer...")
    print(f"  Anchor date/time: {anchor_datetime}")
    print(f"  Location: {latitude}°N, {abs(longitude)}°W")
    
    anchorer = ImageAnchorer(
        image_path=image_path,
        anchor_datetime=anchor_datetime,
        latitude=latitude,
        longitude=longitude,
        sun_pixel=sun_pixel
    )
    print(f"  ✓ Anchorer initialized: {anchorer}")
    print()
    
    # Calibrate camera (using typical values)
    print("Step 3: Calibrating camera field of view...")
    # Typical values for a wide-angle lens
    focal_length = 24  # mm
    sensor_width = 36  # mm (full frame)
    sensor_height = 24  # mm
    
    anchorer.calibrate_from_focal_length(
        focal_length_mm=focal_length,
        sensor_width_mm=sensor_width,
        sensor_height_mm=sensor_height
    )
    
    h_fov = 2 * np.degrees(np.arctan(sensor_width / (2 * focal_length)))
    v_fov = 2 * np.degrees(np.arctan(sensor_height / (2 * focal_length)))
    
    print(f"  Focal length: {focal_length}mm")
    print(f"  Horizontal FOV: {h_fov:.1f}°")
    print(f"  Vertical FOV: {v_fov:.1f}°")
    print(f"  ✓ Calibration complete")
    print()
    
    # Get statistics
    print("Step 4: Analyzing analemma for this location/time...")
    stats = anchorer.get_statistics()
    
    print(f"  Altitude range: {stats['altitude_range'][0]:.2f}° to "
          f"{stats['altitude_range'][1]:.2f}°")
    print(f"  Azimuth range: {stats['azimuth_range'][0]:.2f}° to "
          f"{stats['azimuth_range'][1]:.2f}°")
    print(f"  Analemma size: {stats['altitude_span']:.2f}° × "
          f"{stats['azimuth_span']:.2f}°")
    print(f"  Anchor position: Alt={stats['anchor_altitude']:.2f}°, "
          f"Az={stats['anchor_azimuth']:.2f}°")
    print()
    
    # Create overlay
    print("Step 5: Overlaying analemma on image...")
    output_image = anchorer.overlay_analemma(
        output_path="output_overlay.png",
        dot_size=8,
        dot_color=(255, 255, 0),
        line_color=(255, 200, 0),
        line_width=3,
        show_dates=True,
        date_interval=30
    )
    
    print("  ✓ Overlay created: output_overlay.png")
    print()
    
    # Create composite visualization
    print("Step 6: Creating composite visualization...")
    fig = anchorer.create_composite_plot("output_composite.png")
    print("  ✓ Composite plot created: output_composite.png")
    print()
    
    print("=" * 70)
    print("✓ Image anchoring demonstration complete!")
    print("=" * 70)
    print("\nOutput files created:")
    print("  1. dummy_sky.png - Simulated sky photograph")
    print("  2. output_overlay.png - Photo with analemma overlay")
    print("  3. output_composite.png - Side-by-side comparison")
    print("\nHow it works:")
    print("  • Calculates true sun position for anchor date/time")
    print("  • Generates full-year analemma at same time each day")
    print("  • Maps sky coordinates to image pixels using camera calibration")
    print("  • Overlays the theoretical curve on the photograph")
    print("\nReal-world usage:")
    print("  • Use actual sky photographs with EXIF metadata")
    print("  • Extract GPS coordinates and timestamp from EXIF")
    print("  • Manually mark sun position if needed")
    print("  • Creates 'AR-style' visualization of sun's yearly path")


if __name__ == "__main__":
    main()
