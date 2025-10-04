"""
Vehicle Routing Problem (VRP) - Main Entry Point

This is the main entry point for the VRP application.
"""

from src.models import Order, Vehicle, Route


def main():
    """
    Demonstration of the core data structures usage.
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
    for order in route.orders:
        print(f"  Order {order.id}: "
              f"({order.pickup_lat}, {order.pickup_lon}) -> "
              f"({order.dropoff_lat}, {order.dropoff_lon})")


if __name__ == "__main__":
    main()
