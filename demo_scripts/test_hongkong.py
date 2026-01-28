"""Quick test of Hong Kong image anchoring with auto sun detection."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from analemma.image_anchor import ImageAnchorer

# Create anchorer with auto sun detection
anchorer = ImageAnchorer(
    image_path="output/hongkong_img.jpeg",
    anchor_datetime=datetime(2014, 9, 2, 16, 20, 48),
    latitude=22.3,
    longitude=114.2,
    auto_detect_sun=True
)

# Calibrate using smartphone camera specs
anchorer.calibrate_from_focal_length(
    focal_length_mm=6.1,
    sensor_width_mm=6.2,
    sensor_height_mm=4.6
)

# Generate and overlay analemma
output_path = "output/hongkong_final.png"
result = anchorer.overlay_analemma(output_path=output_path)

print(f"\nAnalemma overlay saved to: {output_path}")
print(f"Sun detected at pixel: {anchorer.sun_pixel}")
print(f"Sun position: Alt={anchorer.anchor_data['altitude']:.1f}°, Az={anchorer.anchor_data['azimuth']:.1f}°")
print(f"Points drawn: {result['points_drawn']} visible, {result['points_filtered']} below horizon")
