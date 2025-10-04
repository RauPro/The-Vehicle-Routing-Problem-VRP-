"""
Simulated Annealing Example for Vehicle Routing Problem

This example demonstrates how to use the Simulated Annealing algorithm
to optimize vehicle routes. It compares SA with the greedy baseline and
shows detailed optimization progress.
"""

import random
from src.models import Order, Vehicle
from src.algorithms import SimulatedAnnealing, GreedyNearestNeighbor


def main():
    """
    Main demonstration of the Simulated Annealing algorithm.
    """
    print("=" * 80)
    print("Vehicle Routing Problem - Simulated Annealing Algorithm")
    print("=" * 80)
    print()
    
    # Set random seed for reproducibility
    random.seed(42)
    
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
        Order(
            id="ORD006",
            pickup_lat=40.7282,  # SoHo
            pickup_lon=-73.9942,
            dropoff_lat=40.7484,  # Midtown
            dropoff_lon=-73.9857
        ),
        Order(
            id="ORD007",
            pickup_lat=40.7505,  # Midtown West
            pickup_lon=-73.9934,
            dropoff_lat=40.7678,  # Lincoln Center
            dropoff_lon=-73.9825
        ),
        Order(
            id="ORD008",
            pickup_lat=40.7417,  # Chelsea
            pickup_lon=-73.9898,
            dropoff_lat=40.7527,  # Times Square North
            dropoff_lon=-73.9772
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
        Vehicle(
            id="VEH003",
            current_lat=40.7831,  # Upper West Side
            current_lon=-73.9712
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
    
    # -------------------------------------------------------------------------
    # PART 1: Run Greedy Algorithm (Baseline)
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("PART 1: Greedy Nearest Neighbor Baseline")
    print("=" * 80)
    print()
    
    greedy = GreedyNearestNeighbor(distance_unit='km')
    greedy_routes, greedy_unassigned = greedy.solve(vehicles, orders)
    greedy_summary = greedy.get_solution_summary(greedy_routes, greedy_unassigned)
    
    print("Greedy Solution:")
    print("-" * 80)
    print(f"Total Distance: {greedy_summary['total_distance']} km")
    print(f"Routes Used: {greedy_summary['routes_used']}/{greedy_summary['total_vehicles']}")
    print()
    
    for detail in greedy_summary['route_details']:
        if detail['orders_count'] > 0:
            print(f"{detail['vehicle_id']}:")
            print(f"  Orders: {' -> '.join(detail['order_sequence'])}")
            print(f"  Distance: {detail['total_distance']} km")
    print()
    
    # -------------------------------------------------------------------------
    # PART 2: Run Simulated Annealing
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("PART 2: Simulated Annealing Optimization")
    print("=" * 80)
    print()
    
    print("Configuration:")
    print("-" * 80)
    initial_temp = 1000.0
    final_temp = 1.0
    cooling_rate = 0.995
    max_iterations = 3000
    
    print(f"  Initial Temperature: {initial_temp}")
    print(f"  Final Temperature: {final_temp}")
    print(f"  Cooling Rate: {cooling_rate}")
    print(f"  Max Iterations: {max_iterations}")
    print()
    
    print("Running Simulated Annealing...")
    print("-" * 80)
    
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
    
    # Display optimization statistics
    print("Optimization Statistics:")
    print("-" * 80)
    print(f"Iterations Completed: {sa_stats['iterations_completed']}")
    print(f"Total Attempts: {sa_stats['total_attempts']}")
    print(f"Solutions Accepted: {sa_stats['total_accepted']} "
          f"({sa_stats['acceptance_rate']:.1%})")
    print(f"  Better Solutions: {sa_stats['better_accepted']}")
    print(f"  Worse Solutions: {sa_stats['worse_accepted']}")
    print()
    print(f"Initial Cost: {sa_stats['initial_cost']} km")
    print(f"Final Cost: {sa_stats['final_cost']} km")
    print(f"Improvement: {sa_stats['improvement']} km "
          f"({sa_stats['improvement_percentage']:.1f}%)")
    print()
    
    # Display SA solution
    print("Simulated Annealing Solution:")
    print("-" * 80)
    print(f"Total Distance: {sa_summary['total_distance']} km")
    print(f"Routes Used: {sa_summary['routes_used']}/{sa_summary['total_vehicles']}")
    print()
    
    for detail in sa_summary['route_details']:
        if detail['orders_count'] > 0:
            print(f"{detail['vehicle_id']}:")
            print(f"  Orders: {' -> '.join(detail['order_sequence'])}")
    print()
    
    # -------------------------------------------------------------------------
    # PART 3: Comparison
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("PART 3: Algorithm Comparison")
    print("=" * 80)
    print()
    
    print("Results Summary:")
    print("-" * 80)
    print(f"{'Algorithm':<30} {'Total Distance':<20} {'Routes Used':<15}")
    print("-" * 80)
    print(f"{'Greedy Nearest Neighbor':<30} "
          f"{greedy_summary['total_distance']:<20} "
          f"{greedy_summary['routes_used']:<15}")
    print(f"{'Simulated Annealing':<30} "
          f"{sa_summary['total_distance']:<20} "
          f"{sa_summary['routes_used']:<15}")
    print("-" * 80)
    
    # Calculate improvement
    improvement = greedy_summary['total_distance'] - sa_summary['total_distance']
    improvement_pct = (improvement / greedy_summary['total_distance'] * 100)
    
    print()
    if improvement > 0:
        print(f"✓ Simulated Annealing improved by {improvement:.2f} km "
              f"({improvement_pct:.1f}%)")
        print(f"  SA found a {improvement_pct:.1f}% better solution than Greedy!")
    elif improvement == 0:
        print(f"= Both algorithms found the same solution")
    else:
        print(f"⚠ Greedy performed better by {-improvement:.2f} km")
        print(f"  Note: This can happen on small instances or with unlucky SA runs")
    
    print()
    
    # -------------------------------------------------------------------------
    # PART 4: Convergence Analysis
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("PART 4: Convergence Analysis")
    print("=" * 80)
    print()
    
    print("Cost Evolution (Sample Points):")
    print("-" * 80)
    print(f"{'Iteration':<12} {'Temperature':<15} {'Current Cost':<15} {'Best Cost':<15}")
    print("-" * 80)
    
    # Show cost at different stages
    sample_points = [0, 100, 500, 1000, 1500, 2000, 2500]
    for i in sample_points:
        if i < len(sa.iteration_history):
            iter_data = sa.iteration_history[i]
            print(f"{iter_data['iteration']:<12} "
                  f"{iter_data['temperature']:<15.2f} "
                  f"{iter_data['current_cost']:<15.2f} "
                  f"{iter_data['best_cost']:<15.2f}")
    
    # Show the last iteration
    if sa.iteration_history:
        last_iter = sa.iteration_history[-1]
        print(f"{last_iter['iteration']:<12} "
              f"{last_iter['temperature']:<15.2f} "
              f"{last_iter['current_cost']:<15.2f} "
              f"{last_iter['best_cost']:<15.2f}")
    
    print()
    
    # Analyze acceptance patterns over time
    print("Acceptance Pattern Analysis:")
    print("-" * 80)
    
    # Divide iterations into quarters
    quarter_size = len(sa.iteration_history) // 4
    
    for q in range(4):
        start_idx = q * quarter_size
        end_idx = (q + 1) * quarter_size if q < 3 else len(sa.iteration_history)
        quarter_data = sa.iteration_history[start_idx:end_idx]
        
        accepted = sum(1 for d in quarter_data if d['accepted'])
        worse_accepted = sum(
            1 for d in quarter_data if d['accepted'] and d['delta_e'] > 0
        )
        acceptance_rate = accepted / len(quarter_data) if quarter_data else 0
        
        print(f"Quarter {q+1} (Iterations {start_idx}-{end_idx}):")
        print(f"  Acceptance Rate: {acceptance_rate:.1%}")
        print(f"  Worse Solutions Accepted: {worse_accepted}")
    
    print()
    
    # -------------------------------------------------------------------------
    # PART 5: Recommendations
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("PART 5: Key Insights & Recommendations")
    print("=" * 80)
    print()
    
    print("Algorithm Performance:")
    print("-" * 80)
    
    if improvement > 0:
        print("✓ Simulated Annealing successfully optimized the routes!")
        print(f"  The algorithm found a solution {improvement_pct:.1f}% better than greedy.")
    
    print()
    print("Simulated Annealing Characteristics Observed:")
    print("-" * 80)
    print(f"  • High Temperature Phase: Accepts {sa.iteration_history[0]['temperature']:.0f} "
          f"-> explores broadly")
    print(f"  • Exploration: Accepted {sa_stats['worse_accepted']} worse solutions "
          f"to escape local optima")
    print(f"  • Exploitation: Found best solution through {sa_stats['iterations_completed']} "
          f"iterations")
    print(f"  • Convergence: Final temperature {sa.iteration_history[-1]['temperature']:.4f} "
          f"ensures stability")
    
    print()
    print("Tips for Tuning SA:")
    print("-" * 80)
    print("  • Higher initial_temp → More exploration (try 2000-5000)")
    print("  • Slower cooling_rate → More thorough search (try 0.998-0.999)")
    print("  • More iterations → Better solution quality (try 5000-10000)")
    print("  • Faster cooling → Quicker convergence (try 0.990-0.995)")
    
    print()
    print("=" * 80)
    print("Demonstration Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
