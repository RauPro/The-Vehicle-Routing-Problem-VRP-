"""
Vehicle Routing Problem (VRP) Package

A comprehensive solution for vehicle routing optimization.
"""

from .models import Order, Vehicle, Route
from .utils import haversine_distance, calculate_distance

__version__ = "0.1.0"

__all__ = [
    'Order',
    'Vehicle',
    'Route',
    'haversine_distance',
    'calculate_distance'
]
