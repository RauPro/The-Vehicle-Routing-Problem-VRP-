"""
Test script for distance calculation functions.

This script demonstrates the usage of the Haversine distance formula
with various examples and edge cases.
"""

from src.utils import haversine_distance, calculate_distance


def test_distance_calculations():
    """
    Test various distance calculations with real-world examples.
    """
    print("=" * 60)
    print("Distance Calculation Tests")
    print("=" * 60)
    print()
    
    # Test 1: Major cities distance
    print("Test 1: Distance between major cities")
    print("-" * 60)
    new_york = (40.7128, -74.0060)
    los_angeles = (34.0522, -118.2437)
    
    distance_km = haversine_distance(new_york, los_angeles)
    distance_miles = haversine_distance(new_york, los_angeles, 'miles')
    
    print(f"New York to Los Angeles:")
    print(f"  Coordinates: {new_york} -> {los_angeles}")
    print(f"  Distance: {distance_km:.2f} km ({distance_miles:.2f} miles)")
    print()
    
    # Test 2: Short distance
    print("Test 2: Short distance (within a city)")
    print("-" * 60)
    point_a = (40.7589, -73.9851)  # Times Square area
    point_b = (40.7614, -73.9776)  # Central Park
    
    distance = calculate_distance(
        point_a[0], point_a[1],
        point_b[0], point_b[1]
    )
    distance_meters = calculate_distance(
        point_a[0], point_a[1],
        point_b[0], point_b[1],
        unit='meters'
    )
    
    print(f"Times Square to Central Park:")
    print(f"  Distance: {distance:.3f} km ({distance_meters:.2f} meters)")
    print()
    
    # Test 3: International distance
    print("Test 3: International distance")
    print("-" * 60)
    london = (51.5074, -0.1278)
    paris = (48.8566, 2.3522)
    tokyo = (35.6762, 139.6503)
    
    london_paris = haversine_distance(london, paris, 'km')
    london_tokyo = haversine_distance(london, tokyo, 'km')
    paris_tokyo = haversine_distance(paris, tokyo, 'km')
    
    print(f"London to Paris: {london_paris:.2f} km")
    print(f"London to Tokyo: {london_tokyo:.2f} km")
    print(f"Paris to Tokyo: {paris_tokyo:.2f} km")
    print()
    
    # Test 4: Same location (edge case)
    print("Test 4: Same location (edge case)")
    print("-" * 60)
    same_point = (40.7128, -74.0060)
    distance_same = haversine_distance(same_point, same_point)
    print(f"Distance from point to itself: {distance_same:.10f} km")
    print()
    
    # Test 5: All supported units
    print("Test 5: All supported units")
    print("-" * 60)
    coord1 = (40.7128, -74.0060)
    coord2 = (40.7589, -73.9851)
    
    print(f"Distance from {coord1} to {coord2}:")
    print(f"  Kilometers: {haversine_distance(coord1, coord2, 'km'):.2f} km")
    print(f"  Miles: {haversine_distance(coord1, coord2, 'miles'):.2f} miles")
    print(f"  Meters: {haversine_distance(coord1, coord2, 'meters'):.2f} m")
    print(f"  Feet: {haversine_distance(coord1, coord2, 'feet'):.2f} ft")
    print()
    
    # Test 6: Error handling
    print("Test 6: Error handling")
    print("-" * 60)
    
    # Test invalid latitude
    try:
        invalid_coord = (91.0, 0.0)  # Latitude > 90
        valid_coord = (40.0, -74.0)
        haversine_distance(invalid_coord, valid_coord)
    except ValueError as e:
        print(f"✓ Caught expected error for invalid latitude: {e}")
    
    # Test invalid longitude
    try:
        invalid_coord = (40.0, 181.0)  # Longitude > 180
        valid_coord = (40.0, -74.0)
        haversine_distance(invalid_coord, valid_coord)
    except ValueError as e:
        print(f"✓ Caught expected error for invalid longitude: {e}")
    
    # Test invalid unit
    try:
        coord1 = (40.0, -74.0)
        coord2 = (41.0, -73.0)
        haversine_distance(coord1, coord2, unit='invalid')
    except ValueError as e:
        print(f"✓ Caught expected error for invalid unit: {e}")
    
    print()
    print("=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    test_distance_calculations()
