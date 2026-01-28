"""Generate Nigeria analemma composite."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter
from analemma.image_anchor import ImageAnchorer
from PIL import Image
import matplotlib.pyplot as plt

# Nigeria photo metadata
image_path = "input_images/nigeria/nigeria_img.jpg"
photo_datetime = datetime(2025, 1, 19, 17, 47, 17)
latitude = 9.766100  # 9° 45′ 57.96″ N
longitude = 8.278986  # 8° 16′ 44.35″ E

# iPhone 14 Plus main camera specs
focal_length = 5.7  # mm
sensor_width = 7.8  # mm
sensor_height = 5.8  # mm

print("=" * 70)
print("NIGERIA ANALEMMA - Generating Composite")
print("=" * 70)
print(f"\nLocation: {latitude:.4f}°N, {longitude:.4f}°E")
print(f"Date/Time: {photo_datetime.strftime('%B %d, %Y at %H:%M:%S')}")
print(f"Camera: iPhone 14 Plus ({focal_length}mm, {sensor_width}x{sensor_height}mm sensor)")

# Step 1: Create anchorer with auto sun detection
print("\nStep 1: Loading image and detecting sun...")
anchorer = ImageAnchorer(
    image_path=image_path,
    anchor_datetime=photo_datetime,
    latitude=latitude,
    longitude=longitude,
    auto_detect_sun=True
)

# Calibrate camera
anchorer.calibrate_from_focal_length(
    focal_length_mm=focal_length,
    sensor_width_mm=sensor_width,
    sensor_height_mm=sensor_height
)

# Generate overlay
print("\nStep 2: Generating analemma overlay...")
overlay_path = "output/nigeria_final.png"
result = anchorer.overlay_analemma(output_path=overlay_path)

print(f"  ✓ Sun detected at pixel: {anchorer.sun_pixel}")
print(f"  ✓ Sun position: Alt={anchorer.anchor_data['altitude']:.1f}°, Az={anchorer.anchor_data['azimuth']:.1f}°")
print(f"  ✓ Points drawn: {result['points_drawn']} visible, {result['points_filtered']} below horizon")

# Step 3: Generate sky chart
print("\nStep 3: Generating sky chart...")
calc = AnalemmaCalculator(mode='approximate', year=2025)
mapper = SkyMapper(latitude=latitude, longitude=longitude)
plotter = AnalemmaPlotter()

calc_data = calc.calculate_year(hour=17, minute=47)
sky_data = mapper.map_to_horizon(calc_data)

fig = plotter.plot_analemma(sky_data, title='Nigeria Analemma - 5:47 PM')
chart_path = "output/nigeria_sky_chart.png"
fig.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  ✓ Sky chart saved")

# Step 4: Create composite
print("\nStep 4: Creating side-by-side composite...")
overlay = Image.open(overlay_path)
chart = Image.open(chart_path)

# Resize chart to match overlay height
chart = chart.resize((int(chart.width * overlay.height / chart.height), overlay.height), Image.Resampling.LANCZOS)

# Create composite
composite = Image.new('RGB', (overlay.width + chart.width, overlay.height), 'white')
composite.paste(overlay, (0, 0))
composite.paste(chart, (overlay.width, 0))

composite_path = "output/nigeria_composite.png"
composite.save(composite_path)

print(f"\n{'=' * 70}")
print("✓ COMPLETE!")
print(f"{'=' * 70}")
print(f"\nOutput files:")
print(f"  • {overlay_path} - Photo with analemma overlay")
print(f"  • {chart_path} - Sky chart visualization")
print(f"  • {composite_path} - Side-by-side composite")
print(f"\nComposite size: {composite.size[0]}x{composite.size[1]} pixels\n")
