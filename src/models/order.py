"""
Order model for the Vehicle Routing Problem.

This module defines the Order class representing a delivery order
with pickup and dropoff locations.
"""

from dataclasses import dataclass


@dataclass
class Order:
    """
    Represents a delivery order with pickup and dropoff locations.
    
    Attributes:
        id (str): Unique identifier for the order.
        pickup_lat (float): Latitude coordinate of the pickup location.
        pickup_lon (float): Longitude coordinate of the pickup location.
        dropoff_lat (float): Latitude coordinate of the dropoff location.
        dropoff_lon (float): Longitude coordinate of the dropoff location.
    """
    id: str
    pickup_lat: float
    pickup_lon: float
    dropoff_lat: float
    dropoff_lon: float
    
    def __post_init__(self) -> None:
        """
        Validate the order data after initialization.
        
        Raises:
            ValueError: If latitude or longitude values are out of valid range.
        """
        self._validate_coordinates()
    
    def _validate_coordinates(self) -> None:
        """
        Validate that all coordinates are within valid geographic ranges.
        
        Raises:
            ValueError: If any coordinate is out of valid range.
        """
        # Validate latitude values are within valid range (-90 to 90)
        if not -90 <= self.pickup_lat <= 90:
            raise ValueError(
                f"Pickup latitude {self.pickup_lat} is out of range "
                f"(-90 to 90)"
            )
        if not -90 <= self.dropoff_lat <= 90:
            raise ValueError(
                f"Dropoff latitude {self.dropoff_lat} is out of range "
                f"(-90 to 90)"
            )
        
        # Validate longitude values are within valid range (-180 to 180)
        if not -180 <= self.pickup_lon <= 180:
            raise ValueError(
                f"Pickup longitude {self.pickup_lon} is out of range "
                f"(-180 to 180)"
            )
        if not -180 <= self.dropoff_lon <= 180:
            raise ValueError(
                f"Dropoff longitude {self.dropoff_lon} is out of range "
                f"(-180 to 180)"
            )
    
    def get_pickup_coordinates(self) -> tuple[float, float]:
        """
        Get the pickup coordinates as a tuple.
        
        Returns:
            tuple[float, float]: (latitude, longitude) of pickup location.
        """
        return (self.pickup_lat, self.pickup_lon)
    
    def get_dropoff_coordinates(self) -> tuple[float, float]:
        """
        Get the dropoff coordinates as a tuple.
        
        Returns:
            tuple[float, float]: (latitude, longitude) of dropoff location.
        """
        return (self.dropoff_lat, self.dropoff_lon)
    
    def __str__(self) -> str:
        """
        String representation of the order.
        
        Returns:
            str: Human-readable string describing the order.
        """
        return (
            f"Order({self.id}: "
            f"[{self.pickup_lat}, {self.pickup_lon}] -> "
            f"[{self.dropoff_lat}, {self.dropoff_lon}])"
        )
