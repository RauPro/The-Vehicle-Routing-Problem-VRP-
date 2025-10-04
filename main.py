"""
Vehicle Routing Problem (VRP) - Main Entry Point

This is the main entry point for the VRP application.
"""

from src.models import Order, Vehicle, Route
from src.utils import haversine_distance, calculate_distance
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor


def main():
    """
    Demonstration of the Greedy Nearest Neighbor baseline algorithm.
    """
    print("=" * 70)
    print("Vehicle Routing Problem - Greedy Nearest Neighbor Algorithm")
    print("=" * 70)
    print()
    
    # Create sample orders across New York City
    orders = [
        Order(
            id="ORD001",
            pickup_lat=40.7128,  # Lower Manhattan
            pickup_lon=-74.0060,
            dropoff_lat=40.7589,  # Times Square
            dropoff_lon=-73.9851
        ),
        Order(
            id="ORD002",
            pickup_lat=40.7580,  # Times Square area
            pickup_lon=-73.9855,
            dropoff_lat=40.7614,  # Central Park South
            dropoff_lon=-73.9776
        ),
        Order(
            id="ORD003",
            pickup_lat=40.7831,  # Upper West Side
            pickup_lon=-73.9712,
            dropoff_lat=40.7489,  # Midtown East
            dropoff_lon=-73.9680
        ),
        Order(
            id="ORD004",
            pickup_lat=40.7061,  # Brooklyn Bridge area
            pickup_lon=-73.9969,
            dropoff_lat=40.7306,  # East Village
            dropoff_lon=-73.9866
        ),
        Order(
            id="ORD005",
            pickup_lat=40.7549,  # Hell's Kitchen
            pickup_lon=-73.9840,
            dropoff_lat=40.7829,  # Upper West Side
            dropoff_lon=-73.9654
        ),
    ]
    
    # Create vehicles starting from different locations
    vehicles = [
        Vehicle(
            id="VEH001",
            current_lat=40.7128,  # Lower Manhattan
            current_lon=-74.0060
        ),
        Vehicle(
            id="VEH002",
            current_lat=40.7580,  # Midtown
            current_lon=-73.9855
        ),
    ]
    
    print(f"Total Orders: {len(orders)}")
    print(f"Total Vehicles: {len(vehicles)}")
    print()
    
    # Display order details
    print("Orders to be assigned:")
    print("-" * 70)
    for order in orders:
        print(f"  {order.id}: "
              f"Pickup ({order.pickup_lat:.4f}, {order.pickup_lon:.4f}) -> "
              f"Dropoff ({order.dropoff_lat:.4f}, {order.dropoff_lon:.4f})")
    print()
    
    # Display vehicle details
    print("Available Vehicles:")
    print("-" * 70)
    for vehicle in vehicles:
        print(f"  {vehicle.id}: "
              f"Starting at ({vehicle.current_lat:.4f}, {vehicle.current_lon:.4f})")
    print()
    
    # Run the greedy nearest neighbor algorithm
    print("Running Greedy Nearest Neighbor Algorithm...")
    print("-" * 70)
    
    algorithm = GreedyNearestNeighbor(distance_unit='km')
    routes, unassigned = algorithm.solve(vehicles, orders)
    
    # Get solution summary
    summary = algorithm.get_solution_summary(routes, unassigned)
    
    print()
    print("Solution Summary:")
    print("=" * 70)
    print(f"Total Vehicles: {summary['total_vehicles']}")
    print(f"Total Orders: {summary['total_orders']}")
    print(f"Assigned Orders: {summary['assigned_orders']}")
    print(f"Unassigned Orders: {summary['unassigned_orders']}")
    print(f"Routes Used: {summary['routes_used']}")
    print(f"Total Distance: {summary['total_distance']} {summary['distance_unit']}")
    print(f"Average Distance per Route: {summary['average_distance_per_route']} {summary['distance_unit']}")
    print()
    
    # Display detailed route information
    print("Detailed Route Information:")
    print("=" * 70)
    for detail in summary['route_details']:
        if detail['orders_count'] > 0:
            print(f"\nVehicle: {detail['vehicle_id']}")
            print(f"  Orders Assigned: {detail['orders_count']}")
            print(f"  Total Distance: {detail['total_distance']} {summary['distance_unit']}")
            print(f"  Order Sequence: {' -> '.join(detail['order_sequence'])}")
            
            # Display route details with coordinates
            route = next(r for r in routes if r.vehicle.id == detail['vehicle_id'])
            print(f"  Route Details:")
            print(f"    Start: {route.vehicle}")
            
            for i, order in enumerate(route.orders, 1):
                pickup_dist = 0.0
                if i == 1:
                    # Distance from vehicle start to first pickup
                    pickup_dist = haversine_distance(
                        route.vehicle.get_current_coordinates(),
                        order.get_pickup_coordinates(),
                        unit='km'
                    )
                else:
                    # Distance from previous dropoff to current pickup
                    prev_order = route.orders[i-2]
                    pickup_dist = haversine_distance(
                        prev_order.get_dropoff_coordinates(),
                        order.get_pickup_coordinates(),
                        unit='km'
                    )
                
                delivery_dist = haversine_distance(
                    order.get_pickup_coordinates(),
                    order.get_dropoff_coordinates(),
                    unit='km'
                )
                
                print(f"    {i}. {order.id}:")
                print(f"       To Pickup: {pickup_dist:.2f} km")
                print(f"       Delivery: {delivery_dist:.2f} km")
    
    # Display unassigned orders if any
    if unassigned:
        print()
        print("Unassigned Orders:")
        print("-" * 70)
        for order in unassigned:
            print(f"  {order.id}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
