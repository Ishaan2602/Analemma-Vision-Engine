"""
Basic Analemma Plot Example

This script demonstrates basic usage of the Analemma Engine to calculate
and visualize the analemma for a specific location.
"""

from datetime import datetime
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter


def main():
    """Generate basic analemma plots for a location."""
    
    # Configuration
    latitude = 40.1  # Champaign, IL (UIUC)
    longitude = -88.2
    year = 2026
    observation_hour = 12  # Noon
    observation_minute = 0
    
    print("=" * 60)
    print("Analemma Engine - Basic Example")
    print("=" * 60)
    print(f"\nLocation: {latitude}°N, {abs(longitude)}°W")
    print(f"Observation time: {observation_hour:02d}:{observation_minute:02d} local time")
    print(f"Year: {year}\n")
    
    # Step 1: Initialize calculator
    print("Step 1: Initializing calculator (approximate mode)...")
    calculator = AnalemmaCalculator(mode='approximate', year=year)
    
    # Step 2: Calculate for entire year
    print("Step 2: Calculating solar positions for entire year...")
    calc_data = calculator.calculate_year(
        hour=observation_hour,
        minute=observation_minute
    )
    
    print(f"  ✓ Calculated {len(calc_data)} data points")
    
    # Display some sample data
    print("\nSample data (first 3 days):")
    for i, data in enumerate(calc_data[:3]):
        print(f"  Day {data['day_of_year']}: "
              f"Declination={data['declination']:+.2f}°, "
              f"EoT={data['eot']:+.2f} min")
    
    # Step 3: Map to horizon coordinates
    print("\nStep 3: Mapping to horizon coordinates...")
    sky_mapper = SkyMapper(latitude, longitude)
    sky_data = sky_mapper.map_to_horizon(calc_data)
    
    print(f"  ✓ Mapped {len(sky_data)} points to local sky")
    print(f"  Observer location: {sky_mapper}")
    
    # Display some sky coordinates
    print("\nSample sky coordinates (first 3 days):")
    for i, data in enumerate(sky_data[:3]):
        print(f"  Day {data['day_of_year']}: "
              f"Altitude={data['altitude']:.2f}°, "
              f"Azimuth={data['azimuth']:.2f}°")
    
    # Step 4: Create visualizations
    print("\nStep 4: Creating visualizations...")
    plotter = AnalemmaPlotter()
    
    # Plot 1: Sky chart (Altitude vs Azimuth)
    print("  - Creating sky chart...")
    fig1 = plotter.plot_analemma(
        sky_data,
        title=f"Analemma at {latitude}°N, {abs(longitude)}°W "
              f"({observation_hour:02d}:{observation_minute:02d})",
        save_path="output_sky_chart.png"
    )
    
    # Plot 2: Figure-8 (EoT vs Declination)
    print("  - Creating figure-8 plot...")
    fig2 = plotter.plot_figure8(
        calc_data,
        save_path="output_figure8.png"
    )
    
    # Plot 3: Time series
    print("  - Creating time series plot...")
    fig3 = plotter.plot_time_series(
        calc_data,
        save_path="output_timeseries.png"
    )
    
    # Plot 4: Sky dome
    print("  - Creating sky dome plot...")
    fig4 = plotter.plot_sky_dome(
        sky_data,
        save_path="output_skydome.png"
    )
    
    print("\n" + "=" * 60)
    print("✓ All plots created successfully!")
    print("=" * 60)
    print("\nOutput files:")
    print("  - output_sky_chart.png")
    print("  - output_figure8.png")
    print("  - output_timeseries.png")
    print("  - output_skydome.png")
    print("\nDisplaying plots...")
    
    # Display all plots
    plotter.show()


if __name__ == "__main__":
    main()
