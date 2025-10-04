# Simulated Annealing Algorithm for VRP

## Overview

Simulated Annealing (SA) is a probabilistic metaheuristic optimization algorithm inspired by the annealing process in metallurgy. In this context, it's used to find near-optimal solutions for the Vehicle Routing Problem by intelligently exploring the solution space.

## Algorithm Concept

### Metallurgical Analogy

In metallurgy, annealing is a heat treatment process where:
1. Metal is heated to a high temperature
2. Temperature is slowly decreased (cooled)
3. This allows atoms to reach a low-energy crystalline state

### Computational Approach

Similarly, in Simulated Annealing:
1. Start with a high "temperature" that allows exploration
2. Gradually decrease the temperature (cooling)
3. Accept both better and worse solutions probabilistically
4. At high temperatures: accept more worse solutions (exploration)
5. At low temperatures: accept mostly better solutions (exploitation)

This approach helps escape local optima and find better global solutions.

## Solution Representation

A solution is represented as a **list of lists**, where:
- Each outer list index corresponds to a vehicle
- Each inner list contains `Order` objects assigned to that vehicle
- Order sequence in the list represents the delivery order

**Example:**
```python
solution = [
    [Order1, Order3, Order5],  # Vehicle 0's route
    [Order2, Order4],           # Vehicle 1's route
    []                          # Vehicle 2's route (empty)
]
```

This representation:
- ✓ Is simple and intuitive
- ✓ Allows easy order reassignment
- ✓ Supports variable route lengths
- ✓ Handles empty routes naturally

## Core Components

### 1. Cost Function

```python
def calculate_total_cost(solution, vehicles) -> float
```

Calculates the total distance for a solution by summing:
1. **Vehicle to first pickup**: Distance from vehicle's starting position to first order's pickup
2. **Pickup to dropoff**: Distance for each order's delivery
3. **Between orders**: Distance from previous dropoff to next pickup

**Example Calculation:**
```
Vehicle at (40.0, -74.0)
  → Pickup Order1 at (40.1, -74.1): 15.7 km
  → Deliver to (40.2, -74.2): 15.7 km
  → Pickup Order2 at (40.3, -74.3): 15.7 km
  → Deliver to (40.4, -74.4): 15.7 km
Total: 62.8 km
```

### 2. Neighbor Function

```python
def get_neighbor(solution) -> List[List[Order]]
```

Generates a new solution by making a small random change. Implements three operators:

#### a) Intra-route Swap (40% probability)
Swap two orders within the same vehicle's route.

```
Before: Vehicle 0: [A, B, C, D]
After:  Vehicle 0: [A, D, C, B]  # Swapped B and D
```

**Use case:** Optimize order sequence within a route

#### b) Inter-route Move (40% probability)
Move an order from one vehicle to another.

```
Before: 
  Vehicle 0: [A, B, C]
  Vehicle 1: [D, E]

After:
  Vehicle 0: [A, C]      # B removed
  Vehicle 1: [D, B, E]   # B inserted
```

**Use case:** Balance workload between vehicles

#### c) Inter-route Swap (20% probability)
Exchange orders between two different vehicles.

```
Before:
  Vehicle 0: [A, B, C]
  Vehicle 1: [D, E, F]

After:
  Vehicle 0: [A, E, C]   # B → E
  Vehicle 1: [D, B, F]   # E → B
```

**Use case:** Explore different order distributions

### 3. Acceptance Criterion

The algorithm decides whether to accept a neighbor solution using:

```python
if neighbor_cost < current_cost:
    accept = True  # Always accept better solutions
else:
    # Accept worse solutions with probability
    probability = exp(-(neighbor_cost - current_cost) / temperature)
    accept = random() < probability
```

**Key insight:** The acceptance probability decreases as:
- Temperature decreases (over time)
- Cost difference increases (worse solutions less likely)

**Example:**
```
Temperature = 1000, ΔE = 10 → P ≈ 99.0% (almost certain acceptance)
Temperature = 100,  ΔE = 10 → P ≈ 90.5% (high acceptance)
Temperature = 10,   ΔE = 10 → P ≈ 36.8% (moderate acceptance)
Temperature = 1,    ΔE = 10 → P ≈ 0.0%  (very low acceptance)
```

## Algorithm Parameters

### Initial Temperature (`initial_temp`)
- **Range:** 100 - 5000
- **Default:** 1000.0
- **Effect:** Higher = more exploration
- **Tuning:** Should be ~10-100× the typical cost difference

### Final Temperature (`final_temp`)
- **Range:** 0.1 - 10
- **Default:** 1.0
- **Effect:** Determines stopping point
- **Tuning:** Lower = longer runtime, potentially better solution

### Cooling Rate (`cooling_rate`)
- **Range:** 0.90 - 0.999
- **Default:** 0.995
- **Effect:** Controls temperature decrease speed
- **Formula:** `T_new = T_old × cooling_rate`

**Cooling comparison:**
```
Rate 0.99:  T=1000 → T=1 in ~460 iterations  (fast)
Rate 0.995: T=1000 → T=1 in ~1380 iterations (medium)
Rate 0.999: T=1000 → T=1 in ~6900 iterations (slow)
```

### Max Iterations (`max_iterations`)
- **Range:** 1000 - 50000
- **Default:** 10000
- **Effect:** Maximum runtime limit
- **Tuning:** More = better but slower

## Usage Example

### Basic Usage

```python
from src.models import Order, Vehicle
from src.algorithms import SimulatedAnnealing

# Create problem instance
vehicles = [
    Vehicle("V1", 40.7128, -74.0060),
    Vehicle("V2", 40.7580, -73.9855)
]

orders = [
    Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
    Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
    # ... more orders
]

# Initialize and solve
sa = SimulatedAnnealing(
    initial_temp=1000.0,
    final_temp=1.0,
    cooling_rate=0.995,
    max_iterations=10000
)

routes, cost, stats = sa.solve(vehicles, orders)

print(f"Best cost: {cost:.2f} km")
print(f"Improvement: {stats['improvement_percentage']:.1f}%")
```

### With Custom Initial Solution

```python
# Start from greedy solution
from src.algorithms import GreedyNearestNeighbor

greedy = GreedyNearestNeighbor()
greedy_routes, _ = greedy.solve(vehicles, orders)

# Convert to solution format
initial_solution = [route.orders for route in greedy_routes]

# Optimize with SA
routes, cost, stats = sa.solve(
    vehicles, 
    orders, 
    initial_solution=initial_solution
)
```

### With Verbose Logging

```python
sa = SimulatedAnnealing(
    initial_temp=1000.0,
    cooling_rate=0.995,
    verbose=True  # Enable iteration logging
)

routes, cost, stats = sa.solve(vehicles, orders)
```

Output:
```
Iter     Temp       Current      Neighbor     ΔE           Accept   Best
--------------------------------------------------------------------------------
0        1000.00    145.23       152.45       7.22         Y        145.23
1        995.00     152.45       148.67       -3.78        Y        145.23
2        990.03     148.67       155.89       7.22         Y        145.23
...
```

## Performance Characteristics

### Time Complexity
- **Per iteration:** O(n) where n = number of orders
- **Total:** O(iterations × n)
- **Typical:** 10,000 iterations × 100 orders ≈ 1 million operations

### Space Complexity
- **Solution storage:** O(n)
- **History tracking:** O(iterations) if verbose
- **Total:** O(n + iterations)

### Scalability

| Orders | Vehicles | Iterations | Time (approx) |
|--------|----------|------------|---------------|
| 10     | 2        | 1,000      | < 1 second    |
| 50     | 5        | 5,000      | ~5 seconds    |
| 100    | 10       | 10,000     | ~20 seconds   |
| 500    | 20       | 20,000     | ~3 minutes    |

## Debugging Guide

### Problem: No Improvement Over Initial Solution

**Symptoms:**
- `improvement_percentage` near 0%
- Cost doesn't decrease

**Diagnoses:**
1. Temperature too low → increase `initial_temp`
2. Cooling too fast → increase `cooling_rate` (closer to 1)
3. Not enough iterations → increase `max_iterations`

**Fix:**
```python
sa = SimulatedAnnealing(
    initial_temp=2000.0,    # Was 1000
    cooling_rate=0.998,     # Was 0.995
    max_iterations=20000    # Was 10000
)
```

### Problem: Too Many Worse Solutions Accepted

**Symptoms:**
- `worse_accepted` > 80% of total
- Cost fluctuates wildly

**Diagnosis:** Temperature too high or cooling too slow

**Fix:**
```python
sa = SimulatedAnnealing(
    initial_temp=500.0,     # Was 1000
    cooling_rate=0.990,     # Was 0.995
)
```

### Problem: Gets Stuck in Local Optimum

**Symptoms:**
- Cost plateaus early
- No worse solutions accepted

**Diagnosis:** Temperature drops too quickly

**Fix:**
```python
sa = SimulatedAnnealing(
    initial_temp=1500.0,    # Higher starting temp
    cooling_rate=0.997,     # Slower cooling
)
```

## Testing Your Implementation

### Test 1: Cost Function
```python
# Verify cost calculation
solution = [[order1, order2], [order3]]
cost = sa.calculate_total_cost(solution, vehicles)
assert cost > 0, "Cost must be positive"
```

### Test 2: Neighbor Generation
```python
# Generate 20 neighbors, verify all orders present
for _ in range(20):
    neighbor = sa.get_neighbor(solution)
    
    # Check all orders still there
    all_orders = [o for route in neighbor for o in route]
    assert len(all_orders) == len(orders)
```

### Test 3: SA Loop
```python
# Run full optimization
routes, cost, stats = sa.solve(vehicles, orders)

# Verify improvement
assert stats['improvement'] >= 0
assert stats['final_cost'] <= stats['initial_cost']
```

### Test 4: Beat Greedy
```python
# Compare with baseline
greedy_cost = greedy.solve(vehicles, orders)[0]
sa_cost = sa.solve(vehicles, orders)[1]

print(f"Greedy: {greedy_cost:.2f}")
print(f"SA: {sa_cost:.2f}")
assert sa_cost <= greedy_cost * 1.1  # Within 10%
```

## Advanced Tips

### 1. Adaptive Cooling
Adjust cooling rate based on acceptance:
```python
if acceptance_rate < 0.1:
    temperature *= 0.999  # Cool slower
else:
    temperature *= 0.995  # Cool faster
```

### 2. Reheating
Restart with higher temperature if stuck:
```python
if no_improvement_for_n_iterations > 1000:
    temperature = initial_temp * 0.5  # Reheat
```

### 3. Multiple Runs
Run SA multiple times with different seeds:
```python
best_cost = float('inf')
for seed in range(10):
    random.seed(seed)
    routes, cost, _ = sa.solve(vehicles, orders)
    if cost < best_cost:
        best_solution = routes
        best_cost = cost
```

## References

- Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). "Optimization by simulated annealing"
- Van Laarhoven, P. J., & Aarts, E. H. (1987). "Simulated annealing: Theory and applications"
- Osman, I. H. (1993). "Metastrategy simulated annealing and tabu search algorithms for the vehicle routing problem"

## Summary

Simulated Annealing is a powerful metaheuristic that:
- ✓ Escapes local optima through probabilistic acceptance
- ✓ Balances exploration (high temp) and exploitation (low temp)
- ✓ Typically outperforms greedy algorithms by 10-30%
- ✓ Is easy to implement and understand
- ✓ Works well for VRP and many other optimization problems

The key to success is proper parameter tuning for your specific problem instance!
