# Greedy Nearest Neighbor - Quick Reference

## Quick Start

```python
from src.models import Order, Vehicle
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

# 1. Create algorithm instance
algorithm = GreedyNearestNeighbor(distance_unit='km')

# 2. Prepare data
vehicles = [Vehicle("V1", 40.7128, -74.0060)]
orders = [Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)]

# 3. Solve
routes, unassigned = algorithm.solve(vehicles, orders)

# 4. Get results
summary = algorithm.get_solution_summary(routes, unassigned)
print(f"Total distance: {summary['total_distance']} km")
```

## Key Methods at a Glance

| Method | Purpose | Returns |
|--------|---------|---------|
| `solve(vehicles, orders)` | Assign orders to vehicles | `(routes, unassigned)` |
| `calculate_total_distance(route)` | Calculate route distance | `float` |
| `get_solution_summary(routes, unassigned)` | Get solution stats | `dict` |

## Constructor Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `distance_unit` | str | 'km' | 'km', 'miles', 'meters', 'feet' |

## Algorithm Flow

```
1. Initialize routes for each vehicle
2. Mark all orders as unassigned
3. While unassigned orders exist:
   a. Get current vehicle (round-robin)
   b. Find nearest unassigned order
   c. Assign order to vehicle
   d. Move to next vehicle
4. Return routes and unassigned orders
```

## Common Patterns

### Pattern 1: Single Vehicle Route

```python
vehicles = [Vehicle("V1", lat, lon)]
algorithm = GreedyNearestNeighbor()
routes, _ = algorithm.solve(vehicles, orders)
print(f"Orders: {routes[0].get_total_orders()}")
```

### Pattern 2: Fleet Optimization

```python
fleet = [Vehicle(f"V{i}", lat, lon) for i in range(1, 6)]
algorithm = GreedyNearestNeighbor()
routes, unassigned = algorithm.solve(fleet, orders)

for route in routes:
    if not route.is_empty():
        dist = algorithm.calculate_total_distance(route)
        print(f"{route.vehicle.id}: {dist:.2f} km")
```

### Pattern 3: Compare Distance Units

```python
for unit in ['km', 'miles', 'meters']:
    alg = GreedyNearestNeighbor(distance_unit=unit)
    routes, _ = alg.solve(vehicles, orders)
    summary = alg.get_solution_summary(routes, [])
    print(f"{unit}: {summary['total_distance']}")
```

## Solution Summary Structure

```python
{
    'total_vehicles': int,           # Total vehicles
    'total_orders': int,             # Total orders
    'assigned_orders': int,          # Orders assigned
    'unassigned_orders': int,        # Orders not assigned
    'routes_used': int,              # Routes with orders
    'total_distance': float,         # Sum of all distances
    'average_distance_per_route': float,  # Avg per route
    'distance_unit': str,            # Unit used
    'route_details': [               # Per-route details
        {
            'vehicle_id': str,
            'orders_count': int,
            'total_distance': float,
            'order_sequence': [str]
        }
    ]
}
```

## Error Handling

```python
try:
    routes, unassigned = algorithm.solve(vehicles, orders)
except ValueError as e:
    # Empty vehicles or orders list
    print(f"Input error: {e}")
```

## Performance Tips

1. **Pre-filter orders** by geographic region if possible
2. **Sort vehicles** by starting location for consistency
3. **Use appropriate units** to avoid conversion overhead
4. **Batch similar orders** before solving
5. **Consider vehicle capacity** in order preparation

## Common Use Cases

### Use Case 1: Morning Dispatch

```python
# Get morning orders
morning_orders = get_orders_by_time_window(6, 12)

# Get available vehicles
available_vehicles = get_idle_vehicles()

# Assign
algorithm = GreedyNearestNeighbor()
routes, unassigned = algorithm.solve(available_vehicles, morning_orders)

# Handle unassigned
if unassigned:
    notify_dispatch(unassigned)
```

### Use Case 2: Real-time Assignment

```python
def assign_new_order(new_order, current_routes):
    # Create temp vehicle at each route's end position
    temp_vehicles = []
    for route in current_routes:
        if route.orders:
            last_order = route.orders[-1]
            lat, lon = last_order.get_dropoff_coordinates()
        else:
            lat, lon = route.vehicle.get_current_coordinates()
        
        temp_vehicles.append(Vehicle(route.vehicle.id, lat, lon))
    
    # Solve for just this order
    algorithm = GreedyNearestNeighbor()
    routes, _ = algorithm.solve(temp_vehicles, [new_order])
    
    # Find which vehicle was assigned
    for route in routes:
        if not route.is_empty():
            return route.vehicle.id
```

### Use Case 3: Route Comparison

```python
def compare_algorithms(vehicles, orders):
    # Greedy baseline
    greedy = GreedyNearestNeighbor()
    greedy_routes, _ = greedy.solve(vehicles, orders)
    greedy_summary = greedy.get_solution_summary(greedy_routes, [])
    
    # TODO: Add other algorithms
    # advanced_routes, _ = advanced_algorithm.solve(vehicles, orders)
    
    return {
        'greedy': greedy_summary['total_distance'],
        # 'advanced': advanced_summary['total_distance']
    }
```

## Testing Quick Reference

```bash
# Run all tests
python3 -m pytest test_greedy_algorithm.py -v

# Run specific test
python3 -m pytest test_greedy_algorithm.py::TestGreedyNearestNeighbor::test_solve_single_vehicle_single_order -v

# Run with coverage
python3 -m pytest test_greedy_algorithm.py --cov=src.algorithms.greedy_nearest_neighbor
```

## Debugging Tips

### Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Your code here
```

### Visualize Routes

```python
def print_route_details(route, algorithm):
    print(f"\n{route.vehicle.id}:")
    current_pos = route.vehicle.get_current_coordinates()
    
    for i, order in enumerate(route.orders, 1):
        pickup = order.get_pickup_coordinates()
        dropoff = order.get_dropoff_coordinates()
        
        to_pickup = haversine_distance(current_pos, pickup)
        to_dropoff = haversine_distance(pickup, dropoff)
        
        print(f"  {i}. {order.id}")
        print(f"     To pickup: {to_pickup:.2f} km")
        print(f"     Delivery: {to_dropoff:.2f} km")
        
        current_pos = dropoff
```

### Validate Solution

```python
def validate_solution(routes, original_orders):
    # Check all orders assigned exactly once
    assigned = []
    for route in routes:
        assigned.extend(order.id for order in route.orders)
    
    original_ids = {order.id for order in original_orders}
    assigned_ids = set(assigned)
    
    assert assigned_ids == original_ids, "Order mismatch!"
    assert len(assigned) == len(assigned_ids), "Duplicate assignment!"
    
    print("✓ Solution valid")
```

## Gotchas and Common Mistakes

1. **Empty Input**: Always check for empty vehicles/orders lists
2. **Coordinate Order**: Remember it's (latitude, longitude), not (lon, lat)
3. **Unit Consistency**: Use same unit throughout calculation
4. **Round-robin**: Algorithm distributes orders across all vehicles
5. **Immutability**: Original vehicle positions aren't changed

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI, HTTPException
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor

app = FastAPI()

@app.post("/solve")
async def solve_vrp(data: dict):
    try:
        # Parse input
        vehicles = [Vehicle(**v) for v in data['vehicles']]
        orders = [Order(**o) for o in data['orders']]
        
        # Solve
        algorithm = GreedyNearestNeighbor()
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # Return summary
        summary = algorithm.get_solution_summary(routes, unassigned)
        return summary
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## See Also

- [Full Documentation](docs/greedy_algorithm.md)
- [Visual Guide](GREEDY_VISUAL_GUIDE.md)
- [Implementation Summary](GREEDY_ALGORITHM_SUMMARY.md)
