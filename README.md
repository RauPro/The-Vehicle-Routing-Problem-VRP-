# Vehicle Routing Problem (VRP)

A comprehensive solution for vehicle routing optimization.

## Project Structure

```
The Vehicle Routing Problem (VRP)/
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   └── greedy_nearest_neighbor.py  # Baseline greedy algorithm
│   ├── models/
│   │   ├── __init__.py
│   │   ├── order.py      # Order data structure
│   │   ├── vehicle.py    # Vehicle data structure
│   │   └── route.py      # Route data structure
│   └── utils/
│       ├── __init__.py
│       └── distance.py   # Distance calculation utilities
├── docs/
│   ├── distance_calculation.md  # Distance calculation documentation
│   └── greedy_algorithm.md      # Greedy algorithm documentation
├── main.py                      # Main entry point with algorithm demo
├── example_greedy_baseline.py   # Simple greedy algorithm example
├── test_distance.py             # Distance calculation tests
├── test_greedy_algorithm.py     # Greedy algorithm tests
├── GREEDY_ALGORITHM_SUMMARY.md  # Implementation summary
├── GREEDY_QUICK_REFERENCE.md    # Quick reference guide
├── GREEDY_VISUAL_GUIDE.md       # Visual algorithm guide
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Core Data Structures

### Order
Represents a delivery order with pickup and dropoff locations.

**Attributes:**
- `id` (str): Unique identifier for the order
- `pickup_lat` (float): Latitude of pickup location
- `pickup_lon` (float): Longitude of pickup location
- `dropoff_lat` (float): Latitude of dropoff location
- `dropoff_lon` (float): Longitude of dropoff location

### Vehicle
Represents a delivery vehicle with its current location.

**Attributes:**
- `id` (str): Unique identifier for the vehicle
- `current_lat` (float): Current latitude position
- `current_lon` (float): Current longitude position

### Route
Represents a route containing orders assigned to a vehicle.

**Attributes:**
- `vehicle` (Vehicle): The assigned vehicle
- `orders` (List[Order]): List of orders in the route

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using UV (recommended):
```bash
uv pip install -r requirements.txt
```

## Usage

Run the demonstration:
```bash
python main.py
```

### Example Usage

```python
from src.models import Order, Vehicle, Route
from src.utils import haversine_distance, calculate_distance

# Create an order
order = Order(
    id="ORD001",
    pickup_lat=40.7128,
    pickup_lon=-74.0060,
    dropoff_lat=40.7589,
    dropoff_lon=-73.9851
)

# Create a vehicle
vehicle = Vehicle(
    id="VEH001",
    current_lat=40.7128,
    current_lon=-74.0060
)

# Create a route
route = Route(vehicle=vehicle)
route.add_order(order)

print(f"Total orders: {route.get_total_orders()}")

# Calculate distances
vehicle_coords = vehicle.get_current_coordinates()
pickup_coords = order.get_pickup_coordinates()
dropoff_coords = order.get_dropoff_coordinates()

distance_to_pickup = haversine_distance(vehicle_coords, pickup_coords)
order_distance = haversine_distance(pickup_coords, dropoff_coords)

print(f"Distance to pickup: {distance_to_pickup:.2f} km")
print(f"Order distance: {order_distance:.2f} km")
```

### Distance Calculation

The project includes a robust distance calculation module using the **Haversine formula** for calculating great-circle distances between geographic coordinates.

```python
from src.utils import haversine_distance

# Calculate distance between two points
new_york = (40.7128, -74.0060)
los_angeles = (34.0522, -118.2437)

distance_km = haversine_distance(new_york, los_angeles)
print(f"{distance_km:.2f} km")  # Output: 3935.75 km

# Use different units
distance_miles = haversine_distance(new_york, los_angeles, unit='miles')
print(f"{distance_miles:.2f} miles")  # Output: 2445.56 miles
```

**Supported Units:**
- Kilometers (`'km'`, `'kilometers'`)
- Miles (`'miles'`)
- Meters (`'meters'`, `'metres'`, `'m'`)
- Feet (`'feet'`, `'ft'`)

For detailed documentation on distance calculations, see [docs/distance_calculation.md](docs/distance_calculation.md).

### Testing Distance Calculations

Run the comprehensive distance calculation tests:

```bash
python3 test_distance.py
```

### Testing Greedy Algorithm

Run the greedy algorithm tests:

```bash
python3 -m pytest test_greedy_algorithm.py -v
```

Or run all tests:

```bash
python3 -m pytest -v
```

## Features

- ✅ Type-safe data structures with full type hints
- ✅ Coordinate validation for all geographic points
- ✅ **Haversine distance calculation** for real-world accuracy
- ✅ Support for multiple distance units (km, miles, meters, feet)
- ✅ **Greedy Nearest Neighbor baseline algorithm** for route optimization
- ✅ Comprehensive route metrics and analysis
- ✅ Round-robin vehicle assignment strategy
- ✅ Clean, modular architecture
- ✅ Comprehensive documentation with visual guides
- ✅ Edge case handling and input validation
- ✅ Extensive test coverage

## Algorithms

### Greedy Nearest Neighbor (Baseline)

A simple, fast baseline algorithm that assigns orders to vehicles using a greedy nearest neighbor heuristic.

**Quick Example:**

```python
from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# Create vehicles and orders
vehicles = [
    Vehicle("V1", 40.7128, -74.0060),
    Vehicle("V2", 40.7580, -73.9855),
]

orders = [
    Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
    Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
    Order("O3", 40.7831, -73.9712, 40.7489, -73.9680),
]

# Solve using greedy algorithm
algorithm = GreedyNearestNeighbor(distance_unit='km')
routes, unassigned = algorithm.solve(vehicles, orders)

# Get solution summary
summary = algorithm.get_solution_summary(routes, unassigned)
print(f"Total distance: {summary['total_distance']} km")
print(f"Routes used: {summary['routes_used']}")
```

**Algorithm Characteristics:**
- **Time Complexity**: O(v × o²) where v = vehicles, o = orders
- **Space Complexity**: O(v + o)
- **Approach**: Iteratively assigns nearest unassigned order to each vehicle
- **Distribution**: Round-robin across all vehicles
- **Best For**: Baseline comparisons, quick solutions, small-medium problems

**Documentation:**
- 📚 [Full Documentation](docs/greedy_algorithm.md)
- 🚀 [Quick Reference](GREEDY_QUICK_REFERENCE.md)
- 📊 [Visual Guide](GREEDY_VISUAL_GUIDE.md)
- ✅ [Implementation Summary](GREEDY_ALGORITHM_SUMMARY.md)

**Run the Demo:**
```bash
python3 main.py
```

**Run Simple Example:**
```bash
python3 example_greedy_baseline.py
```

## Development

This project follows PEP 8 style guidelines and uses Python dataclasses for clean, maintainable code.

## License

MIT License
