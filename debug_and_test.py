"""
Debug & Test Script for Vehicle Routing Problem

This script thoroughly tests all components:
1. Data Structures (Order, Vehicle, Route)
2. Distance Functions (Haversine)
3. Greedy Algorithm (with manual verification)
"""

from src.models import Order, Vehicle, Route
from src.utils import haversine_distance, calculate_distance
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor


def test_data_structures():
    """
    Test 1: Data Structures
    Verify that objects store data correctly.
    """
    print("=" * 70)
    print("TEST 1: DATA STRUCTURES")
    print("=" * 70)
    print()
    
    # Test Order creation
    print("Testing Order Creation:")
    print("-" * 70)
    my_order = Order(
        id="TEST_ORDER_001",
        pickup_lat=40.7128,
        pickup_lon=-74.0060,
        dropoff_lat=40.7589,
        dropoff_lon=-73.9851
    )
    
    print(f"Order Object: {my_order}")
    print(f"  ID: {my_order.id}")
    print(f"  Pickup Location: ({my_order.pickup_lat}, {my_order.pickup_lon})")
    print(f"  Dropoff Location: ({my_order.dropoff_lat}, {my_order.dropoff_lon})")
    print(f"  Pickup Coordinates (method): {my_order.get_pickup_coordinates()}")
    print(f"  Dropoff Coordinates (method): {my_order.get_dropoff_coordinates()}")
    print()
    
    # Verify data is stored correctly
    assert my_order.id == "TEST_ORDER_001", "Order ID mismatch!"
    assert my_order.pickup_lat == 40.7128, "Pickup lat mismatch!"
    assert my_order.pickup_lon == -74.0060, "Pickup lon mismatch!"
    assert my_order.dropoff_lat == 40.7589, "Dropoff lat mismatch!"
    assert my_order.dropoff_lon == -73.9851, "Dropoff lon mismatch!"
    print("✓ Order stores data correctly!")
    print()
    
    # Test Vehicle creation
    print("Testing Vehicle Creation:")
    print("-" * 70)
    my_vehicle = Vehicle(
        id="TEST_VEHICLE_001",
        current_lat=40.7128,
        current_lon=-74.0060
    )
    
    print(f"Vehicle Object: {my_vehicle}")
    print(f"  ID: {my_vehicle.id}")
    print(f"  Current Location: ({my_vehicle.current_lat}, {my_vehicle.current_lon})")
    print(f"  Current Coordinates (method): {my_vehicle.get_current_coordinates()}")
    print()
    
    # Verify data is stored correctly
    assert my_vehicle.id == "TEST_VEHICLE_001", "Vehicle ID mismatch!"
    assert my_vehicle.current_lat == 40.7128, "Vehicle lat mismatch!"
    assert my_vehicle.current_lon == -74.0060, "Vehicle lon mismatch!"
    print("✓ Vehicle stores data correctly!")
    print()
    
    # Test Route creation
    print("Testing Route Creation:")
    print("-" * 70)
    my_route = Route(vehicle=my_vehicle)
    print(f"Route Object: {my_route}")
    print(f"  Vehicle: {my_route.vehicle.id}")
    print(f"  Orders: {my_route.orders}")
    print(f"  Total Orders: {my_route.get_total_orders()}")
    print(f"  Is Empty: {my_route.is_empty()}")
    print()
    
    # Add order to route
    my_route.add_order(my_order)
    print(f"After adding order:")
    print(f"  Orders: {[o.id for o in my_route.orders]}")
    print(f"  Total Orders: {my_route.get_total_orders()}")
    print(f"  Is Empty: {my_route.is_empty()}")
    print()
    
    # Verify route data
    assert my_route.vehicle.id == "TEST_VEHICLE_001", "Route vehicle mismatch!"
    assert len(my_route.orders) == 1, "Route order count mismatch!"
    assert my_route.orders[0].id == "TEST_ORDER_001", "Route order ID mismatch!"
    print("✓ Route stores data correctly!")
    print()


def test_distance_function():
    """
    Test 2: Distance Functions
    Verify distance calculations with known coordinates.
    """
    print("=" * 70)
    print("TEST 2: DISTANCE FUNCTIONS")
    print("=" * 70)
    print()
    
    # Test 1: Distance between identical points should be zero
    print("Test 2.1: Distance between identical points")
    print("-" * 70)
    point_a = (40.7128, -74.0060)  # Same point
    point_b = (40.7128, -74.0060)  # Same point
    
    distance = haversine_distance(point_a, point_b)
    print(f"Point A: {point_a}")
    print(f"Point B: {point_b}")
    print(f"Distance: {distance:.10f} km")
    print()
    
    assert distance == 0.0, f"Distance should be 0, got {distance}!"
    print("✓ Distance between identical points is zero!")
    print()
    
    # Test 2: Distance between New York and Los Angeles
    # Verified using: https://www.nhc.noaa.gov/gccalc.shtml
    # Expected: ~3936 km
    print("Test 2.2: Distance between New York and Los Angeles")
    print("-" * 70)
    new_york = (40.7128, -74.0060)
    los_angeles = (34.0522, -118.2437)
    
    distance_km = haversine_distance(new_york, los_angeles, unit='km')
    distance_miles = haversine_distance(new_york, los_angeles, unit='miles')
    
    print(f"New York: {new_york}")
    print(f"Los Angeles: {los_angeles}")
    print(f"Distance: {distance_km:.2f} km")
    print(f"Distance: {distance_miles:.2f} miles")
    print()
    
    # Verify against known values (approximately)
    # Real distance is about 3936 km / 2445 miles
    expected_km = 3936
    expected_miles = 2445
    tolerance_km = 50  # Allow 50 km tolerance
    tolerance_miles = 50  # Allow 50 miles tolerance
    
    assert abs(distance_km - expected_km) < tolerance_km, \
        f"Expected ~{expected_km} km, got {distance_km:.2f} km"
    assert abs(distance_miles - expected_miles) < tolerance_miles, \
        f"Expected ~{expected_miles} miles, got {distance_miles:.2f} miles"
    
    print(f"✓ Distance matches expected values (within {tolerance_km} km tolerance)!")
    print()
    
    # Test 3: Short distance (Manhattan to Times Square)
    print("Test 2.3: Distance from Lower Manhattan to Times Square")
    print("-" * 70)
    lower_manhattan = (40.7128, -74.0060)
    times_square = (40.7580, -73.9855)
    
    distance = haversine_distance(lower_manhattan, times_square)
    print(f"Lower Manhattan: {lower_manhattan}")
    print(f"Times Square: {times_square}")
    print(f"Distance: {distance:.2f} km")
    print()
    
    # Should be roughly 5-6 km
    assert 5.0 <= distance <= 6.0, \
        f"Expected ~5-6 km, got {distance:.2f} km"
    print("✓ Short distance calculation is reasonable!")
    print()
    
    # Test 4: Using calculate_distance wrapper
    print("Test 2.4: Using calculate_distance wrapper function")
    print("-" * 70)
    distance_wrapper = calculate_distance(40.7128, -74.0060, 40.7580, -73.9855)
    distance_direct = haversine_distance((40.7128, -74.0060), (40.7580, -73.9855))
    
    print(f"Distance (wrapper): {distance_wrapper:.2f} km")
    print(f"Distance (direct): {distance_direct:.2f} km")
    print()
    
    assert distance_wrapper == distance_direct, \
        "Wrapper function should produce same result!"
    print("✓ Wrapper function works correctly!")
    print()
    
    # Test 5: Different units
    print("Test 2.5: Testing different distance units")
    print("-" * 70)
    point1 = (40.7128, -74.0060)
    point2 = (40.7580, -73.9855)
    
    dist_km = haversine_distance(point1, point2, unit='km')
    dist_miles = haversine_distance(point1, point2, unit='miles')
    dist_meters = haversine_distance(point1, point2, unit='meters')
    dist_feet = haversine_distance(point1, point2, unit='feet')
    
    print(f"Kilometers: {dist_km:.2f} km")
    print(f"Miles: {dist_miles:.2f} miles")
    print(f"Meters: {dist_meters:.2f} m")
    print(f"Feet: {dist_feet:.2f} ft")
    print()
    
    # Verify conversions
    assert abs(dist_km - dist_miles / 0.621371) < 0.01, "km to miles conversion error!"
    assert abs(dist_km - dist_meters / 1000.0) < 0.01, "km to meters conversion error!"
    print("✓ All distance units work correctly!")
    print()


def test_greedy_algorithm():
    """
    Test 3: Greedy Algorithm
    Create a tiny dataset and manually verify the results.
    """
    print("=" * 70)
    print("TEST 3: GREEDY ALGORITHM")
    print("=" * 70)
    print()
    
    print("Creating a tiny, fixed dataset:")
    print("  2 vehicles, 4 orders")
    print("-" * 70)
    print()
    
    # Create 2 vehicles at different locations
    vehicles = [
        Vehicle(id="V1", current_lat=40.7128, current_lon=-74.0060),  # Lower Manhattan
        Vehicle(id="V2", current_lat=40.7580, current_lon=-73.9855),  # Times Square
    ]
    
    print("Vehicles:")
    for v in vehicles:
        print(f"  {v.id}: ({v.current_lat}, {v.current_lon})")
    print()
    
    # Create 4 orders
    orders = [
        # Order 1: Very close to V1
        Order(id="O1", pickup_lat=40.7130, pickup_lon=-74.0055,
              dropoff_lat=40.7150, dropoff_lon=-74.0040),
        
        # Order 2: Very close to V2
        Order(id="O2", pickup_lat=40.7582, pickup_lon=-73.9850,
              dropoff_lat=40.7600, dropoff_lon=-73.9840),
        
        # Order 3: Between V1 and V2, closer to V1
        Order(id="O3", pickup_lat=40.7300, pickup_lon=-74.0000,
              dropoff_lat=40.7320, dropoff_lon=-73.9990),
        
        # Order 4: Between V1 and V2, closer to V2
        Order(id="O4", pickup_lat=40.7500, pickup_lon=-73.9900,
              dropoff_lat=40.7520, dropoff_lon=-73.9890),
    ]
    
    print("Orders:")
    for o in orders:
        print(f"  {o.id}: Pickup ({o.pickup_lat}, {o.pickup_lon}) -> "
              f"Dropoff ({o.dropoff_lat}, {o.dropoff_lon})")
    print()
    
    # Manual calculation of expected behavior
    print("=" * 70)
    print("MANUAL CALCULATION")
    print("=" * 70)
    print()
    
    print("Round 1 - Vehicle V1:")
    print("  Calculate distances from V1 (40.7128, -74.0060) to all order pickups:")
    v1_pos = (40.7128, -74.0060)
    for o in orders:
        dist = haversine_distance(v1_pos, o.get_pickup_coordinates())
        print(f"    V1 -> {o.id} pickup: {dist:.4f} km")
    
    # V1 should pick O1 (closest)
    print(f"  Expected: V1 picks O1 (nearest)")
    print()
    
    print("Round 1 - Vehicle V2:")
    print("  Calculate distances from V2 (40.7580, -73.9855) to remaining pickups:")
    v2_pos = (40.7580, -73.9855)
    for o in orders[1:]:  # O1 already assigned
        dist = haversine_distance(v2_pos, o.get_pickup_coordinates())
        print(f"    V2 -> {o.id} pickup: {dist:.4f} km")
    
    # V2 should pick O2 (closest)
    print(f"  Expected: V2 picks O2 (nearest)")
    print()
    
    print("Round 2 - Vehicle V1:")
    print("  Current position: O1 dropoff (40.7150, -74.0040)")
    o1_dropoff = (40.7150, -74.0040)
    for o in [orders[2], orders[3]]:  # O3, O4 remaining
        dist = haversine_distance(o1_dropoff, o.get_pickup_coordinates())
        print(f"    O1 dropoff -> {o.id} pickup: {dist:.4f} km")
    
    # V1 should pick O3 (closer)
    print(f"  Expected: V1 picks O3 (nearest)")
    print()
    
    print("Round 2 - Vehicle V2:")
    print("  Current position: O2 dropoff (40.7600, -73.9840)")
    o2_dropoff = (40.7600, -73.9840)
    for o in [orders[3]]:  # Only O4 remaining
        dist = haversine_distance(o2_dropoff, o.get_pickup_coordinates())
        print(f"    O2 dropoff -> {o.id} pickup: {dist:.4f} km")
    
    # V2 should pick O4 (only option)
    print(f"  Expected: V2 picks O4 (only remaining)")
    print()
    
    print("Expected Final Assignment:")
    print("  V1 -> [O1, O3]")
    print("  V2 -> [O2, O4]")
    print()
    
    # Now run the actual algorithm
    print("=" * 70)
    print("RUNNING GREEDY ALGORITHM")
    print("=" * 70)
    print()
    
    algorithm = GreedyNearestNeighbor(distance_unit='km')
    routes, unassigned = algorithm.solve(vehicles, orders)
    
    print("Algorithm Results:")
    print("-" * 70)
    for route in routes:
        order_ids = [order.id for order in route.orders]
        print(f"  {route.vehicle.id} -> {order_ids}")
        
        # Show detailed distances
        total_dist = algorithm.calculate_total_distance(route)
        print(f"    Total Distance: {total_dist:.2f} km")
        
        # Show order sequence with distances
        current_pos = route.vehicle.get_current_coordinates()
        for i, order in enumerate(route.orders, 1):
            pickup = order.get_pickup_coordinates()
            dropoff = order.get_dropoff_coordinates()
            
            to_pickup = haversine_distance(current_pos, pickup)
            delivery = haversine_distance(pickup, dropoff)
            
            print(f"    {i}. {order.id}:")
            print(f"       To pickup: {to_pickup:.4f} km")
            print(f"       Delivery: {delivery:.4f} km")
            
            current_pos = dropoff
        print()
    
    print(f"Unassigned orders: {[o.id for o in unassigned]}")
    print()
    
    # Verify the results match our manual calculation
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print()
    
    # Check V1's route
    v1_route = routes[0]
    v1_order_ids = [o.id for o in v1_route.orders]
    print(f"V1 Expected: [O1, O3]")
    print(f"V1 Actual:   {v1_order_ids}")
    
    assert v1_route.vehicle.id == "V1", "V1 route mismatch!"
    assert len(v1_route.orders) == 2, f"V1 should have 2 orders, got {len(v1_route.orders)}"
    assert v1_order_ids == ["O1", "O3"], f"V1 orders should be [O1, O3], got {v1_order_ids}"
    print("✓ V1 route matches expected!")
    print()
    
    # Check V2's route
    v2_route = routes[1]
    v2_order_ids = [o.id for o in v2_route.orders]
    print(f"V2 Expected: [O2, O4]")
    print(f"V2 Actual:   {v2_order_ids}")
    
    assert v2_route.vehicle.id == "V2", "V2 route mismatch!"
    assert len(v2_route.orders) == 2, f"V2 should have 2 orders, got {len(v2_route.orders)}"
    assert v2_order_ids == ["O2", "O4"], f"V2 orders should be [O2, O4], got {v2_order_ids}"
    print("✓ V2 route matches expected!")
    print()
    
    # Check no unassigned orders
    assert len(unassigned) == 0, f"Should have no unassigned orders, got {len(unassigned)}"
    print("✓ All orders assigned!")
    print()
    
    # Get solution summary
    summary = algorithm.get_solution_summary(routes, unassigned)
    print("Solution Summary:")
    print("-" * 70)
    print(f"  Total Vehicles: {summary['total_vehicles']}")
    print(f"  Total Orders: {summary['total_orders']}")
    print(f"  Assigned Orders: {summary['assigned_orders']}")
    print(f"  Unassigned Orders: {summary['unassigned_orders']}")
    print(f"  Routes Used: {summary['routes_used']}")
    print(f"  Total Distance: {summary['total_distance']} km")
    print(f"  Average Distance per Route: {summary['average_distance_per_route']} km")
    print()
    
    assert summary['total_vehicles'] == 2
    assert summary['total_orders'] == 4
    assert summary['assigned_orders'] == 4
    assert summary['unassigned_orders'] == 0
    assert summary['routes_used'] == 2
    print("✓ Solution summary is correct!")
    print()


def main():
    """
    Run all debugging and testing.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  VEHICLE ROUTING PROBLEM - DEBUG & TEST SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    try:
        # Test 1: Data Structures
        test_data_structures()
        
        # Test 2: Distance Functions
        test_distance_function()
        
        # Test 3: Greedy Algorithm
        test_greedy_algorithm()
        
        # Final summary
        print("=" * 70)
        print("ALL TESTS PASSED! ✓")
        print("=" * 70)
        print()
        print("Summary:")
        print("  ✓ Data structures store data correctly")
        print("  ✓ Distance function calculates accurately")
        print("  ✓ Greedy algorithm produces expected results")
        print()
        print("The VRP implementation is working correctly!")
        print()
        
    except AssertionError as e:
        print()
        print("=" * 70)
        print("TEST FAILED! ✗")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        raise
    
    except Exception as e:
        print()
        print("=" * 70)
        print("UNEXPECTED ERROR! ✗")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        raise


if __name__ == "__main__":
    main()
