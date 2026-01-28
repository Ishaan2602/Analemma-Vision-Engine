"""
Mode Comparison Example

Compare approximate vs high-precision calculation modes to validate accuracy.
"""

from datetime import datetime
from analemma import AnalemmaCalculator, SkyMapper, AnalemmaPlotter


def main():
    """Compare approximate and high-precision modes."""
    
    print("=" * 70)
    print("Mode Comparison - Approximate vs High-Precision")
    print("=" * 70)
    print()
    
    # Check if astropy is available
    try:
        import astropy
        astropy_available = True
    except ImportError:
        astropy_available = False
        print("⚠ Warning: Astropy not installed.")
        print("Install with: pip install astropy")
        print("\nRunning approximate mode only...\n")
    
    # Configuration
    year = 2026
    latitude = 40.1
    longitude = -88.2
    
    # Initialize calculators
    print("Initializing calculators...")
    calc_approx = AnalemmaCalculator(mode='approximate', year=year)
    print(f"  ✓ {calc_approx}")
    
    if astropy_available:
        calc_precise = AnalemmaCalculator(mode='high-precision', year=year)
        print(f"  ✓ {calc_precise}")
    print()
    
    # Calculate for entire year
    print("Calculating for entire year at noon...")
    approx_data = calc_approx.calculate_year(hour=12, minute=0)
    print(f"  ✓ Approximate mode: {len(approx_data)} data points")
    
    if astropy_available:
        precise_data = calc_precise.calculate_year(hour=12, minute=0)
        print(f"  ✓ High-precision mode: {len(precise_data)} data points")
    print()
    
    # Statistical comparison
    if astropy_available:
        print("Statistical Comparison:")
        print("-" * 70)
        
        dec_diffs = [abs(a['declination'] - p['declination']) 
                    for a, p in zip(approx_data, precise_data)]
        eot_diffs = [abs(a['eot'] - p['eot']) 
                    for a, p in zip(approx_data, precise_data)]
        
        print(f"\nDeclination differences:")
        print(f"  Mean: {sum(dec_diffs)/len(dec_diffs):.4f}°")
        print(f"  Max:  {max(dec_diffs):.4f}°")
        print(f"  Min:  {min(dec_diffs):.4f}°")
        
        print(f"\nEquation of Time differences:")
        print(f"  Mean: {sum(eot_diffs)/len(eot_diffs):.4f} minutes")
        print(f"  Max:  {max(eot_diffs):.4f} minutes")
        print(f"  Min:  {min(eot_diffs):.4f} minutes")
        
        # Find worst-case days
        max_dec_idx = dec_diffs.index(max(dec_diffs))
        max_eot_idx = eot_diffs.index(max(eot_diffs))
        
        print(f"\nLargest declination difference:")
        print(f"  Day {approx_data[max_dec_idx]['day_of_year']} "
              f"({approx_data[max_dec_idx]['date'].strftime('%b %d')})")
        print(f"  Approximate: {approx_data[max_dec_idx]['declination']:.4f}°")
        print(f"  Precise:     {precise_data[max_dec_idx]['declination']:.4f}°")
        
        print(f"\nLargest EoT difference:")
        print(f"  Day {approx_data[max_eot_idx]['day_of_year']} "
              f"({approx_data[max_eot_idx]['date'].strftime('%b %d')})")
        print(f"  Approximate: {approx_data[max_eot_idx]['eot']:.4f} min")
        print(f"  Precise:     {precise_data[max_eot_idx]['eot']:.4f} min")
        print()
    
    # Create visualizations
    print("Creating comparison visualizations...")
    plotter = AnalemmaPlotter()
    
    if astropy_available:
        # Comparison plot
        fig1 = plotter.plot_comparison(
            approx_data,
            precise_data,
            save_path="output_mode_comparison.png"
        )
        print("  ✓ Comparison plot saved: output_mode_comparison.png")
        
        # Both modes on same analemma plot
        sky_mapper = SkyMapper(latitude, longitude)
        approx_sky = sky_mapper.map_to_horizon(approx_data)
        precise_sky = sky_mapper.map_to_horizon(precise_data)
        
        fig2 = plotter.plot_analemma(
            approx_sky,
            title=f"Approximate Mode Analemma",
            save_path="output_approx_analemma.png"
        )
        
        fig3 = plotter.plot_analemma(
            precise_sky,
            title=f"High-Precision Mode Analemma",
            save_path="output_precise_analemma.png"
        )
        print("  ✓ Individual analemma plots saved")
        
        # Figure-8 comparison
        fig4 = plotter.plot_figure8(
            approx_data,
            title="Approximate Mode - Figure-8",
            save_path="output_approx_figure8.png"
        )
        
        fig5 = plotter.plot_figure8(
            precise_data,
            title="High-Precision Mode - Figure-8",
            save_path="output_precise_figure8.png"
        )
        print("  ✓ Figure-8 plots saved")
        
    else:
        # Just approximate mode
        sky_mapper = SkyMapper(latitude, longitude)
        approx_sky = sky_mapper.map_to_horizon(approx_data)
        
        fig1 = plotter.plot_analemma(
            approx_sky,
            save_path="output_analemma.png"
        )
        
        fig2 = plotter.plot_figure8(
            approx_data,
            save_path="output_figure8.png"
        )
        print("  ✓ Plots saved (approximate mode only)")
    
    print()
    print("=" * 70)
    if astropy_available:
        print("✓ Mode comparison complete!")
        print("=" * 70)
        print("\nConclusion:")
        print("  The approximate mode provides good qualitative agreement")
        print("  for educational purposes and visualization.")
        print("  Use high-precision mode for scientific accuracy.")
    else:
        print("✓ Approximate mode demonstration complete!")
        print("=" * 70)
        print("\nNote: Install astropy for high-precision mode comparison:")
        print("  pip install astropy")
    
    plotter.show()


if __name__ == "__main__":
    main()
