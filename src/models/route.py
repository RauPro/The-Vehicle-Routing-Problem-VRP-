"""
Route model for the Vehicle Routing Problem.

This module defines the Route class that combines a vehicle
with a sequence of orders.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .order import Order
from .vehicle import Vehicle


@dataclass
class Route:
    """
    Represents a route containing a list of orders assigned to a vehicle.
    
    Attributes:
        vehicle (Vehicle): The vehicle assigned to this route.
        orders (List[Order]): List of orders to be fulfilled by the vehicle.
            Defaults to an empty list if not provided.
    """
    vehicle: Vehicle
    orders: List[Order] = field(default_factory=list)
    
    def add_order(self, order: Order) -> None:
        """
        Add an order to the route.
        
        Parameters:
            order (Order): The order to be added to the route.
        """
        self.orders.append(order)
    
    def remove_order(self, order_id: str) -> bool:
        """
        Remove an order from the route by its ID.
        
        Parameters:
            order_id (str): The ID of the order to remove.
        
        Returns:
            bool: True if the order was found and removed, False otherwise.
        """
        for i, order in enumerate(self.orders):
            if order.id == order_id:
                self.orders.pop(i)
                return True
        return False
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """
        Retrieve an order from the route by its ID.
        
        Parameters:
            order_id (str): The ID of the order to retrieve.
        
        Returns:
            Optional[Order]: The order if found, None otherwise.
        """
        for order in self.orders:
            if order.id == order_id:
                return order
        return None
    
    def get_total_orders(self) -> int:
        """
        Get the total number of orders in the route.
        
        Returns:
            int: The number of orders assigned to this route.
        """
        return len(self.orders)
    
    def clear_orders(self) -> None:
        """
        Remove all orders from the route.
        """
        self.orders.clear()
    
    def is_empty(self) -> bool:
        """
        Check if the route has no orders.
        
        Returns:
            bool: True if the route has no orders, False otherwise.
        """
        return len(self.orders) == 0
    
    def __str__(self) -> str:
        """
        String representation of the route.
        
        Returns:
            str: Human-readable string describing the route.
        """
        return (
            f"Route(Vehicle: {self.vehicle.id}, "
            f"Orders: {self.get_total_orders()})"
        )
