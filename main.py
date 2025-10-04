"""
Vehicle Routing Problem (VRP) - Main Entry Point

This is the main entry point for the VRP application.
"""

from src.models import Order, Vehicle, Route
from src.utils import haversine_distance, calculate_distance


def main():
    """
    Demonstration of the core data structures and distance calculations.
    """
    # Create sample orders
    order1 = Order(
        id="ORD001",
        pickup_lat=40.7128,
        pickup_lon=-74.0060,
        dropoff_lat=40.7589,
        dropoff_lon=-73.9851
    )
    
    order2 = Order(
        id="ORD002",
        pickup_lat=40.7580,
        pickup_lon=-73.9855,
        dropoff_lat=40.7614,
        dropoff_lon=-73.9776
    )
    
    # Create a vehicle
    vehicle = Vehicle(
        id="VEH001",
        current_lat=40.7128,
        current_lon=-74.0060
    )
    
    # Create a route and assign orders
    route = Route(vehicle=vehicle)
    route.add_order(order1)
    route.add_order(order2)
    
    # Display route information
    print(f"Route for Vehicle {route.vehicle.id}:")
    print(f"Total Orders: {route.get_total_orders()}")
    print()
    
    # Calculate and display distances
    print("Distance Calculations:")
    print("-" * 50)
    
    # Distance from vehicle to first order pickup
    vehicle_coords = vehicle.get_current_coordinates()
    order1_pickup = order1.get_pickup_coordinates()
    
    distance_to_pickup = haversine_distance(vehicle_coords, order1_pickup)
    print(f"Vehicle to Order 1 Pickup: {distance_to_pickup:.2f} km")
    
    # Distance for order1 (pickup to dropoff)
    order1_dropoff = order1.get_dropoff_coordinates()
    order1_distance = haversine_distance(order1_pickup, order1_dropoff)
    print(f"Order 1 Distance: {order1_distance:.2f} km")
    
    # Distance for order2 (pickup to dropoff)
    order2_pickup = order2.get_pickup_coordinates()
    order2_dropoff = order2.get_dropoff_coordinates()
    order2_distance = calculate_distance(
        order2_pickup[0], order2_pickup[1],
        order2_dropoff[0], order2_dropoff[1]
    )
    print(f"Order 2 Distance: {order2_distance:.2f} km")
    
    # Distance in different units
    print()
    print("Order 1 Distance in different units:")
    print(f"  Kilometers: {haversine_distance(order1_pickup, order1_dropoff, 'km'):.2f} km")
    print(f"  Miles: {haversine_distance(order1_pickup, order1_dropoff, 'miles'):.2f} miles")
    print(f"  Meters: {haversine_distance(order1_pickup, order1_dropoff, 'meters'):.2f} m")
    
    print()
    for i, order in enumerate(route.orders, 1):
        print(f"  Order {order.id}: "
              f"({order.pickup_lat}, {order.pickup_lon}) -> "
              f"({order.dropoff_lat}, {order.dropoff_lon})")


if __name__ == "__main__":
    main()
