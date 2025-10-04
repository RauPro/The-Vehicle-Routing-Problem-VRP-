"""
Distance calculation utilities for the Vehicle Routing Problem.

This module provides functions to calculate distances between coordinate points
using the Haversine formula for real-world accuracy.
"""

import math
from typing import Tuple


def haversine_distance(
    coord1: Tuple[float, float],
    coord2: Tuple[float, float],
    unit: str = 'km'
) -> float:
    """
    Calculate the great-circle distance between two points on Earth using the
    Haversine formula.
    
    The Haversine formula determines the great-circle distance between two
    points on a sphere given their longitudes and latitudes. This is important
    for calculating real-world distances between geographic coordinates.
    
    Parameters:
        coord1 (Tuple[float, float]): First coordinate as (latitude, longitude)
            in decimal degrees.
        coord2 (Tuple[float, float]): Second coordinate as (latitude, longitude)
            in decimal degrees.
        unit (str): Unit for the result. Options are:
            - 'km': kilometers (default)
            - 'miles': miles
            - 'meters': meters
            - 'feet': feet
    
    Returns:
        float: Distance between the two coordinates in the specified unit.
    
    Raises:
        ValueError: If coordinates are out of valid range or unit is invalid.
    
    Examples:
        >>> # Distance between New York and Los Angeles
        >>> ny = (40.7128, -74.0060)
        >>> la = (34.0522, -118.2437)
        >>> distance = haversine_distance(ny, la)
        >>> print(f"{distance:.2f} km")
        3936.00 km
        
        >>> # Distance in miles
        >>> distance_miles = haversine_distance(ny, la, unit='miles')
        >>> print(f"{distance_miles:.2f} miles")
        2445.53 miles
    """
    # Validate coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError(
            f"Latitude values must be between -90 and 90 degrees. "
            f"Got: {lat1}, {lat2}"
        )
    
    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError(
            f"Longitude values must be between -180 and 180 degrees. "
            f"Got: {lon1}, {lon2}"
        )
    
    # Earth's radius in kilometers
    earth_radius_km = 6371.0
    
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    
    # Calculate differences
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    # Haversine formula
    # a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    # c = 2 * atan2(√a, √(1−a))
    # d = R * c
    a = (
        math.sin(delta_lat / 2) ** 2 +
        math.cos(lat1_rad) * math.cos(lat2_rad) *
        math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Calculate distance in kilometers
    distance_km = earth_radius_km * c
    
    # Convert to requested unit
    unit_conversions = {
        'km': 1.0,
        'kilometers': 1.0,
        'miles': 0.621371,
        'meters': 1000.0,
        'metres': 1000.0,
        'm': 1000.0,
        'feet': 3280.84,
        'ft': 3280.84
    }
    
    unit_lower = unit.lower()
    if unit_lower not in unit_conversions:
        raise ValueError(
            f"Invalid unit '{unit}'. Valid units are: "
            f"{', '.join(sorted(set(unit_conversions.keys())))}"
        )
    
    return distance_km * unit_conversions[unit_lower]


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = 'km'
) -> float:
    """
    Calculate the distance between two coordinate points.
    
    This is a convenience wrapper around haversine_distance that accepts
    individual latitude and longitude values instead of tuples.
    
    Parameters:
        lat1 (float): Latitude of the first point in decimal degrees.
        lon1 (float): Longitude of the first point in decimal degrees.
        lat2 (float): Latitude of the second point in decimal degrees.
        lon2 (float): Longitude of the second point in decimal degrees.
        unit (str): Unit for the result ('km', 'miles', 'meters', 'feet').
            Defaults to 'km'.
    
    Returns:
        float: Distance between the two points in the specified unit.
    
    Raises:
        ValueError: If coordinates are out of valid range or unit is invalid.
    
    Examples:
        >>> # Distance between two points
        >>> distance = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
        >>> print(f"{distance:.2f} km")
        3936.00 km
    """
    return haversine_distance((lat1, lon1), (lat2, lon2), unit=unit)
