"""
Greedy Nearest Neighbor Algorithm for the Vehicle Routing Problem.

This module implements a simple baseline algorithm that assigns orders to
vehicles using a greedy nearest neighbor approach. This serves as a baseline
for comparing more sophisticated routing algorithms.
"""

from typing import List, Tuple, Set, Optional
from ..models import Order, Vehicle, Route
from ..utils import haversine_distance


class GreedyNearestNeighbor:
    """
    Implements a greedy nearest neighbor algorithm for vehicle routing.
    
    This is a simple baseline algorithm that iteratively assigns the closest
    unassigned order pickup point to each vehicle. The algorithm continues
    until all orders are assigned.
    
    Algorithm Logic:
        1. For each vehicle in sequence:
           a. Start from the vehicle's current location
           b. Find the nearest unassigned order pickup point
           c. Assign that order to the vehicle
           d. Update the current position to the order's dropoff location
           e. Repeat until all orders are assigned or vehicle capacity is reached
    
    This serves as a baseline "dumb" algorithm for comparison with more
    sophisticated heuristics.
    """
    
    def __init__(self, distance_unit: str = 'km'):
        """
        Initialize the Greedy Nearest Neighbor algorithm.
        
        Parameters:
            distance_unit (str): Unit for distance calculations.
                Options: 'km', 'miles', 'meters', 'feet'. Defaults to 'km'.
        """
        self.distance_unit = distance_unit
    
    def solve(
        self,
        vehicles: List[Vehicle],
        orders: List[Order]
    ) -> Tuple[List[Route], List[Order]]:
        """
        Assign orders to vehicles using the greedy nearest neighbor approach.
        
        This method creates routes for all vehicles by iteratively assigning
        the nearest unassigned order to each vehicle. The algorithm cycles
        through all vehicles until all orders are assigned.
        
        Parameters:
            vehicles (List[Vehicle]): List of available vehicles.
            orders (List[Order]): List of orders to be assigned.
        
        Returns:
            Tuple[List[Route], List[Order]]: A tuple containing:
                - List of routes (one per vehicle) with assigned orders
                - List of unassigned orders (empty if all orders were assigned)
        
        Raises:
            ValueError: If vehicles or orders lists are empty.
        
        Examples:
            >>> algorithm = GreedyNearestNeighbor()
            >>> vehicles = [Vehicle("V1", 40.7128, -74.0060)]
            >>> orders = [Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)]
            >>> routes, unassigned = algorithm.solve(vehicles, orders)
            >>> print(f"Routes: {len(routes)}, Unassigned: {len(unassigned)}")
            Routes: 1, Unassigned: 0
        """
        # Validate input
        if not vehicles:
            raise ValueError("Vehicles list cannot be empty")
        if not orders:
            raise ValueError("Orders list cannot be empty")
        
        # Initialize routes for each vehicle
        routes = [Route(vehicle=vehicle) for vehicle in vehicles]
        
        # Track which orders have been assigned
        unassigned_orders: Set[str] = {order.id for order in orders}
        
        # Create a mapping of order IDs to Order objects for quick lookup
        order_map = {order.id: order for order in orders}
        
        # Keep assigning orders until all are assigned
        # Use round-robin approach across all vehicles
        vehicle_index = 0
        
        while unassigned_orders:
            # Get current vehicle and its route
            current_route = routes[vehicle_index]
            
            # Find the nearest unassigned order for this vehicle
            nearest_order_id = self._find_nearest_order(
                current_route=current_route,
                unassigned_orders=unassigned_orders,
                order_map=order_map
            )
            
            # If we found a nearest order, assign it
            if nearest_order_id:
                order_to_assign = order_map[nearest_order_id]
                current_route.add_order(order_to_assign)
                unassigned_orders.remove(nearest_order_id)
            
            # Move to next vehicle (round-robin)
            vehicle_index = (vehicle_index + 1) % len(vehicles)
            
            # Safety check: if we've cycled through all vehicles and
            # no order was assigned, break to avoid infinite loop
            if nearest_order_id is None:
                break
        
        # Collect any remaining unassigned orders
        remaining_orders = [
            order_map[order_id] for order_id in unassigned_orders
        ]
        
        return routes, remaining_orders
    
    def _find_nearest_order(
        self,
        current_route: Route,
        unassigned_orders: Set[str],
        order_map: dict
    ) -> Optional[str]:
        """
        Find the nearest unassigned order to the vehicle's current position.
        
        The current position is determined by:
        - If the route has orders: the dropoff location of the last order
        - If the route is empty: the vehicle's initial location
        
        Parameters:
            current_route (Route): The route being built for the vehicle.
            unassigned_orders (Set[str]): Set of unassigned order IDs.
            order_map (dict): Mapping of order IDs to Order objects.
        
        Returns:
            Optional[str]: The ID of the nearest order, or None if no orders
                are available.
        """
        if not unassigned_orders:
            return None
        
        # Determine current position
        if current_route.is_empty():
            # Start from vehicle's initial location
            current_position = current_route.vehicle.get_current_coordinates()
        else:
            # Continue from last order's dropoff location
            last_order = current_route.orders[-1]
            current_position = last_order.get_dropoff_coordinates()
        
        # Find the nearest unassigned order
        nearest_order_id = None
        min_distance = float('inf')
        
        for order_id in unassigned_orders:
            order = order_map[order_id]
            pickup_coords = order.get_pickup_coordinates()
            
            # Calculate distance from current position to pickup
            distance = haversine_distance(
                current_position,
                pickup_coords,
                unit=self.distance_unit
            )
            
            # Update if this is the nearest order so far
            if distance < min_distance:
                min_distance = distance
                nearest_order_id = order_id
        
        return nearest_order_id
    
    def calculate_total_distance(self, route: Route) -> float:
        """
        Calculate the total distance for a complete route.
        
        The total distance includes:
        1. Distance from vehicle's start to first order's pickup
        2. Distance from each pickup to its dropoff
        3. Distance between consecutive orders (previous dropoff to next pickup)
        
        Parameters:
            route (Route): The route to calculate distance for.
        
        Returns:
            float: Total distance in the configured unit.
        
        Examples:
            >>> algorithm = GreedyNearestNeighbor()
            >>> route = Route(vehicle=Vehicle("V1", 40.7128, -74.0060))
            >>> route.add_order(Order("O1", 40.7580, -73.9855, 40.7614, -73.9776))
            >>> total_distance = algorithm.calculate_total_distance(route)
            >>> print(f"Total distance: {total_distance:.2f} km")
        """
        if route.is_empty():
            return 0.0
        
        total_distance = 0.0
        current_position = route.vehicle.get_current_coordinates()
        
        for order in route.orders:
            pickup_coords = order.get_pickup_coordinates()
            dropoff_coords = order.get_dropoff_coordinates()
            
            # Distance from current position to pickup
            total_distance += haversine_distance(
                current_position,
                pickup_coords,
                unit=self.distance_unit
            )
            
            # Distance from pickup to dropoff
            total_distance += haversine_distance(
                pickup_coords,
                dropoff_coords,
                unit=self.distance_unit
            )
            
            # Update current position to dropoff location
            current_position = dropoff_coords
        
        return total_distance
    
    def get_solution_summary(
        self,
        routes: List[Route],
        unassigned_orders: List[Order]
    ) -> dict:
        """
        Generate a summary of the routing solution.
        
        Parameters:
            routes (List[Route]): List of routes with assigned orders.
            unassigned_orders (List[Order]): List of orders that weren't assigned.
        
        Returns:
            dict: Summary statistics including:
                - total_vehicles: Number of vehicles
                - total_orders: Total number of orders
                - assigned_orders: Number of assigned orders
                - unassigned_orders: Number of unassigned orders
                - routes_used: Number of routes with at least one order
                - total_distance: Total distance across all routes
                - average_distance_per_route: Average distance per used route
                - route_details: List of details for each route
        """
        total_orders = sum(route.get_total_orders() for route in routes)
        total_orders += len(unassigned_orders)
        
        routes_used = sum(1 for route in routes if not route.is_empty())
        
        # Calculate distances for all routes
        route_distances = [
            self.calculate_total_distance(route) for route in routes
        ]
        total_distance = sum(route_distances)
        
        avg_distance = (
            total_distance / routes_used if routes_used > 0 else 0.0
        )
        
        # Build detailed route information
        route_details = []
        for i, (route, distance) in enumerate(zip(routes, route_distances)):
            route_details.append({
                'vehicle_id': route.vehicle.id,
                'orders_count': route.get_total_orders(),
                'total_distance': round(distance, 2),
                'order_sequence': [order.id for order in route.orders]
            })
        
        return {
            'total_vehicles': len(routes),
            'total_orders': total_orders,
            'assigned_orders': total_orders - len(unassigned_orders),
            'unassigned_orders': len(unassigned_orders),
            'routes_used': routes_used,
            'total_distance': round(total_distance, 2),
            'average_distance_per_route': round(avg_distance, 2),
            'distance_unit': self.distance_unit,
            'route_details': route_details
        }
