"""
Unit Tests for Analemma Calculator

Tests the core physics calculations against known values.
"""

import unittest
import sys
import os
from datetime import datetime
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analemma.calculator import AnalemmaCalculator
from analemma.sky_mapper import SkyMapper


class TestAnalemmaCalculator(unittest.TestCase):
    """Test the AnalemmaCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AnalemmaCalculator(mode='approximate', year=2026)
    
    def test_initialization(self):
        """Test calculator initialization."""
        self.assertEqual(self.calc.mode, 'approximate')
        self.assertEqual(self.calc.year, 2026)
        self.assertEqual(self.calc.OBLIQUITY, 23.45)
    
    def test_declination_at_equinoxes(self):
        """Test that declination is ~0 at equinoxes."""
        # Vernal equinox (around day 80-81)
        dec_vernal = self.calc.calculate_declination_approximate(81)
        self.assertAlmostEqual(dec_vernal, 0.0, places=1)
        
        # Autumnal equinox (around day 264-265)
        dec_autumn = self.calc.calculate_declination_approximate(264)
        self.assertAlmostEqual(dec_autumn, 0.0, places=0)
    
    def test_declination_at_solstices(self):
        """Test that declination is ±23.45° at solstices."""
        # Summer solstice (around day 172)
        dec_summer = self.calc.calculate_declination_approximate(172)
        self.assertAlmostEqual(dec_summer, 23.45, delta=1.0)
        
        # Winter solstice (around day 355)
        dec_winter = self.calc.calculate_declination_approximate(355)
        self.assertAlmostEqual(dec_winter, -23.45, delta=1.0)
    
    def test_declination_range(self):
        """Test that declination stays within ±23.45°."""
        for day in range(1, 366):
            dec = self.calc.calculate_declination_approximate(day)
            self.assertLessEqual(abs(dec), 23.5)
    
    def test_equation_of_time_range(self):
        """Test that EoT stays within reasonable bounds (-20 to +20 minutes)."""
        for day in range(1, 366):
            eot = self.calc.calculate_equation_of_time_approximate(day)
            self.assertLessEqual(abs(eot), 20)
    
    def test_calculate_full_year(self):
        """Test calculating full year returns correct number of points."""
        data = self.calc.calculate_year(hour=12, minute=0)
        self.assertEqual(len(data), 365)
        
        # Check data structure
        for point in data[:5]:  # Check first 5 points
            self.assertIn('declination', point)
            self.assertIn('eot', point)
            self.assertIn('day_of_year', point)
            self.assertIn('date', point)
    
    def test_max_declination(self):
        """Test max declination getter."""
        max_dec, min_dec = self.calc.get_max_declination()
        self.assertEqual(max_dec, 23.45)
        self.assertEqual(min_dec, -23.45)


class TestSkyMapper(unittest.TestCase):
    """Test the SkyMapper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mapper = SkyMapper(latitude=40.1, longitude=-88.2)
        self.calc = AnalemmaCalculator(mode='approximate', year=2026)
    
    def test_initialization(self):
        """Test sky mapper initialization."""
        self.assertEqual(self.mapper.latitude, 40.1)
        self.assertEqual(self.mapper.longitude, -88.2)
    
    def test_altitude_at_zenith(self):
        """Test altitude calculation when sun is at zenith."""
        # When declination equals latitude and hour angle is 0,
        # sun should be at maximum altitude
        declination = self.mapper.latitude
        hour_angle = 0
        altitude = self.mapper.calculate_altitude(declination, hour_angle)
        
        # Should be close to 90° (zenith)
        expected = 90
        self.assertAlmostEqual(altitude, expected, places=0)
    
    def test_max_altitude_formula(self):
        """Test maximum altitude formula."""
        # At summer solstice (dec = 23.45) for lat 40.1
        # Max altitude should be 90 - |40.1 - 23.45| = 73.35
        declination = 23.45
        max_alt = self.mapper.calculate_max_altitude(declination)
        expected = 90 - abs(40.1 - 23.45)
        self.assertAlmostEqual(max_alt, expected, places=1)
    
    def test_azimuth_range(self):
        """Test that azimuth is in 0-360 range."""
        data = self.calc.calculate_year(hour=12, minute=0)
        sky_data = self.mapper.map_to_horizon(data)
        
        for point in sky_data:
            azimuth = point['azimuth']
            self.assertGreaterEqual(azimuth, 0)
            self.assertLess(azimuth, 360)
    
    def test_noon_azimuth_northern_hemisphere(self):
        """Test that noon sun is roughly south in Northern hemisphere."""
        # At solar noon, sun should be roughly south (azimuth ~180°)
        data = self.calc.calculate(datetime(2026, 6, 21, 12, 0))
        sky_point = self.mapper.map_single_point(data)
        
        # Should be between 160° and 200° (roughly south)
        azimuth = sky_point['azimuth']
        self.assertGreater(azimuth, 160)
        self.assertLess(azimuth, 200)
    
    def test_map_single_point(self):
        """Test mapping a single calculation result."""
        calc_result = self.calc.calculate(datetime(2026, 1, 1, 12, 0))
        sky_result = self.mapper.map_single_point(calc_result)
        
        # Check all expected keys are present
        self.assertIn('altitude', sky_result)
        self.assertIn('azimuth', sky_result)
        self.assertIn('hour_angle', sky_result)
        self.assertIn('declination', sky_result)
        self.assertIn('eot', sky_result)
    
    def test_altitude_positive_at_noon(self):
        """Test that altitude is positive (above horizon) at noon."""
        data = self.calc.calculate_year(hour=12, minute=0)
        sky_data = self.mapper.map_to_horizon(data)
        
        # All altitudes at noon should be positive
        for point in sky_data:
            self.assertGreater(point['altitude'], 0,
                             f"Negative altitude on day {point['day_of_year']}")


class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline."""
    
    def test_full_pipeline(self):
        """Test complete calculation pipeline."""
        # Initialize all components
        calc = AnalemmaCalculator(mode='approximate', year=2026)
        mapper = SkyMapper(latitude=40.1, longitude=-88.2)
        
        # Calculate full year
        calc_data = calc.calculate_year(hour=12, minute=0, days=365)
        self.assertEqual(len(calc_data), 365)
        
        # Map to horizon
        sky_data = mapper.map_to_horizon(calc_data)
        self.assertEqual(len(sky_data), 365)
        
        # Verify data integrity
        for i, (calc_point, sky_point) in enumerate(zip(calc_data, sky_data)):
            # Same date
            self.assertEqual(calc_point['date'], sky_point['date'])
            
            # Same day of year
            self.assertEqual(calc_point['day_of_year'], sky_point['day_of_year'])
            
            # Sky data includes calc data
            self.assertEqual(calc_point['declination'], sky_point['declination'])
            self.assertEqual(calc_point['eot'], sky_point['eot'])
    
    def test_analemma_shape(self):
        """Test that analemma forms expected figure-8 shape."""
        calc = AnalemmaCalculator(mode='approximate', year=2026)
        data = calc.calculate_year(hour=12, minute=0)
        
        declinations = [d['declination'] for d in data]
        eots = [d['eot'] for d in data]
        
        # Declination should vary sinusoidally (roughly)
        dec_range = max(declinations) - min(declinations)
        self.assertGreater(dec_range, 40)  # Should span ~46° (2 * obliquity)
        
        # EoT should have both positive and negative values
        self.assertGreater(max(eots), 0)
        self.assertLess(min(eots), 0)
        
        # EoT range should be roughly -20 to +20 minutes
        eot_range = max(eots) - min(eots)
        self.assertGreater(eot_range, 20)


def run_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Analemma Engine Tests")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAnalemmaCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestSkyMapper))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
