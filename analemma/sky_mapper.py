"""
Layer 2: The Sky Projector (SkyMapper)

Transforms celestial coordinates (declination, equation of time) into
local horizon coordinates (altitude, azimuth) for a specific observer location.
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timezone


class SkyMapper:
    """
    Convert solar coordinates to local horizon coordinates.
    
    Transforms the output from AnalemmaCalculator (declination, EoT) into
    altitude and azimuth as seen from a specific observer's location.
    
    Parameters
    ----------
    latitude : float
        Observer's latitude in degrees (positive = North, negative = South)
    longitude : float
        Observer's longitude in degrees (positive = East, negative = West)
    timezone_offset : float, optional
        Timezone offset from UTC in hours (e.g., -6 for CST, -5 for EST)
        If None, will be calculated from longitude
    """
    
    def __init__(self, latitude: float, longitude: float, 
                 timezone_offset: float = None):
        """Initialize sky mapper with observer location."""
        self.latitude = latitude
        self.longitude = longitude
        
        # Calculate timezone offset from longitude if not provided
        # Standard time zones are roughly 15° apart (360°/24h = 15°/h)
        if timezone_offset is None:
            self.timezone_offset = round(longitude / 15)
        else:
            self.timezone_offset = timezone_offset
        
        # Convert latitude to radians for calculations
        self.latitude_rad = np.radians(latitude)
    
    def equation_of_time_to_hour_angle(self, eot_minutes: float, 
                                       hour: int, minute: int,
                                       longitude: float = None) -> float:
        """
        Convert equation of time to local hour angle.
        
        The hour angle is the angular distance from the observer's meridian,
        measured westward from the south point.
        
        Parameters
        ----------
        eot_minutes : float
            Equation of time in minutes
        hour : int
            Hour of observation (0-23, local time)
        minute : int
            Minute of observation (0-59)
        longitude : float, optional
            Observer's longitude (uses instance value if None)
        
        Returns
        -------
        float
            Hour angle in degrees
        """
        if longitude is None:
            longitude = self.longitude
        
        # Calculate time difference from local noon (12:00)
        time_from_noon = (hour - 12) + (minute / 60.0)
        
        # Convert to hour angle
        # 1 hour = 15 degrees of rotation
        hour_angle_from_time = time_from_noon * 15
        
        # Apply equation of time correction (4 minutes of time = 1 degree)
        eot_degrees = eot_minutes / 4.0
        
        # Apply longitude correction relative to timezone meridian
        timezone_meridian = self.timezone_offset * 15
        longitude_correction = longitude - timezone_meridian
        
        # Total hour angle
        hour_angle = hour_angle_from_time + eot_degrees + longitude_correction
        
        return hour_angle
    
    def calculate_altitude(self, declination: float, hour_angle: float) -> float:
        """
        Calculate solar altitude using spherical law of cosines.
        
        Formula: sin(a) = sin(φ)sin(δ) + cos(φ)cos(δ)cos(H)
        
        Where:
        - a = altitude
        - φ = observer's latitude
        - δ = solar declination
        - H = hour angle
        
        Parameters
        ----------
        declination : float
            Solar declination in degrees
        hour_angle : float
            Hour angle in degrees
        
        Returns
        -------
        float
            Solar altitude in degrees above horizon
        """
        # Convert to radians
        dec_rad = np.radians(declination)
        ha_rad = np.radians(hour_angle)
        
        # Spherical law of cosines
        sin_altitude = (np.sin(self.latitude_rad) * np.sin(dec_rad) + 
                       np.cos(self.latitude_rad) * np.cos(dec_rad) * np.cos(ha_rad))
        
        # Convert back to degrees
        altitude = np.degrees(np.arcsin(sin_altitude))
        
        return altitude
    
    def calculate_azimuth(self, declination: float, hour_angle: float, 
                         altitude: float) -> float:
        """
        Calculate solar azimuth.
        
        Azimuth is measured clockwise from North (0° = N, 90° = E, 180° = S, 270° = W)
        
        Parameters
        ----------
        declination : float
            Solar declination in degrees
        hour_angle : float
            Hour angle in degrees
        altitude : float
            Solar altitude in degrees
        
        Returns
        -------
        float
            Solar azimuth in degrees (0-360)
        """
        # Convert to radians
        dec_rad = np.radians(declination)
        ha_rad = np.radians(hour_angle)
        alt_rad = np.radians(altitude)
        
        # Calculate azimuth using spherical trigonometry
        # cos(δ) * sin(H) / cos(a)
        sin_azimuth = np.cos(dec_rad) * np.sin(ha_rad) / np.cos(alt_rad)
        
        # cos(δ) * cos(H) * sin(φ) - sin(δ) * cos(φ) / cos(a)
        cos_azimuth = ((np.cos(dec_rad) * np.cos(ha_rad) * np.sin(self.latitude_rad) - 
                       np.sin(dec_rad) * np.cos(self.latitude_rad)) / np.cos(alt_rad))
        
        # Calculate azimuth using atan2 for proper quadrant
        azimuth = np.degrees(np.arctan2(sin_azimuth, cos_azimuth))
        
        # Normalize to 0-360 range (measured from North, clockwise)
        # Our calculation gives azimuth from South, so we need to adjust
        azimuth = (azimuth + 180) % 360
        
        return azimuth
    
    def calculate_max_altitude(self, declination: float) -> float:
        """
        Calculate maximum possible altitude (at meridian transit/solar noon).
        
        Formula: a_max = 90° - |φ - δ|
        
        Parameters
        ----------
        declination : float
            Solar declination in degrees
        
        Returns
        -------
        float
            Maximum altitude in degrees
        """
        max_altitude = 90 - abs(self.latitude - declination)
        return max_altitude
    
    def map_single_point(self, calc_result: Dict) -> Dict:
        """
        Map a single calculation result to horizon coordinates.
        
        Parameters
        ----------
        calc_result : dict
            Result from AnalemmaCalculator.calculate(), containing:
            - 'declination': Solar declination
            - 'eot': Equation of time
            - 'date': datetime object
        
        Returns
        -------
        dict
            Original data plus:
            - 'altitude': Solar altitude in degrees
            - 'azimuth': Solar azimuth in degrees
            - 'hour_angle': Hour angle in degrees
        """
        # Extract data
        declination = calc_result['declination']
        eot = calc_result['eot']
        date = calc_result['date']
        
        # Calculate hour angle
        hour_angle = self.equation_of_time_to_hour_angle(
            eot, date.hour, date.minute
        )
        
        # Calculate altitude and azimuth
        altitude = self.calculate_altitude(declination, hour_angle)
        azimuth = self.calculate_azimuth(declination, hour_angle, altitude)
        
        # Return enhanced result
        result = calc_result.copy()
        result.update({
            'altitude': altitude,
            'azimuth': azimuth,
            'hour_angle': hour_angle
        })
        
        return result
    
    def map_to_horizon(self, calc_results: List[Dict]) -> List[Dict]:
        """
        Map multiple calculation results to horizon coordinates.
        
        Parameters
        ----------
        calc_results : list
            List of results from AnalemmaCalculator.calculate_year()
        
        Returns
        -------
        list
            List of dictionaries with added altitude/azimuth data
        """
        return [self.map_single_point(result) for result in calc_results]
    
    def get_solar_noon_time(self, eot_minutes: float) -> Tuple[int, int]:
        """
        Calculate the time of solar noon (when sun crosses meridian).
        
        Parameters
        ----------
        eot_minutes : float
            Equation of time in minutes
        
        Returns
        -------
        tuple
            (hour, minute) of solar noon in local time
        """
        # Solar noon is displaced from 12:00 by the equation of time
        # and longitude correction
        
        # Longitude correction
        timezone_meridian = self.timezone_offset * 15
        longitude_correction_deg = self.longitude - timezone_meridian
        longitude_correction_min = longitude_correction_deg * 4  # 4 min per degree
        
        # Total correction
        total_correction_min = eot_minutes + longitude_correction_min
        
        # Apply to noon
        noon_minutes = 12 * 60 + total_correction_min
        
        hour = int(noon_minutes // 60) % 24
        minute = int(noon_minutes % 60)
        
        return (hour, minute)
    
    def get_sunrise_sunset_approx(self, declination: float) -> Tuple[float, float]:
        """
        Approximate sunrise and sunset hour angles.
        
        Note: This is a simplified calculation ignoring atmospheric refraction
        and assuming geometric horizon.
        
        Parameters
        ----------
        declination : float
            Solar declination in degrees
        
        Returns
        -------
        tuple
            (sunrise_hour_angle, sunset_hour_angle) in degrees
        """
        # At sunrise/sunset, altitude = 0
        # cos(H) = -tan(φ) * tan(δ)
        
        dec_rad = np.radians(declination)
        
        cos_h = -np.tan(self.latitude_rad) * np.tan(dec_rad)
        
        # Check if sun rises/sets (doesn't at extreme latitudes during solstices)
        if abs(cos_h) > 1:
            return (None, None)  # Polar day or polar night
        
        h_rad = np.arccos(cos_h)
        h_deg = np.degrees(h_rad)
        
        # Sunrise is at -H, sunset at +H (hour angle measured from noon)
        return (-h_deg, h_deg)
    
    def __repr__(self) -> str:
        return (f"SkyMapper(latitude={self.latitude}°, "
                f"longitude={self.longitude}°, "
                f"timezone_offset={self.timezone_offset}h)")
