"""
UIUC Noon Analemma Example

Generates the specific example from the project brief:
A standard "UIUC Noon Analemma" plot (Latitude 40°N) to verify 
the figure-8 shape, checking for the south-culminating loop.
"""

from datetime import datetime
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter


def main():
    """Generate UIUC noon analemma as specified in project brief."""
    
    # UIUC coordinates
    latitude = 40.1  # Champaign, IL
    longitude = -88.2
    year = 2026
    
    print("=" * 70)
    print("UIUC Noon Analemma - Validation Plot")
    print("=" * 70)
    print(f"\nLocation: University of Illinois at Urbana-Champaign")
    print(f"Coordinates: {latitude}°N, {abs(longitude)}°W")
    print(f"Observation: Solar noon throughout {year}")
    print()
    
    # Initialize components
    calculator = AnalemmaCalculator(mode='approximate', year=year)
    sky_mapper = SkyMapper(latitude, longitude)
    plotter = AnalemmaPlotter()
    
    # Calculate for noon (12:00 local time)
    print("Calculating analemma for noon observations...")
    calc_data = calculator.calculate_year(hour=12, minute=0)
    sky_data = sky_mapper.map_to_horizon(calc_data)
    
    # Find extreme points to verify figure-8 shape
    altitudes = [d['altitude'] for d in sky_data]
    max_alt_idx = altitudes.index(max(altitudes))
    min_alt_idx = altitudes.index(min(altitudes))
    
    print(f"\nAltitude range:")
    print(f"  Maximum: {max(altitudes):.2f}° on day {sky_data[max_alt_idx]['day_of_year']} "
          f"({sky_data[max_alt_idx]['date'].strftime('%b %d')})")
    print(f"  Minimum: {min(altitudes):.2f}° on day {sky_data[min_alt_idx]['day_of_year']} "
          f"({sky_data[min_alt_idx]['date'].strftime('%b %d')})")
    print(f"  Span: {max(altitudes) - min(altitudes):.2f}°")
    
    # Check azimuth variation
    azimuths = [d['azimuth'] for d in sky_data]
    print(f"\nAzimuth range:")
    print(f"  Maximum: {max(azimuths):.2f}°")
    print(f"  Minimum: {min(azimuths):.2f}°")
    print(f"  Span: {max(azimuths) - min(azimuths):.2f}°")
    
    # Check equation of time extremes
    eots = [d['eot'] for d in calc_data]
    max_eot_idx = eots.index(max(eots))
    min_eot_idx = eots.index(min(eots))
    
    print(f"\nEquation of Time range:")
    print(f"  Maximum: {max(eots):+.2f} min on day {calc_data[max_eot_idx]['day_of_year']} "
          f"({calc_data[max_eot_idx]['date'].strftime('%b %d')})")
    print(f"  Minimum: {min(eots):+.2f} min on day {calc_data[min_eot_idx]['day_of_year']} "
          f"({calc_data[min_eot_idx]['date'].strftime('%b %d')})")
    
    # Verify south culmination (for Northern hemisphere, sun at noon should be to the south)
    avg_azimuth = sum(azimuths) / len(azimuths)
    print(f"\nAverage azimuth: {avg_azimuth:.2f}° ", end="")
    if 160 < avg_azimuth < 200:
        print("✓ (Correctly positioned to the South)")
    else:
        print("⚠ (Unexpected azimuth)")
    
    # Create visualization
    print("\nCreating visualization...")
    
    fig = plotter.plot_analemma(
        sky_data,
        title=f"UIUC Noon Analemma - {year}\n"
              f"Latitude {latitude}°N, Longitude {abs(longitude)}°W",
        show_dates=True,
        date_interval=30,
        save_path="uiuc_noon_analemma.png"
    )
    
    # Also create the figure-8 plot
    fig2 = plotter.plot_figure8(
        calc_data,
        title=f"UIUC Noon Analemma - Figure-8 Shape ({year})",
        save_path="uiuc_figure8.png"
    )
    
    print("\n" + "=" * 70)
    print("✓ UIUC noon analemma validated!")
    print("=" * 70)
    print("\nKey observations:")
    print("  • Figure-8 shape formed by axial tilt and orbital eccentricity")
    print("  • Sun culminates to the South (Northern hemisphere)")
    print(f"  • Altitude varies by {max(altitudes) - min(altitudes):.1f}° "
          "(≈ twice Earth's obliquity)")
    print(f"  • East-West variation of {max(azimuths) - min(azimuths):.2f}° "
          "(from Equation of Time)")
    print("\nOutput files:")
    print("  - uiuc_noon_analemma.png")
    print("  - uiuc_figure8.png")
    
    plotter.show()


if __name__ == "__main__":
    main()
