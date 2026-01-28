#!/usr/bin/env python3
"""
Analemma Engine - Command Line Interface

A CLI tool for calculating and visualizing the analemma.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter
from analemma.image_anchor import ImageAnchorer


def cmd_calculate(args):
    """Calculate analemma for a location."""
    print(f"Calculating analemma for {args.latitude}°, {args.longitude}°")
    print(f"Time: {args.hour:02d}:{args.minute:02d}")
    print(f"Year: {args.year}")
    print(f"Mode: {args.mode}")
    print()
    
    # Initialize components
    calculator = AnalemmaCalculator(mode=args.mode, year=args.year)
    sky_mapper = SkyMapper(args.latitude, args.longitude)
    
    # Calculate
    calc_data = calculator.calculate_year(hour=args.hour, minute=args.minute)
    sky_data = sky_mapper.map_to_horizon(calc_data)
    
    # Print summary statistics
    altitudes = [d['altitude'] for d in sky_data]
    azimuths = [d['azimuth'] for d in sky_data]
    
    print("Analemma Statistics:")
    print(f"  Altitude range: {min(altitudes):.2f}° to {max(altitudes):.2f}°")
    print(f"  Azimuth range: {min(azimuths):.2f}° to {max(azimuths):.2f}°")
    print(f"  Angular size: {max(altitudes)-min(altitudes):.2f}° × {max(azimuths)-min(azimuths):.2f}°")
    print()
    
    # Create visualizations if requested
    if args.plot:
        print("Creating visualizations...")
        plotter = AnalemmaPlotter()
        
        output_dir = Path(args.output) if args.output else Path(".")
        output_dir.mkdir(exist_ok=True)
        
        # Sky chart
        plotter.plot_analemma(
            sky_data,
            title=f"Analemma at {args.latitude}°, {args.longitude}° ({args.hour:02d}:{args.minute:02d})",
            save_path=str(output_dir / "analemma_sky.png")
        )
        
        # Figure-8
        plotter.plot_figure8(
            calc_data,
            save_path=str(output_dir / "analemma_figure8.png")
        )
        
        # Time series
        plotter.plot_time_series(
            calc_data,
            save_path=str(output_dir / "analemma_timeseries.png")
        )
        
        print(f"✓ Plots saved to {output_dir}/")
        
        if args.show:
            plotter.show()


def cmd_compare(args):
    """Compare approximate and high-precision modes."""
    print("Comparing calculation modes...")
    print(f"Location: {args.latitude}°, {args.longitude}°")
    print(f"Year: {args.year}")
    print()
    
    try:
        # Initialize both calculators
        calc_approx = AnalemmaCalculator(mode='approximate', year=args.year)
        calc_precise = AnalemmaCalculator(mode='high-precision', year=args.year)
        
        # Calculate
        approx_data = calc_approx.calculate_year(hour=12, minute=0)
        precise_data = calc_precise.calculate_year(hour=12, minute=0)
        
        # Compute differences
        dec_diffs = [abs(a['declination'] - p['declination']) 
                    for a, p in zip(approx_data, precise_data)]
        eot_diffs = [abs(a['eot'] - p['eot']) 
                    for a, p in zip(approx_data, precise_data)]
        
        print("Declination differences:")
        print(f"  Mean: {sum(dec_diffs)/len(dec_diffs):.4f}°")
        print(f"  Max:  {max(dec_diffs):.4f}°")
        
        print("\nEquation of Time differences:")
        print(f"  Mean: {sum(eot_diffs)/len(eot_diffs):.4f} minutes")
        print(f"  Max:  {max(eot_diffs):.4f} minutes")
        print()
        
        # Create comparison plot if requested
        if args.plot:
            plotter = AnalemmaPlotter()
            output_dir = Path(args.output) if args.output else Path(".")
            output_dir.mkdir(exist_ok=True)
            
            plotter.plot_comparison(
                approx_data,
                precise_data,
                save_path=str(output_dir / "mode_comparison.png")
            )
            
            print(f"✓ Comparison plot saved to {output_dir}/mode_comparison.png")
            
            if args.show:
                plotter.show()
    
    except RuntimeError as e:
        print(f"Error: {e}")
        print("High-precision mode requires astropy.")
        print("Install with: pip install astropy")
        sys.exit(1)


def cmd_anchor(args):
    """Anchor analemma to an image."""
    print("Image Anchoring Mode")
    print(f"Image: {args.image}")
    print(f"Date/Time: {args.datetime}")
    print(f"Location: {args.latitude}°, {args.longitude}°")
    print()
    
    # Parse datetime
    try:
        dt = datetime.fromisoformat(args.datetime)
    except ValueError:
        print("Error: Invalid datetime format. Use ISO format: YYYY-MM-DD HH:MM")
        sys.exit(1)
    
    # Initialize anchorer
    anchorer = ImageAnchorer(
        image_path=args.image,
        anchor_datetime=dt,
        latitude=args.latitude,
        longitude=args.longitude
    )
    
    # Calibrate
    if args.focal_length:
        print(f"Calibrating with focal length: {args.focal_length}mm")
        anchorer.calibrate_from_focal_length(
            focal_length_mm=args.focal_length,
            sensor_width_mm=args.sensor_width,
            sensor_height_mm=args.sensor_height
        )
    elif args.fov:
        h_fov, v_fov = map(float, args.fov.split(','))
        print(f"Calibrating with FOV: {h_fov}° × {v_fov}°")
        anchorer.calibrate_from_field_of_view(h_fov, v_fov)
    else:
        print("Error: Must specify either --focal-length or --fov")
        sys.exit(1)
    
    # Get statistics
    stats = anchorer.get_statistics()
    print(f"\nAnalemma size: {stats['altitude_span']:.2f}° × {stats['azimuth_span']:.2f}°")
    
    # Create overlay
    output_path = args.output or "analemma_overlay.png"
    print(f"\nCreating overlay: {output_path}")
    
    anchorer.overlay_analemma(
        output_path=output_path,
        show_dates=not args.no_dates
    )
    
    print(f"✓ Overlay saved to {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analemma Engine - Calculate and visualize the Sun's analemma",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate analemma for UIUC at noon
  %(prog)s calculate --lat 40.1 --lon -88.2 --hour 12 --plot
  
  # Compare calculation modes
  %(prog)s compare --lat 40.1 --lon -88.2 --plot
  
  # Anchor analemma to an image
  %(prog)s anchor --image sky.jpg --datetime "2026-06-21 12:00" \\
                   --lat 40.1 --lon -88.2 --focal-length 24
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Calculate command
    calc_parser = subparsers.add_parser('calculate', help='Calculate analemma')
    calc_parser.add_argument('--lat', '--latitude', dest='latitude', type=float, required=True,
                           help='Latitude in degrees (positive = North)')
    calc_parser.add_argument('--lon', '--longitude', dest='longitude', type=float, required=True,
                           help='Longitude in degrees (positive = East)')
    calc_parser.add_argument('--hour', type=int, default=12,
                           help='Hour of observation (0-23, default: 12)')
    calc_parser.add_argument('--minute', type=int, default=0,
                           help='Minute of observation (0-59, default: 0)')
    calc_parser.add_argument('--year', type=int, default=datetime.now().year,
                           help='Year for calculation (default: current year)')
    calc_parser.add_argument('--mode', choices=['approximate', 'high-precision'],
                           default='approximate',
                           help='Calculation mode (default: approximate)')
    calc_parser.add_argument('--plot', action='store_true',
                           help='Generate plots')
    calc_parser.add_argument('--show', action='store_true',
                           help='Display plots interactively')
    calc_parser.add_argument('--output', '-o', help='Output directory for plots')
    calc_parser.set_defaults(func=cmd_calculate)
    
    # Compare command
    comp_parser = subparsers.add_parser('compare', help='Compare calculation modes')
    comp_parser.add_argument('--lat', '--latitude', dest='latitude', type=float, required=True,
                           help='Latitude in degrees')
    comp_parser.add_argument('--lon', '--longitude', dest='longitude', type=float, required=True,
                           help='Longitude in degrees')
    comp_parser.add_argument('--year', type=int, default=datetime.now().year,
                           help='Year for calculation')
    comp_parser.add_argument('--plot', action='store_true',
                           help='Generate comparison plots')
    comp_parser.add_argument('--show', action='store_true',
                           help='Display plots interactively')
    comp_parser.add_argument('--output', '-o', help='Output directory for plots')
    comp_parser.set_defaults(func=cmd_compare)
    
    # Anchor command
    anchor_parser = subparsers.add_parser('anchor', help='Anchor analemma to image')
    anchor_parser.add_argument('--image', required=True,
                             help='Path to sky image')
    anchor_parser.add_argument('--datetime', required=True,
                             help='Image date/time (ISO format: YYYY-MM-DD HH:MM)')
    anchor_parser.add_argument('--lat', '--latitude', dest='latitude', type=float, required=True,
                             help='Image location latitude')
    anchor_parser.add_argument('--lon', '--longitude', dest='longitude', type=float, required=True,
                             help='Image location longitude')
    anchor_parser.add_argument('--focal-length', type=float,
                             help='Camera focal length in mm')
    anchor_parser.add_argument('--sensor-width', type=float, default=36.0,
                             help='Sensor width in mm (default: 36)')
    anchor_parser.add_argument('--sensor-height', type=float, default=24.0,
                             help='Sensor height in mm (default: 24)')
    anchor_parser.add_argument('--fov',
                             help='Field of view as "horizontal,vertical" in degrees')
    anchor_parser.add_argument('--no-dates', action='store_true',
                             help='Do not show date labels')
    anchor_parser.add_argument('--output', '-o',
                             help='Output file path (default: analemma_overlay.png)')
    anchor_parser.set_defaults(func=cmd_anchor)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
