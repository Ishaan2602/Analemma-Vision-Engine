#!/usr/bin/env python3
"""
Quick Start Script

Run this script to verify the Analemma Engine installation and see it in action.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def main():
    """Run quick start demonstration."""
    
    print_header("ANALEMMA ENGINE - QUICK START")
    
    print("This script demonstrates the basic functionality of the Analemma Engine.")
    print("It will calculate and visualize the analemma for UIUC at noon.\n")
    
    # Configuration
    latitude = 40.1  # Champaign, IL (UIUC)
    longitude = -88.2
    year = 2026
    hour = 12  # Noon
    minute = 0
    
    print(f"Configuration:")
    print(f"  Location: {latitude}°N, {abs(longitude)}°W (UIUC)")
    print(f"  Observation time: {hour:02d}:{minute:02d} local time")
    print(f"  Year: {year}")
    print()
    
    # Step 1: Initialize calculator
    print("Step 1: Initializing calculator...")
    try:
        calculator = AnalemmaCalculator(mode='approximate', year=year)
        print(f"  ✓ Calculator initialized: {calculator}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Step 2: Calculate for entire year
    print("\nStep 2: Calculating solar positions for entire year...")
    try:
        calc_data = calculator.calculate_year(hour=hour, minute=minute)
        print(f"  ✓ Calculated {len(calc_data)} data points")
        
        # Show sample
        sample = calc_data[0]
        print(f"\n  Sample (Jan 1):")
        print(f"    Declination: {sample['declination']:+.2f}°")
        print(f"    Equation of Time: {sample['eot']:+.2f} minutes")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Step 3: Map to horizon coordinates
    print("\nStep 3: Mapping to local horizon coordinates...")
    try:
        sky_mapper = SkyMapper(latitude, longitude)
        sky_data = sky_mapper.map_to_horizon(calc_data)
        print(f"  ✓ Mapped {len(sky_data)} points to local sky")
        
        # Show sample
        sample = sky_data[0]
        print(f"\n  Sample (Jan 1):")
        print(f"    Altitude: {sample['altitude']:.2f}° above horizon")
        print(f"    Azimuth: {sample['azimuth']:.2f}° (from North)")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Step 4: Compute statistics
    print("\nStep 4: Computing analemma statistics...")
    try:
        altitudes = [d['altitude'] for d in sky_data]
        azimuths = [d['azimuth'] for d in sky_data]
        
        print(f"  Altitude range: {min(altitudes):.2f}° to {max(altitudes):.2f}°")
        print(f"  Altitude span: {max(altitudes) - min(altitudes):.2f}°")
        print(f"  Azimuth range: {min(azimuths):.2f}° to {max(azimuths):.2f}°")
        print(f"  Azimuth span: {max(azimuths) - min(azimuths):.2f}°")
        
        # Verify south-facing (northern hemisphere)
        avg_az = sum(azimuths) / len(azimuths)
        if 160 < avg_az < 200:
            print(f"  ✓ Sun correctly positioned to south (avg azimuth: {avg_az:.1f}°)")
        else:
            print(f"  ⚠ Unexpected azimuth: {avg_az:.1f}°")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Step 5: Create visualizations
    print("\nStep 5: Creating visualizations...")
    try:
        plotter = AnalemmaPlotter()
        
        # Create plots
        print("  Creating sky chart...")
        fig1 = plotter.plot_analemma(
            sky_data,
            title=f"Analemma at UIUC - Noon ({year})",
            save_path="output/quickstart_sky_chart.png"
        )
        
        print("  Creating figure-8 plot...")
        fig2 = plotter.plot_figure8(
            calc_data,
            title=f"Analemma Figure-8 ({year})",
            save_path="output/quickstart_figure8.png"
        )
        
        print("  ✓ Visualizations created")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Success!
    print_header("✓ QUICK START COMPLETE!")
    
    print("Output files created:")
    print("  • output/quickstart_sky_chart.png - Analemma in local sky")
    print("  • output/quickstart_figure8.png - Classic figure-8 plot")
    print()
    print("Next steps:")
    print("  1. Check the example scripts in examples/")
    print("  2. Read USAGE_GUIDE.md for detailed documentation")
    print("  3. Try different locations and times of day")
    print("  4. Explore the CLI: python analemma_cli.py --help")
    print()
    print("Displaying plots...")
    
    try:
        plotter.show()
    except KeyboardInterrupt:
        print("\nPlot display cancelled.")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nQuick start interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
