"""
Vehicle Routing Problem (VRP) - Main Entry Point

This is the main entry point for the VRP application.
Demonstrates both Greedy Nearest Neighbor and Simulated Annealing algorithms.
"""

import random
from src.models import Order, Vehicle, Route
from src.utils import haversine_distance, calculate_distance
from src.algorithms import GreedyNearestNeighbor, SimulatedAnnealing


def main():
    """
    Demonstration of VRP algorithms: Greedy baseline and Simulated Annealing.
    """
    # Set random seed for reproducibility
    random.seed(42)
    
    print("=" * 80)
    print("Vehicle Routing Problem - Algorithm Comparison")
    print("=" * 80)
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
    print("-" * 80)
    for order in orders:
        print(f"  {order.id}: "
              f"Pickup ({order.pickup_lat:.4f}, {order.pickup_lon:.4f}) -> "
              f"Dropoff ({order.dropoff_lat:.4f}, {order.dropoff_lon:.4f})")
    print()
    
    # Display vehicle details
    print("Available Vehicles:")
    print("-" * 80)
    for vehicle in vehicles:
        print(f"  {vehicle.id}: "
              f"Starting at ({vehicle.current_lat:.4f}, {vehicle.current_lon:.4f})")
    print()
    
    # =========================================================================
    # PART 1: Greedy Nearest Neighbor Algorithm (Baseline)
    # =========================================================================
    
    print("=" * 80)
    print("PART 1: Greedy Nearest Neighbor Algorithm (Baseline)")
    print("=" * 80)
    print()
    
    print("Running Greedy Nearest Neighbor Algorithm...")
    print("-" * 80)
    
    algorithm = GreedyNearestNeighbor(distance_unit='km')
    routes, unassigned = algorithm.solve(vehicles, orders)
    
    # Get solution summary
    summary = algorithm.get_solution_summary(routes, unassigned)
    
    print()
    print("Greedy Solution Summary:")
    print("=" * 80)
    print(f"Total Distance: {summary['total_distance']} {summary['distance_unit']}")
    print(f"Routes Used: {summary['routes_used']}/{summary['total_vehicles']}")
    print(f"Assigned Orders: {summary['assigned_orders']}/{summary['total_orders']}")
    print()
    
    # Display route details
    print("Route Details:")
    print("-" * 80)
    for detail in summary['route_details']:
        if detail['orders_count'] > 0:
            print(f"{detail['vehicle_id']}:")
            print(f"  Orders: {' -> '.join(detail['order_sequence'])}")
            print(f"  Distance: {detail['total_distance']} {summary['distance_unit']}")
            print()
    
    # =========================================================================
    # PART 2: Simulated Annealing Algorithm (Advanced Heuristic)
    # =========================================================================
    
    print("=" * 80)
    print("PART 2: Simulated Annealing Algorithm (Advanced Heuristic)")
    print("=" * 80)
    print()
    
    print("Configuration:")
    print("-" * 80)
    initial_temp = 1000.0
    final_temp = 1.0
    cooling_rate = 0.995
    max_iterations = 5000
    
    print(f"  Initial Temperature: {initial_temp}")
    print(f"  Final Temperature: {final_temp}")
    print(f"  Cooling Rate: {cooling_rate}")
    print(f"  Max Iterations: {max_iterations}")
    print()
    
    print("Running Simulated Annealing...")
    print("-" * 80)
    print("This may take a moment...")
    print()
    
    sa = SimulatedAnnealing(
        initial_temp=initial_temp,
        final_temp=final_temp,
        cooling_rate=cooling_rate,
        max_iterations=max_iterations,
        distance_unit='km',
        verbose=False
    )
    
    sa_routes, sa_cost, sa_stats = sa.solve(vehicles, orders)
    sa_summary = sa.get_solution_summary(sa_routes, sa_cost)
    
    print("Optimization Complete!")
    print()
    
    print("Simulated Annealing Solution Summary:")
    print("=" * 80)
    print(f"Total Distance: {sa_summary['total_distance']} {sa_summary['distance_unit']}")
    print(f"Routes Used: {sa_summary['routes_used']}/{sa_summary['total_vehicles']}")
    print()
    
    print("Optimization Statistics:")
    print("-" * 80)
    print(f"Iterations: {sa_stats['iterations_completed']}")
    print(f"Acceptance Rate: {sa_stats['acceptance_rate']:.1%}")
    print(f"Better Solutions: {sa_stats['better_accepted']}")
    print(f"Worse Solutions Accepted: {sa_stats['worse_accepted']}")
    print()
    print(f"Initial Cost: {sa_stats['initial_cost']} km")
    print(f"Final Cost: {sa_stats['final_cost']} km")
    print(f"Improvement: {sa_stats['improvement']} km "
          f"({sa_stats['improvement_percentage']:.1f}%)")
    print()
    
    print("Route Details:")
    print("-" * 80)
    for detail in sa_summary['route_details']:
        if detail['orders_count'] > 0:
            print(f"{detail['vehicle_id']}:")
            print(f"  Orders: {' -> '.join(detail['order_sequence'])}")
            print()
    
    # =========================================================================
    # PART 3: Algorithm Comparison
    # =========================================================================
    
    print("=" * 80)
    print("PART 3: Algorithm Comparison")
    print("=" * 80)
    print()
    
    print(f"{'Algorithm':<35} {'Total Distance':<20} {'Routes Used':<15}")
    print("-" * 80)
    print(f"{'Greedy Nearest Neighbor':<35} "
          f"{summary['total_distance']:<20} "
          f"{summary['routes_used']:<15}")
    print(f"{'Simulated Annealing':<35} "
          f"{sa_summary['total_distance']:<20} "
          f"{sa_summary['routes_used']:<15}")
    print("-" * 80)
    print()
    
    # Calculate improvement
    improvement = summary['total_distance'] - sa_summary['total_distance']
    improvement_pct = (improvement / summary['total_distance'] * 100)
    
    if improvement > 0:
        print(f"✓ Simulated Annealing improved by {improvement:.2f} km "
              f"({improvement_pct:.1f}%)")
        print(f"  SA found a solution {improvement_pct:.1f}% better than Greedy!")
    elif improvement == 0:
        print(f"= Both algorithms found solutions with equal cost")
    else:
        print(f"⚠ In this run, Greedy performed better by {-improvement:.2f} km")
    
    print()
    
    # =========================================================================
    # PART 4: Key Insights
    # =========================================================================
    
    print("=" * 80)
    print("PART 4: Key Insights")
    print("=" * 80)
    print()
    
    print("Greedy Nearest Neighbor:")
    print("-" * 80)
    print("  ✓ Fast and simple")
    print("  ✓ Deterministic results")
    print("  ✓ Good for quick baseline solutions")
    print("  ✗ Can get stuck in local optima")
    print("  ✗ Quality depends on starting configuration")
    print()
    
    print("Simulated Annealing:")
    print("-" * 80)
    print("  ✓ Escapes local optima through probabilistic acceptance")
    print("  ✓ Typically finds better solutions than greedy")
    print("  ✓ Flexible and tunable")
    print("  ✗ Slower than greedy")
    print("  ✗ Results may vary between runs")
    print()
    
    print("When to use each:")
    print("-" * 80)
    print("  • Greedy: Quick solutions, small problems, baseline comparison")
    print("  • SA: High-quality solutions needed, larger problems, time available")
    print()
    
    print("=" * 80)
    print("Demonstration Complete!")
    print("=" * 80)
    print()
    print("To run individual algorithms:")
    print("  • Greedy: python example_greedy_baseline.py")
    print("  • SA: python example_simulated_annealing.py")
    print()
    print("To run tests:")
    print("  • SA Tests: python test_simulated_annealing.py")
    print()


if __name__ == "__main__":
    main()
