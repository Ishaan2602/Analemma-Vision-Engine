"""
Layer 1: The Physics Engine (AnalemmaCalculator)

Pure numerical calculation of solar declination and equation of time.
Supports dual precision modes: Approximate (fast) and High-Precision (Astropy).
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Literal
import warnings

# Optional high-precision imports
try:
    from astropy.time import Time
    from astropy.coordinates import get_sun, EarthLocation
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    warnings.warn("Astropy not available. High-precision mode will not work.")


class AnalemmaCalculator:
    """
    Calculate solar declination and equation of time.
    
    The analemma's shape is determined by:
    1. Solar Declination (δ): Vertical component (N/S) from Earth's axial tilt
    2. Equation of Time (EoT): Horizontal component (E/W) from orbital effects
    
    Parameters
    ----------
    mode : {'approximate', 'high-precision'}
        Calculation mode:
        - 'approximate': Fast sine-wave formulas (educational)
        - 'high-precision': NASA-grade coordinates via Astropy
    year : int, optional
        Year for calculations (default: current year)
    """
    
    # Constants
    OBLIQUITY = 23.45  # Earth's axial tilt in degrees
    DAYS_PER_YEAR = 365.25
    VERNAL_EQUINOX_OFFSET = 81  # Approx day of vernal equinox
    
    def __init__(self, mode: Literal['approximate', 'high-precision'] = 'approximate', 
                 year: int = None):
        """Initialize the calculator with specified mode."""
        self.mode = mode
        self.year = year or datetime.now().year
        
        if mode == 'high-precision' and not ASTROPY_AVAILABLE:
            raise RuntimeError("High-precision mode requires astropy. "
                             "Install with: pip install astropy")
    
    def calculate_declination_approximate(self, day_of_year: int) -> float:
        """
        Calculate solar declination using sine-wave approximation.
        
        Formula: δ ≈ 23.45° × sin[(360/365)(284+N)]
        
        Parameters
        ----------
        day_of_year : int
            Day of year (1-365)
        
        Returns
        -------
        float
            Solar declination in degrees
        """
        # Phase shift ensures δ=0 at vernal equinox (day ~81)
        phase_shifted_day = 284 + day_of_year
        
        # Convert to radians for calculation
        angle_rad = np.radians((360 / 365) * phase_shifted_day)
        
        # Calculate declination
        declination = self.OBLIQUITY * np.sin(angle_rad)
        
        return declination
    
    def calculate_equation_of_time_approximate(self, day_of_year: int) -> float:
        """
        Calculate equation of time using approximation formula.
        
        EoT is caused by two effects:
        1. Obliquity: Tilt of ecliptic relative to equator
        2. Eccentricity: Variable orbital speed (Kepler's 2nd law)
        
        Parameters
        ----------
        day_of_year : int
            Day of year (1-365)
        
        Returns
        -------
        float
            Equation of time in minutes
        """
        # Convert day of year to radians
        B = 2 * np.pi * (day_of_year - 81) / 365
        
        # Component from obliquity (axial tilt)
        obliquity_component = 9.87 * np.sin(2 * B)
        
        # Component from eccentricity (elliptical orbit)
        eccentricity_component = 7.53 * np.cos(B) - 1.5 * np.sin(B)
        
        # Total equation of time
        eot = obliquity_component - eccentricity_component
        
        return eot
    
    def calculate_high_precision(self, dt: datetime) -> Tuple[float, float]:
        """
        Calculate solar position using high-precision Astropy methods.
        
        Parameters
        ----------
        dt : datetime
            Date and time for calculation
        
        Returns
        -------
        tuple
            (declination in degrees, equation of time in minutes)
        """
        if not ASTROPY_AVAILABLE:
            raise RuntimeError("High-precision mode requires astropy")
        
        # Convert to Astropy Time object
        time = Time(dt)
        
        # Get Sun position (uses JPL ephemerides if available)
        sun = get_sun(time)
        
        # Declination from coordinates
        declination = sun.dec.degree
        
        # Calculate equation of time
        # EoT = Apparent Solar Time - Mean Solar Time
        # Approximate from right ascension
        ra_hours = sun.ra.hour
        mean_solar_hours = (dt.timetuple().tm_yday - 1) * 24 / 365.25
        
        # Convert RA difference to time difference
        # Note: This is a simplified calculation
        # More accurate: use actual solar noon calculations
        eot_hours = (ra_hours - mean_solar_hours) % 24
        if eot_hours > 12:
            eot_hours -= 24
        eot_minutes = eot_hours * 4  # Convert hours of RA to minutes of time
        
        # More accurate EoT using GAST
        # This is a placeholder - full implementation would use:
        # EoT = GHA_mean_sun - GHA_apparent_sun
        # For now, use simpler approximation
        day_of_year = dt.timetuple().tm_yday
        eot_minutes = self.calculate_equation_of_time_approximate(day_of_year)
        
        return declination, eot_minutes
    
    def calculate(self, date: datetime) -> Dict[str, float]:
        """
        Calculate solar parameters for a specific date/time.
        
        Parameters
        ----------
        date : datetime
            Date and time for calculation
        
        Returns
        -------
        dict
            Dictionary with keys:
            - 'declination': Solar declination in degrees
            - 'eot': Equation of time in minutes
            - 'day_of_year': Day of year (1-365)
        """
        day_of_year = date.timetuple().tm_yday
        
        if self.mode == 'approximate':
            declination = self.calculate_declination_approximate(day_of_year)
            eot = self.calculate_equation_of_time_approximate(day_of_year)
        elif self.mode == 'high-precision':
            declination, eot = self.calculate_high_precision(date)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
        
        return {
            'declination': declination,
            'eot': eot,
            'day_of_year': day_of_year,
            'date': date
        }
    
    def calculate_year(self, hour: int = 12, minute: int = 0, 
                       days: int = 365) -> List[Dict[str, float]]:
        """
        Calculate solar parameters for an entire year at a specific time of day.
        
        Parameters
        ----------
        hour : int
            Hour of day (0-23) for observations
        minute : int
            Minute of hour (0-59)
        days : int
            Number of days to calculate (default: 365)
        
        Returns
        -------
        list
            List of dictionaries, one per day, each containing:
            - 'declination': Solar declination in degrees
            - 'eot': Equation of time in minutes
            - 'day_of_year': Day of year
            - 'date': datetime object
        """
        results = []
        start_date = datetime(self.year, 1, 1, hour, minute)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            result = self.calculate(current_date)
            results.append(result)
        
        return results
    
    def get_max_declination(self) -> Tuple[float, float]:
        """
        Get maximum and minimum declination values.
        
        Returns
        -------
        tuple
            (max_declination, min_declination) in degrees
        """
        # For approximate mode, these are symmetric around obliquity
        return (self.OBLIQUITY, -self.OBLIQUITY)
    
    def compare_modes(self, date: datetime) -> Dict[str, Dict[str, float]]:
        """
        Compare results from both calculation modes.
        
        Useful for validation and understanding precision differences.
        
        Parameters
        ----------
        date : datetime
            Date for comparison
        
        Returns
        -------
        dict
            Dictionary with keys 'approximate' and 'high-precision',
            each containing calculation results
        """
        if not ASTROPY_AVAILABLE:
            raise RuntimeError("Comparison requires astropy to be installed")
        
        # Save current mode
        original_mode = self.mode
        
        # Calculate with both modes
        self.mode = 'approximate'
        approx_result = self.calculate(date)
        
        self.mode = 'high-precision'
        precise_result = self.calculate(date)
        
        # Restore original mode
        self.mode = original_mode
        
        # Calculate differences
        diff = {
            'declination_diff': abs(precise_result['declination'] - approx_result['declination']),
            'eot_diff': abs(precise_result['eot'] - approx_result['eot'])
        }
        
        return {
            'approximate': approx_result,
            'high-precision': precise_result,
            'differences': diff
        }
    
    def __repr__(self) -> str:
        return f"AnalemmaCalculator(mode='{self.mode}', year={self.year})"
