"""Diagnostic visualization showing sun detection."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from analemma.image_anchor import ImageAnchorer
from PIL import Image, ImageDraw

# Create anchorer
anchorer = ImageAnchorer(
    image_path="output/hongkong_img.jpeg",
    anchor_datetime=datetime(2014, 9, 2, 16, 20, 48),
    latitude=22.3,
    longitude=114.2,
    auto_detect_sun=True
)

print(f"Sun auto-detected at: {anchorer.sun_pixel}")
print(f"Calculated sun position: Alt={anchorer.anchor_data['altitude']:.2f}°, Az={anchorer.anchor_data['azimuth']:.2f}°")

# Create diagnostic image showing detection
img = anchorer.image.copy()
draw = ImageDraw.Draw(img)

# Draw large red circle at detected sun
sun_x, sun_y = anchorer.sun_pixel
radius = 50
draw.ellipse([sun_x - radius, sun_y - radius, sun_x + radius, sun_y + radius],
             outline=(255, 0, 0), width=5)

# Add crosshair
draw.line([(sun_x - radius - 20, sun_y), (sun_x + radius + 20, sun_y)], fill=(255, 0, 0), width=3)
draw.line([(sun_x, sun_y - radius - 20), (sun_x, sun_y + radius + 20)], fill=(255, 0, 0), width=3)

# Add text
draw.text((sun_x + radius + 30, sun_y), 
          f"Auto-detected\nSun Position\n({sun_x}, {sun_y})", 
          fill=(255, 255, 0))

img.save("output/hongkong_detection.png")
print("\nDetection visualization saved to: output/hongkong_detection.png")
