"""
Example demonstration of the Greedy Nearest Neighbor baseline algorithm.

This script shows how to use the GreedyNearestNeighbor algorithm
to solve a simple Vehicle Routing Problem.
"""

from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor


def main():
    """
    Simple example demonstrating the greedy baseline algorithm.
    """
    print("Greedy Nearest Neighbor - Simple Example")
    print("=" * 50)
    print()
    
    # Create a simple set of orders
    orders = [
        Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
        Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
        Order("O3", 40.7831, -73.9712, 40.7489, -73.9680),
    ]
    
    # Create a single vehicle
    vehicles = [
        Vehicle("V1", 40.7128, -74.0060),
    ]
    
    # Initialize and run the algorithm
    algorithm = GreedyNearestNeighbor(distance_unit='km')
    routes, unassigned = algorithm.solve(vehicles, orders)
    
    # Display results
    print(f"Orders assigned: {sum(r.get_total_orders() for r in routes)}")
    print(f"Unassigned orders: {len(unassigned)}")
    print()
    
    for route in routes:
        if not route.is_empty():
            print(f"Vehicle {route.vehicle.id}:")
            for order in route.orders:
                print(f"  - {order.id}")
            
            distance = algorithm.calculate_total_distance(route)
            print(f"  Total distance: {distance:.2f} km")
    
    # Get full summary
    summary = algorithm.get_solution_summary(routes, unassigned)
    print()
    print("Summary:")
    print(f"  Total distance: {summary['total_distance']} km")
    print(f"  Routes used: {summary['routes_used']}")


if __name__ == "__main__":
    main()
