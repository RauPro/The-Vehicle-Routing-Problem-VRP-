# Distance Calculation Module

## Overview

The distance calculation module provides functions to calculate the great-circle distance between two geographic coordinate points using the **Haversine formula**. This is essential for vehicle routing problems where accurate real-world distances are needed.

## What is the Haversine Formula?

The Haversine formula calculates the shortest distance between two points on a sphere given their longitudes and latitudes. It's particularly useful for calculating distances on Earth's surface.

### Mathematical Formula

```
a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
c = 2 * atan2(√a, √(1−a))
d = R * c
```

Where:
- φ1, φ2: Latitude of point 1 and latitude of point 2 (in radians)
- Δφ: Difference in latitude
- Δλ: Difference in longitude
- R: Earth's radius (mean radius = 6,371 km)
- d: Distance between the two points

## Functions

### `haversine_distance(coord1, coord2, unit='km')`

Calculate the great-circle distance between two coordinate points.

**Parameters:**
- `coord1` (Tuple[float, float]): First coordinate as (latitude, longitude) in decimal degrees
- `coord2` (Tuple[float, float]): Second coordinate as (latitude, longitude) in decimal degrees
- `unit` (str): Unit for the result. Options:
  - `'km'` or `'kilometers'`: Kilometers (default)
  - `'miles'`: Miles
  - `'meters'`, `'metres'`, or `'m'`: Meters
  - `'feet'` or `'ft'`: Feet

**Returns:**
- `float`: Distance between the two coordinates in the specified unit

**Raises:**
- `ValueError`: If coordinates are out of valid range (-90 to 90 for latitude, -180 to 180 for longitude)
- `ValueError`: If unit is invalid

**Example:**
```python
from src.utils import haversine_distance

# Distance between New York and Los Angeles
ny = (40.7128, -74.0060)
la = (34.0522, -118.2437)

distance_km = haversine_distance(ny, la)
print(f"{distance_km:.2f} km")  # Output: 3935.75 km

distance_miles = haversine_distance(ny, la, unit='miles')
print(f"{distance_miles:.2f} miles")  # Output: 2445.56 miles
```

### `calculate_distance(lat1, lon1, lat2, lon2, unit='km')`

Convenience wrapper that accepts individual latitude and longitude values.

**Parameters:**
- `lat1` (float): Latitude of the first point in decimal degrees
- `lon1` (float): Longitude of the first point in decimal degrees
- `lat2` (float): Latitude of the second point in decimal degrees
- `lon2` (float): Longitude of the second point in decimal degrees
- `unit` (str): Unit for the result (same options as `haversine_distance`)

**Returns:**
- `float`: Distance between the two points in the specified unit

**Example:**
```python
from src.utils import calculate_distance

# Distance between two points
distance = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
print(f"{distance:.2f} km")  # Output: 3935.75 km
```

## Usage Examples

### Basic Usage

```python
from src.utils import haversine_distance, calculate_distance

# Using tuple coordinates
point1 = (40.7128, -74.0060)  # New York
point2 = (51.5074, -0.1278)   # London

distance = haversine_distance(point1, point2)
print(f"Distance: {distance:.2f} km")

# Using individual coordinates
distance = calculate_distance(40.7128, -74.0060, 51.5074, -0.1278)
print(f"Distance: {distance:.2f} km")
```

### Integration with VRP Models

```python
from src.models import Vehicle, Order
from src.utils import haversine_distance

# Create a vehicle and order
vehicle = Vehicle(id="VEH001", current_lat=40.7128, current_lon=-74.0060)
order = Order(
    id="ORD001",
    pickup_lat=40.7589,
    pickup_lon=-73.9851,
    dropoff_lat=40.7614,
    dropoff_lon=-73.9776
)

# Calculate distance from vehicle to pickup
vehicle_coords = vehicle.get_current_coordinates()
pickup_coords = order.get_pickup_coordinates()
distance_to_pickup = haversine_distance(vehicle_coords, pickup_coords)
print(f"Distance to pickup: {distance_to_pickup:.2f} km")

# Calculate order distance (pickup to dropoff)
dropoff_coords = order.get_dropoff_coordinates()
order_distance = haversine_distance(pickup_coords, dropoff_coords)
print(f"Order distance: {order_distance:.2f} km")
```

### Multiple Units

```python
from src.utils import haversine_distance

coord1 = (40.7128, -74.0060)
coord2 = (40.7589, -73.9851)

print(f"Kilometers: {haversine_distance(coord1, coord2, 'km'):.2f} km")
print(f"Miles: {haversine_distance(coord1, coord2, 'miles'):.2f} miles")
print(f"Meters: {haversine_distance(coord1, coord2, 'meters'):.2f} m")
print(f"Feet: {haversine_distance(coord1, coord2, 'feet'):.2f} ft")
```

## Accuracy and Limitations

### Accuracy
- The Haversine formula assumes Earth is a perfect sphere with a mean radius of 6,371 km
- Actual distances may vary slightly (±0.5%) due to Earth's ellipsoidal shape
- For most vehicle routing applications, this accuracy is sufficient

### When to Use
✅ **Good for:**
- Short to medium distances (< 1000 km)
- General vehicle routing and logistics
- Quick distance estimates
- Applications not requiring sub-meter precision

❌ **Consider alternatives for:**
- High-precision geodetic applications
- Very long distances (> 10,000 km)
- Applications requiring accuracy better than 0.5%

### Alternative: Vincenty Formula
For higher accuracy, consider the Vincenty formula which accounts for Earth's ellipsoidal shape. However, it's more computationally expensive and rarely necessary for vehicle routing.

## Performance Considerations

- **Computation Time**: The Haversine formula is very fast (microseconds per calculation)
- **Scalability**: Suitable for calculating millions of distances
- **Memory**: Minimal memory footprint

## Error Handling

The module includes comprehensive validation:

```python
from src.utils import haversine_distance

# Invalid latitude (must be -90 to 90)
try:
    haversine_distance((91.0, 0.0), (40.0, -74.0))
except ValueError as e:
    print(f"Error: {e}")

# Invalid longitude (must be -180 to 180)
try:
    haversine_distance((40.0, 181.0), (40.0, -74.0))
except ValueError as e:
    print(f"Error: {e}")

# Invalid unit
try:
    haversine_distance((40.0, -74.0), (41.0, -73.0), unit='invalid')
except ValueError as e:
    print(f"Error: {e}")
```

## Testing

Run the test suite to verify distance calculations:

```bash
python3 test_distance.py
```

The test suite includes:
- Major city distances
- Short distances (within a city)
- International distances
- Edge cases (same location)
- All supported units
- Error handling validation

## References

- [Haversine Formula - Wikipedia](https://en.wikipedia.org/wiki/Haversine_formula)
- [Great-circle distance](https://en.wikipedia.org/wiki/Great-circle_distance)
- [Geographic coordinate system](https://en.wikipedia.org/wiki/Geographic_coordinate_system)
