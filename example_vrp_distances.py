"""
Practical example of using distance calculations in a VRP scenario.

This script demonstrates how distance calculations can be used to:
1. Calculate distances from vehicles to order pickups
2. Calculate order distances (pickup to dropoff)
3. Estimate total route distances
4. Find the nearest vehicle to an order
"""

from typing import List
from src.models import Order, Vehicle, Route
from src.utils import haversine_distance


def find_nearest_vehicle(
    order: Order,
    vehicles: List[Vehicle]
) -> tuple[Vehicle, float]:
    """
    Find the nearest vehicle to an order's pickup location.
    
    Parameters:
        order (Order): The order to find a vehicle for.
        vehicles (List[Vehicle]): List of available vehicles.
    
    Returns:
        tuple[Vehicle, float]: The nearest vehicle and distance to pickup (km).
    """
    pickup_coords = order.get_pickup_coordinates()
    nearest_vehicle = None
    min_distance = float('inf')
    
    for vehicle in vehicles:
        vehicle_coords = vehicle.get_current_coordinates()
        distance = haversine_distance(vehicle_coords, pickup_coords)
        
        if distance < min_distance:
            min_distance = distance
            nearest_vehicle = vehicle
    
    return nearest_vehicle, min_distance


def calculate_route_distance(route: Route) -> float:
    """
    Calculate the total distance for a route.
    
    This includes:
    - Distance from vehicle to first pickup
    - Distance for each order (pickup to dropoff)
    - Distance between consecutive dropoff and pickup locations
    
    Parameters:
        route (Route): The route to calculate distance for.
    
    Returns:
        float: Total route distance in kilometers.
    """
    if route.is_empty():
        return 0.0
    
    total_distance = 0.0
    current_position = route.vehicle.get_current_coordinates()
    
    for order in route.orders:
        # Distance to pickup
        pickup_coords = order.get_pickup_coordinates()
        distance_to_pickup = haversine_distance(current_position, pickup_coords)
        total_distance += distance_to_pickup
        
        # Distance from pickup to dropoff
        dropoff_coords = order.get_dropoff_coordinates()
        order_distance = haversine_distance(pickup_coords, dropoff_coords)
        total_distance += order_distance
        
        # Update current position to dropoff location
        current_position = dropoff_coords
    
    return total_distance


def main():
    """
    Demonstrate practical VRP distance calculations.
    """
    print("=" * 70)
    print("VRP Distance Calculation - Practical Example")
    print("=" * 70)
    print()
    
    # Create multiple vehicles at different locations
    vehicles = [
        Vehicle(id="VEH001", current_lat=40.7128, current_lon=-74.0060),  # NYC
        Vehicle(id="VEH002", current_lat=40.7580, current_lon=-73.9855),  # Manhattan
        Vehicle(id="VEH003", current_lat=40.6782, current_lon=-73.9442),  # Brooklyn
    ]
    
    # Create multiple orders
    orders = [
        Order(
            id="ORD001",
            pickup_lat=40.7589, pickup_lon=-73.9851,  # Times Square
            dropoff_lat=40.7614, dropoff_lon=-73.9776  # Central Park
        ),
        Order(
            id="ORD002",
            pickup_lat=40.7484, pickup_lon=-73.9857,  # Empire State
            dropoff_lat=40.7058, dropoff_lon=-74.0134  # Battery Park
        ),
        Order(
            id="ORD003",
            pickup_lat=40.7829, pickup_lon=-73.9654,  # Upper East Side
            dropoff_lat=40.7794, dropoff_lon=-73.9632  # Metropolitan Museum
        ),
    ]
    
    print("Available Vehicles:")
    for vehicle in vehicles:
        print(f"  {vehicle.id}: {vehicle.get_current_coordinates()}")
    print()
    
    print("Orders to Process:")
    for order in orders:
        print(f"  {order.id}: {order.get_pickup_coordinates()} -> "
              f"{order.get_dropoff_coordinates()}")
    print()
    
    # Find nearest vehicle for each order
    print("Nearest Vehicle Assignment:")
    print("-" * 70)
    assignments = {}
    
    for order in orders:
        nearest_vehicle, distance = find_nearest_vehicle(order, vehicles)
        assignments[order.id] = nearest_vehicle
        
        pickup = order.get_pickup_coordinates()
        dropoff = order.get_dropoff_coordinates()
        order_dist = haversine_distance(pickup, dropoff)
        
        print(f"{order.id}:")
        print(f"  Nearest Vehicle: {nearest_vehicle.id}")
        print(f"  Distance to Pickup: {distance:.2f} km")
        print(f"  Order Distance: {order_dist:.2f} km")
        print(f"  Total: {distance + order_dist:.2f} km")
        print()
    
    # Create sample routes
    print("Sample Route Analysis:")
    print("-" * 70)
    
    # Route 1: VEH002 handles ORD001 and ORD003
    route1 = Route(vehicle=vehicles[1])  # VEH002
    route1.add_order(orders[0])  # ORD001
    route1.add_order(orders[2])  # ORD003
    
    route1_distance = calculate_route_distance(route1)
    print(f"Route 1 (VEH002):")
    print(f"  Orders: {[order.id for order in route1.orders]}")
    print(f"  Total Distance: {route1_distance:.2f} km")
    print()
    
    # Route 2: VEH001 handles ORD002
    route2 = Route(vehicle=vehicles[0])  # VEH001
    route2.add_order(orders[1])  # ORD002
    
    route2_distance = calculate_route_distance(route2)
    print(f"Route 2 (VEH001):")
    print(f"  Orders: {[order.id for order in route2.orders]}")
    print(f"  Total Distance: {route2_distance:.2f} km")
    print()
    
    # Summary
    print("Summary:")
    print("-" * 70)
    total_distance = route1_distance + route2_distance
    print(f"Total Distance All Routes: {total_distance:.2f} km")
    print(f"Average Distance per Route: {total_distance / 2:.2f} km")
    print(f"Total Orders Processed: {route1.get_total_orders() + route2.get_total_orders()}")
    print()
    
    # Distance comparison
    print("Distance Comparison (Multiple Units):")
    print("-" * 70)
    print(f"Total Distance:")
    print(f"  {total_distance:.2f} km")
    print(f"  {haversine_distance((0, 0), (0, total_distance/111), 'miles'):.2f} miles (approx)")
    print(f"  {total_distance * 1000:.2f} meters")
    
    print()
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
