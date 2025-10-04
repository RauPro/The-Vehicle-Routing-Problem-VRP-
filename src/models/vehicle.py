"""
Vehicle model for the Vehicle Routing Problem.

This module defines the Vehicle class representing a delivery vehicle
with its current location.
"""

from dataclasses import dataclass


@dataclass
class Vehicle:
    """
    Represents a vehicle with its current location.
    
    Attributes:
        id (str): Unique identifier for the vehicle.
        current_lat (float): Latitude coordinate of the vehicle's 
            current location.
        current_lon (float): Longitude coordinate of the vehicle's 
            current location.
    """
    id: str
    current_lat: float
    current_lon: float
    
    def __post_init__(self) -> None:
        """
        Validate the vehicle data after initialization.
        
        Raises:
            ValueError: If latitude or longitude values are out of valid range.
        """
        self._validate_coordinates()
    
    def _validate_coordinates(self) -> None:
        """
        Validate that coordinates are within valid geographic ranges.
        
        Raises:
            ValueError: If any coordinate is out of valid range.
        """
        # Validate latitude is within valid range (-90 to 90)
        if not -90 <= self.current_lat <= 90:
            raise ValueError(
                f"Vehicle latitude {self.current_lat} is out of range "
                f"(-90 to 90)"
            )
        
        # Validate longitude is within valid range (-180 to 180)
        if not -180 <= self.current_lon <= 180:
            raise ValueError(
                f"Vehicle longitude {self.current_lon} is out of range "
                f"(-180 to 180)"
            )
    
    def get_current_coordinates(self) -> tuple[float, float]:
        """
        Get the current coordinates of the vehicle.
        
        Returns:
            tuple[float, float]: (latitude, longitude) of current location.
        """
        return (self.current_lat, self.current_lon)
    
    def update_location(self, new_lat: float, new_lon: float) -> None:
        """
        Update the vehicle's current location.
        
        Parameters:
            new_lat (float): New latitude coordinate.
            new_lon (float): New longitude coordinate.
        
        Raises:
            ValueError: If new coordinates are out of valid range.
        """
        # Temporarily update coordinates for validation
        old_lat, old_lon = self.current_lat, self.current_lon
        self.current_lat = new_lat
        self.current_lon = new_lon
        
        try:
            self._validate_coordinates()
        except ValueError:
            # Revert to old coordinates if validation fails
            self.current_lat = old_lat
            self.current_lon = old_lon
            raise
    
    def __str__(self) -> str:
        """
        String representation of the vehicle.
        
        Returns:
            str: Human-readable string describing the vehicle.
        """
        return (
            f"Vehicle({self.id} at "
            f"[{self.current_lat}, {self.current_lon}])"
        )
