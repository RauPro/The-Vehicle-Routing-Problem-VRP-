# Greedy Nearest Neighbor Algorithm

## Overview

The **Greedy Nearest Neighbor** algorithm is a simple, baseline heuristic for solving the Vehicle Routing Problem (VRP). It serves as a "dumb" algorithm that can be used to compare against more sophisticated routing solutions.

## Algorithm Description

### Concept

The algorithm uses a greedy approach where, for each vehicle, it iteratively assigns the closest unassigned order pickup point until all orders are assigned. This is a straightforward implementation of the Nearest Neighbor heuristic.

### Logic

1. **Initialization**
   - Create a route for each available vehicle
   - Mark all orders as unassigned
   - Start with the first vehicle

2. **Assignment Loop**
   - For the current vehicle:
     - Determine the current position:
       - If no orders assigned yet: use vehicle's starting location
       - If orders already assigned: use the dropoff location of the last order
     - Find the nearest unassigned order's pickup point
     - Assign that order to the vehicle's route
     - Mark the order as assigned
   - Move to the next vehicle (round-robin)
   - Repeat until all orders are assigned

3. **Result**
   - Return the list of routes with assigned orders
   - Return any unassigned orders (if applicable)

## Implementation

### Class: `GreedyNearestNeighbor`

Located in: `src/algorithms/greedy_nearest_neighbor.py`

#### Constructor

```python
algorithm = GreedyNearestNeighbor(distance_unit='km')
```

**Parameters:**
- `distance_unit` (str): Unit for distance calculations. Options: 'km', 'miles', 'meters', 'feet'. Default: 'km'

#### Main Methods

##### `solve(vehicles, orders)`

Assigns orders to vehicles using the greedy nearest neighbor approach.

**Parameters:**
- `vehicles` (List[Vehicle]): List of available vehicles
- `orders` (List[Order]): List of orders to be assigned

**Returns:**
- Tuple[List[Route], List[Order]]: Routes with assigned orders and list of unassigned orders

**Example:**
```python
from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# Create vehicles and orders
vehicles = [Vehicle("V1", 40.7128, -74.0060)]
orders = [
    Order("O1", 40.7580, -73.9855, 40.7614, -73.9776),
    Order("O2", 40.7831, -73.9712, 40.7489, -73.9680),
]

# Solve
algorithm = GreedyNearestNeighbor()
routes, unassigned = algorithm.solve(vehicles, orders)
```

##### `calculate_total_distance(route)`

Calculate the total distance for a complete route.

**Parameters:**
- `route` (Route): The route to calculate distance for

**Returns:**
- float: Total distance in the configured unit

**Example:**
```python
distance = algorithm.calculate_total_distance(routes[0])
print(f"Total distance: {distance:.2f} km")
```

##### `get_solution_summary(routes, unassigned_orders)`

Generate a comprehensive summary of the routing solution.

**Parameters:**
- `routes` (List[Route]): List of routes with assigned orders
- `unassigned_orders` (List[Order]): List of unassigned orders

**Returns:**
- dict: Summary statistics including:
  - `total_vehicles`: Number of vehicles
  - `total_orders`: Total number of orders
  - `assigned_orders`: Number of assigned orders
  - `unassigned_orders`: Number of unassigned orders
  - `routes_used`: Number of routes with at least one order
  - `total_distance`: Total distance across all routes
  - `average_distance_per_route`: Average distance per used route
  - `distance_unit`: Unit used for distances
  - `route_details`: List of details for each route

**Example:**
```python
summary = algorithm.get_solution_summary(routes, unassigned)
print(f"Total distance: {summary['total_distance']} {summary['distance_unit']}")
```

## Characteristics

### Advantages

1. **Simple**: Easy to understand and implement
2. **Fast**: Low computational complexity
3. **Baseline**: Provides a reference point for comparison
4. **Deterministic**: Given the same input, produces the same output
5. **No External Dependencies**: Uses only basic distance calculations

### Limitations

1. **Locally Optimal**: Makes greedy choices without considering global optimization
2. **Order-Dependent**: Results can vary based on vehicle order
3. **No Backtracking**: Once an order is assigned, it's not reconsidered
4. **Simple Distance Metric**: Only considers distance, not time windows or capacity
5. **Sub-optimal Solutions**: Generally produces routes longer than optimal

### Time Complexity

- **Worst Case**: O(v × o²) where v = number of vehicles, o = number of orders
- **Space Complexity**: O(v + o) for storing routes and orders

## Usage Examples

### Example 1: Simple Single Vehicle

```python
from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# Create vehicle and orders
vehicles = [Vehicle("V1", 40.7128, -74.0060)]
orders = [
    Order("O1", 40.7580, -73.9855, 40.7614, -73.9776),
    Order("O2", 40.7831, -73.9712, 40.7489, -73.9680),
    Order("O3", 40.7061, -73.9969, 40.7306, -73.9866),
]

# Solve
algorithm = GreedyNearestNeighbor(distance_unit='km')
routes, unassigned = algorithm.solve(vehicles, orders)

# Display results
for route in routes:
    print(f"Vehicle {route.vehicle.id}:")
    for order in route.orders:
        print(f"  - {order.id}")
    distance = algorithm.calculate_total_distance(route)
    print(f"  Total: {distance:.2f} km")
```

### Example 2: Multiple Vehicles

```python
from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# Create multiple vehicles
vehicles = [
    Vehicle("V1", 40.7128, -74.0060),  # Lower Manhattan
    Vehicle("V2", 40.7580, -73.9855),  # Midtown
]

# Create orders
orders = [
    Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
    Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
    Order("O3", 40.7831, -73.9712, 40.7489, -73.9680),
    Order("O4", 40.7061, -73.9969, 40.7306, -73.9866),
]

# Solve and get summary
algorithm = GreedyNearestNeighbor()
routes, unassigned = algorithm.solve(vehicles, orders)
summary = algorithm.get_solution_summary(routes, unassigned)

print(f"Total Distance: {summary['total_distance']} km")
print(f"Routes Used: {summary['routes_used']}")
print(f"Assigned: {summary['assigned_orders']}/{summary['total_orders']}")
```

### Example 3: Different Distance Units

```python
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# Using miles
algorithm_miles = GreedyNearestNeighbor(distance_unit='miles')
routes_miles, _ = algorithm_miles.solve(vehicles, orders)
summary_miles = algorithm_miles.get_solution_summary(routes_miles, [])

print(f"Distance in miles: {summary_miles['total_distance']} miles")

# Using meters
algorithm_meters = GreedyNearestNeighbor(distance_unit='meters')
routes_meters, _ = algorithm_meters.solve(vehicles, orders)
summary_meters = algorithm_meters.get_solution_summary(routes_meters, [])

print(f"Distance in meters: {summary_meters['total_distance']} m")
```

## Testing

Comprehensive unit tests are available in `test_greedy_algorithm.py`. Run tests with:

```bash
python3 -m pytest test_greedy_algorithm.py -v
```

Test coverage includes:
- Initialization with different units
- Single vehicle, single order
- Single vehicle, multiple orders
- Multiple vehicles, multiple orders
- Empty input validation
- Distance calculations
- Solution summary generation
- Greedy selection verification
- Round-robin assignment
- Different distance units

## Performance Considerations

### When to Use

- **Baseline Comparison**: When you need a simple baseline to compare advanced algorithms
- **Quick Solutions**: When speed is more important than optimality
- **Small Problems**: For problems with few vehicles and orders
- **Prototyping**: During initial development before implementing complex heuristics

### When Not to Use

- **Optimal Solutions Required**: When you need the best possible routes
- **Complex Constraints**: When dealing with time windows, capacity limits, etc.
- **Large-Scale Problems**: For problems with hundreds of vehicles and orders
- **Production Systems**: Where route quality significantly impacts costs

## Future Enhancements

Potential improvements for this baseline algorithm:

1. **2-opt Improvement**: Add local search to improve initial solution
2. **Look-ahead**: Consider next k orders instead of just nearest
3. **Weighted Distance**: Include factors like traffic, time windows
4. **Capacity Constraints**: Respect vehicle capacity limits
5. **Time Windows**: Consider pickup and delivery time constraints
6. **Multi-start**: Run multiple times with different vehicle orders
7. **Insertion Heuristics**: Try inserting orders at different positions

## References

- **Nearest Neighbor Heuristic**: Classic greedy algorithm for TSP and VRP
- **Vehicle Routing Problem**: Combinatorial optimization problem
- **Haversine Distance**: Great-circle distance calculation used for routing

## See Also

- [Distance Calculation Documentation](distance_calculation.md)
- [Vehicle Model](../src/models/vehicle.py)
- [Order Model](../src/models/order.py)
- [Route Model](../src/models/route.py)
