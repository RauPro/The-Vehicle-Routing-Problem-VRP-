"""
Detailed Debugging Script for Simulated Annealing

This script provides comprehensive debugging output for the SA algorithm,
showing every iteration with detailed acceptance logic.
"""

import random
from src.models import Order, Vehicle
from src.algorithms import SimulatedAnnealing, GreedyNearestNeighbor


def debug_cost_function():
    """
    DEBUG TEST 1: Cost Function Verification
    Test with simple, handcrafted solution to verify correct distance calculation.
    """
    print("=" * 80)
    print("DEBUG TEST 1: Cost Function Verification")
    print("=" * 80)
    print()
    
    # Create simple test case with known distances
    vehicles = [
        Vehicle(id="VEH001", current_lat=40.0, current_lon=-74.0),
        Vehicle(id="VEH002", current_lat=41.0, current_lon=-73.0)
    ]
    
    orders = [
        Order(id="ORD001", pickup_lat=40.1, pickup_lon=-74.1,
              dropoff_lat=40.2, dropoff_lon=-74.2),
        Order(id="ORD002", pickup_lat=40.3, pickup_lon=-74.3,
              dropoff_lat=40.4, dropoff_lon=-74.4),
    ]
    
    # Handcrafted solution: Vehicle 0 → Order 0, Vehicle 1 → Order 1
    solution = [[orders[0]], [orders[1]]]
    
    print("Handcrafted Solution:")
    for i, route in enumerate(solution):
        print(f"  Vehicle {i}: {[o.id for o in route]}")
    print()
    
    # Calculate cost step by step
    sa = SimulatedAnnealing()
    
    print("Cost Breakdown:")
    print("-" * 80)
    
    from src.utils import haversine_distance
    
    total = 0.0
    for i, route_orders in enumerate(solution):
        vehicle = vehicles[i]
        print(f"\nVehicle {i} ({vehicle.id}):")
        print(f"  Start Position: ({vehicle.current_lat}, {vehicle.current_lon})")
        
        route_cost = 0.0
        current_pos = vehicle.get_current_coordinates()
        
        for j, order in enumerate(route_orders):
            print(f"\n  Order {j+1} ({order.id}):")
            
            # To pickup
            pickup = order.get_pickup_coordinates()
            dist_to_pickup = haversine_distance(current_pos, pickup)
            route_cost += dist_to_pickup
            print(f"    Current → Pickup: {dist_to_pickup:.4f} km")
            
            # Pickup to dropoff
            dropoff = order.get_dropoff_coordinates()
            dist_delivery = haversine_distance(pickup, dropoff)
            route_cost += dist_delivery
            print(f"    Pickup → Dropoff: {dist_delivery:.4f} km")
            
            current_pos = dropoff
        
        print(f"\n  Vehicle {i} Total: {route_cost:.4f} km")
        total += route_cost
    
    print()
    print("=" * 80)
    print(f"TOTAL COST: {total:.4f} km")
    print("=" * 80)
    
    # Verify with SA cost function
    calculated_cost = sa.calculate_total_cost(solution, vehicles)
    print(f"SA Cost Function: {calculated_cost:.4f} km")
    
    if abs(calculated_cost - total) < 0.01:
        print("✓ Cost function verification PASSED!")
    else:
        print("✗ Cost function verification FAILED!")
        print(f"  Expected: {total:.4f}, Got: {calculated_cost:.4f}")
    
    print()


def debug_neighbor_function():
    """
    DEBUG TEST 2: Neighbor Function Verification
    Generate 20 neighbors and verify all changes are valid.
    """
    print("=" * 80)
    print("DEBUG TEST 2: Neighbor Function Verification")
    print("=" * 80)
    print()
    
    # Create test scenario
    vehicles = [
        Vehicle(id="VEH001", current_lat=40.7128, current_lon=-74.0060),
        Vehicle(id="VEH002", current_lat=40.7580, current_lon=-73.9855),
    ]
    
    orders = [
        Order(id="ORD001", pickup_lat=40.7128, pickup_lon=-74.0060,
              dropoff_lat=40.7589, dropoff_lon=-73.9851),
        Order(id="ORD002", pickup_lat=40.7580, pickup_lon=-73.9855,
              dropoff_lat=40.7614, dropoff_lon=-73.9776),
        Order(id="ORD003", pickup_lat=40.7831, pickup_lon=-73.9712,
              dropoff_lat=40.7489, dropoff_lon=-73.9680),
        Order(id="ORD004", pickup_lat=40.7061, pickup_lon=-73.9969,
              dropoff_lat=40.7306, dropoff_lon=-73.9866),
    ]
    
    # Initial solution
    initial_solution = [[orders[0], orders[1]], [orders[2], orders[3]]]
    
    print("Initial Solution:")
    for i, route in enumerate(initial_solution):
        print(f"  Vehicle {i}: {[o.id for o in route]}")
    print()
    
    sa = SimulatedAnnealing()
    
    print("Generating 20 Neighbor Solutions:")
    print("=" * 80)
    
    all_order_ids = {order.id for order in orders}
    
    for i in range(20):
        neighbor = sa.get_neighbor(initial_solution)
        
        print(f"\nNeighbor {i+1}:")
        print("-" * 80)
        
        # Show the neighbor
        for j, route in enumerate(neighbor):
            print(f"  Vehicle {j}: {[o.id for o in route]}")
        
        # Verify integrity
        neighbor_order_ids = set()
        for route in neighbor:
            for order in route:
                neighbor_order_ids.add(order.id)
        
        # Check if all orders present
        if neighbor_order_ids == all_order_ids:
            print("  ✓ All orders present")
        else:
            print("  ✗ INTEGRITY VIOLATION!")
            print(f"    Missing: {all_order_ids - neighbor_order_ids}")
            print(f"    Extra: {neighbor_order_ids - all_order_ids}")
        
        # Check if different from original
        is_different = neighbor != initial_solution
        if is_different:
            print("  ✓ Solution changed")
        else:
            print("  = Same as original (rare but valid)")
    
    print()


def debug_sa_loop_detailed():
    """
    DEBUG TEST 3: SA Loop with Detailed Logging
    Shows iteration-by-iteration what's happening with acceptance decisions.
    """
    print("=" * 80)
    print("DEBUG TEST 3: SA Loop - Detailed Iteration Log")
    print("=" * 80)
    print()
    
    # Set seed for reproducibility
    random.seed(42)
    
    # Create test scenario
    vehicles = [
        Vehicle(id="VEH001", current_lat=40.7128, current_lon=-74.0060),
        Vehicle(id="VEH002", current_lat=40.7580, current_lon=-73.9855),
    ]
    
    orders = [
        Order(id="ORD001", pickup_lat=40.7128, pickup_lon=-74.0060,
              dropoff_lat=40.7589, dropoff_lon=-73.9851),
        Order(id="ORD002", pickup_lat=40.7580, pickup_lon=-73.9855,
              dropoff_lat=40.7614, dropoff_lon=-73.9776),
        Order(id="ORD003", pickup_lat=40.7831, pickup_lon=-73.9712,
              dropoff_lat=40.7489, dropoff_lon=-73.9680),
        Order(id="ORD004", pickup_lat=40.7061, pickup_lon=-73.9969,
              dropoff_lat=40.7306, dropoff_lon=-73.9866),
        Order(id="ORD005", pickup_lat=40.7549, pickup_lon=-73.9840,
              dropoff_lat=40.7829, dropoff_lon=-73.9654),
    ]
    
    print("Configuration:")
    print("-" * 80)
    initial_temp = 500.0
    final_temp = 1.0
    cooling_rate = 0.995
    max_iterations = 100  # Limited for debugging
    
    print(f"  Initial Temperature: {initial_temp}")
    print(f"  Final Temperature: {final_temp}")
    print(f"  Cooling Rate: {cooling_rate}")
    print(f"  Max Iterations: {max_iterations}")
    print()
    
    print("Running SA with Detailed Logging:")
    print("=" * 80)
    print()
    
    # Run with verbose mode
    sa = SimulatedAnnealing(
        initial_temp=initial_temp,
        final_temp=final_temp,
        cooling_rate=cooling_rate,
        max_iterations=max_iterations,
        distance_unit='km',
        verbose=True  # This will show all iterations
    )
    
    routes, best_cost, stats = sa.solve(vehicles, orders)
    
    print()
    print("=" * 80)
    print("Analysis of Acceptance Pattern:")
    print("=" * 80)
    print()
    
    # Analyze first 20 iterations (high temp)
    early_iters = sa.iteration_history[:20]
    early_worse = sum(1 for it in early_iters if it['accepted'] and it['delta_e'] > 0)
    early_accept_rate = sum(1 for it in early_iters if it['accepted']) / len(early_iters)
    
    print("EARLY PHASE (First 20 iterations - HIGH TEMPERATURE):")
    print(f"  Temperature Range: {early_iters[0]['temperature']:.2f} → {early_iters[-1]['temperature']:.2f}")
    print(f"  Acceptance Rate: {early_accept_rate:.1%}")
    print(f"  Worse Solutions Accepted: {early_worse}/{len(early_iters)}")
    print(f"  ✓ Expected: Many worse solutions accepted (exploration)")
    print()
    
    # Analyze last 20 iterations (low temp)
    late_iters = sa.iteration_history[-20:]
    late_worse = sum(1 for it in late_iters if it['accepted'] and it['delta_e'] > 0)
    late_accept_rate = sum(1 for it in late_iters if it['accepted']) / len(late_iters)
    
    print("LATE PHASE (Last 20 iterations - LOW TEMPERATURE):")
    print(f"  Temperature Range: {late_iters[0]['temperature']:.2f} → {late_iters[-1]['temperature']:.2f}")
    print(f"  Acceptance Rate: {late_accept_rate:.1%}")
    print(f"  Worse Solutions Accepted: {late_worse}/{len(late_iters)}")
    print(f"  ✓ Expected: Few/no worse solutions accepted (exploitation)")
    print()
    
    print("OVERALL STATISTICS:")
    print("-" * 80)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


def debug_sa_vs_greedy():
    """
    DEBUG TEST 4: SA vs Greedy Comparison
    Verify that SA beats greedy baseline.
    """
    print("=" * 80)
    print("DEBUG TEST 4: SA vs Greedy - Head-to-Head Comparison")
    print("=" * 80)
    print()
    
    # Set seed
    random.seed(42)
    
    # Create test scenario
    vehicles = [
        Vehicle(id="VEH001", current_lat=40.7128, current_lon=-74.0060),
        Vehicle(id="VEH002", current_lat=40.7580, current_lon=-73.9855),
    ]
    
    orders = [
        Order(id="ORD001", pickup_lat=40.7128, pickup_lon=-74.0060,
              dropoff_lat=40.7589, dropoff_lon=-73.9851),
        Order(id="ORD002", pickup_lat=40.7580, pickup_lon=-73.9855,
              dropoff_lat=40.7614, dropoff_lon=-73.9776),
        Order(id="ORD003", pickup_lat=40.7831, pickup_lon=-73.9712,
              dropoff_lat=40.7489, dropoff_lon=-73.9680),
        Order(id="ORD004", pickup_lat=40.7061, pickup_lon=-73.9969,
              dropoff_lat=40.7306, dropoff_lon=-73.9866),
        Order(id="ORD005", pickup_lat=40.7549, pickup_lon=-73.9840,
              dropoff_lat=40.7829, dropoff_lon=-73.9654),
        Order(id="ORD006", pickup_lat=40.7282, pickup_lon=-73.9942,
              dropoff_lat=40.7484, dropoff_lon=-73.9857),
    ]
    
    print("Test Scenario:")
    print(f"  Vehicles: {len(vehicles)}")
    print(f"  Orders: {len(orders)}")
    print()
    
    # Run Greedy
    print("STEP 1: Running Greedy Nearest Neighbor...")
    print("-" * 80)
    greedy = GreedyNearestNeighbor(distance_unit='km')
    greedy_routes, _ = greedy.solve(vehicles, orders)
    greedy_cost = sum(greedy.calculate_total_distance(route) for route in greedy_routes)
    
    print(f"Greedy Solution:")
    for route in greedy_routes:
        if not route.is_empty():
            print(f"  {route.vehicle.id}: {[o.id for o in route.orders]}")
    print(f"Greedy Total Cost: {greedy_cost:.2f} km")
    print()
    
    # Run SA
    print("STEP 2: Running Simulated Annealing...")
    print("-" * 80)
    sa = SimulatedAnnealing(
        initial_temp=1000.0,
        final_temp=1.0,
        cooling_rate=0.995,
        max_iterations=2000,
        distance_unit='km',
        verbose=False
    )
    
    sa_routes, sa_cost, sa_stats = sa.solve(vehicles, orders)
    
    print(f"SA Solution:")
    for route in sa_routes:
        if not route.is_empty():
            print(f"  {route.vehicle.id}: {[o.id for o in route.orders]}")
    print(f"SA Total Cost: {sa_cost:.2f} km")
    print()
    
    # Compare
    print("STEP 3: Comparison")
    print("=" * 80)
    print(f"{'Algorithm':<30} {'Cost (km)':<15} {'Result':<20}")
    print("-" * 80)
    print(f"{'Greedy Nearest Neighbor':<30} {greedy_cost:<15.2f} {'Baseline':<20}")
    print(f"{'Simulated Annealing':<30} {sa_cost:<15.2f} ", end="")
    
    improvement = greedy_cost - sa_cost
    improvement_pct = (improvement / greedy_cost * 100) if greedy_cost > 0 else 0
    
    if improvement > 0:
        print(f"✓ Better by {improvement_pct:.1f}%")
        print()
        print(f"✓✓✓ SUCCESS! SA beat Greedy by {improvement:.2f} km ({improvement_pct:.1f}%)")
    elif improvement == 0:
        print(f"= Equal")
        print()
        print(f"= TIED: Both algorithms found the same solution")
    else:
        print(f"✗ Worse")
        print()
        print(f"✗✗✗ PROBLEM! SA is worse than Greedy by {-improvement:.2f} km")
        print(f"    This indicates a potential bug!")
    
    print()
    
    # Show improvement details
    print("Detailed Analysis:")
    print("-" * 80)
    print(f"  Greedy Cost: {greedy_cost:.2f} km")
    print(f"  SA Initial Cost: {sa_stats['initial_cost']:.2f} km")
    print(f"  SA Final Cost: {sa_stats['final_cost']:.2f} km")
    print(f"  SA Improvement from Initial: {sa_stats['improvement']:.2f} km ({sa_stats['improvement_percentage']:.1f}%)")
    print(f"  SA vs Greedy: {improvement:.2f} km ({improvement_pct:.1f}%)")
    print()


def main():
    """
    Run all debugging tests.
    """
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "SIMULATED ANNEALING - DETAILED DEBUG SUITE" + " " * 21 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Test 1: Cost Function
    debug_cost_function()
    input("Press Enter to continue to Test 2...")
    print("\n\n")
    
    # Test 2: Neighbor Function
    debug_neighbor_function()
    input("Press Enter to continue to Test 3...")
    print("\n\n")
    
    # Test 3: SA Loop
    debug_sa_loop_detailed()
    input("Press Enter to continue to Test 4...")
    print("\n\n")
    
    # Test 4: SA vs Greedy
    debug_sa_vs_greedy()
    
    print()
    print("=" * 80)
    print("ALL DEBUGGING TESTS COMPLETE!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
