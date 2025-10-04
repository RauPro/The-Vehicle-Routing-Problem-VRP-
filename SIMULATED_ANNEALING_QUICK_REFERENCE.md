# Simulated Annealing - Quick Reference Guide

## 🚀 Quick Start

```python
from src.algorithms import SimulatedAnnealing
from src.models import Order, Vehicle

# Create problem
vehicles = [Vehicle("V1", 40.7128, -74.0060)]
orders = [Order("O1", 40.7, -74.0, 40.8, -73.9)]

# Solve with SA
sa = SimulatedAnnealing()
routes, cost, stats = sa.solve(vehicles, orders)

print(f"Cost: {cost:.2f} km")
print(f"Improvement: {stats['improvement_percentage']:.1f}%")
```

## 📊 Common Configurations

### Default (Balanced)
```python
SimulatedAnnealing(
    initial_temp=1000.0,
    final_temp=1.0,
    cooling_rate=0.995,
    max_iterations=10000
)
```
**Time:** ~10-30 seconds for 100 orders
**Quality:** Good balance

### Fast (Quick Results)
```python
SimulatedAnnealing(
    initial_temp=500.0,
    final_temp=1.0,
    cooling_rate=0.990,
    max_iterations=2000
)
```
**Time:** ~2-5 seconds for 100 orders
**Quality:** Decent, may miss optimal

### High Quality (Best Results)
```python
SimulatedAnnealing(
    initial_temp=2000.0,
    final_temp=0.5,
    cooling_rate=0.998,
    max_iterations=20000
)
```
**Time:** ~1-3 minutes for 100 orders
**Quality:** Excellent, near-optimal

## 🔍 Solution Representation

```python
# Solution = List of routes
# Route = List of orders per vehicle
solution = [
    [order1, order3, order5],  # Vehicle 0
    [order2, order4],          # Vehicle 1
    []                         # Vehicle 2 (empty)
]
```

## 🎯 Key Methods

### Solve Problem
```python
routes, cost, stats = sa.solve(vehicles, orders)
# Returns:
# - routes: List[Route] - optimized routes
# - cost: float - total distance
# - stats: dict - optimization statistics
```

### Calculate Cost
```python
cost = sa.calculate_total_cost(solution, vehicles)
# Returns total distance for a solution
```

### Generate Neighbor
```python
neighbor = sa.get_neighbor(solution)
# Returns a modified copy of the solution
```

### Get Summary
```python
summary = sa.get_solution_summary(routes, cost)
# Returns detailed summary statistics
```

## 📈 Statistics Available

```python
stats = {
    'iterations_completed': 1379,
    'total_attempts': 1379,
    'total_accepted': 1156,
    'acceptance_rate': 0.838,
    'better_accepted': 550,
    'worse_accepted': 606,
    'initial_cost': 39.58,
    'final_cost': 32.69,
    'improvement': 6.89,
    'improvement_percentage': 17.4,
    'distance_unit': 'km',
    'initial_temperature': 1000.0,
    'final_temperature': 1.0,
    'cooling_rate': 0.995
}
```

## 🐛 Debugging Checklist

### Problem: No Improvement
- [ ] Increase `initial_temp` (try 2000-5000)
- [ ] Increase `cooling_rate` (try 0.998-0.999)
- [ ] Increase `max_iterations` (try 20000+)

### Problem: Cost Increases
- [ ] Check cost function implementation
- [ ] Verify neighbor function preserves all orders
- [ ] Ensure best solution is tracked separately

### Problem: Too Slow
- [ ] Decrease `max_iterations` (try 2000-5000)
- [ ] Increase `cooling_rate` (try 0.985-0.990)
- [ ] Decrease `initial_temp` (try 500-800)

### Problem: Gets Stuck
- [ ] Temperature dropping too fast
- [ ] Increase `initial_temp`
- [ ] Increase `cooling_rate` (slower cooling)

## 🧪 Testing Commands

```bash
# Run all tests
python test_simulated_annealing.py

# Run main demo
python main.py

# Run detailed example
python example_simulated_annealing.py

# Run specific test
python -c "from test_simulated_annealing import test_cost_function; test_cost_function()"
```

## 📏 Parameter Guidelines

### Initial Temperature
| Problem Size | Recommended Range |
|--------------|------------------|
| < 20 orders  | 500 - 1000       |
| 20-50 orders | 1000 - 2000      |
| 50-100 orders| 2000 - 3000      |
| 100+ orders  | 3000 - 5000      |

**Rule of thumb:** ~10-100× typical cost difference

### Cooling Rate
| Speed | Rate | Description |
|-------|------|-------------|
| Fast  | 0.985-0.990 | Quick convergence |
| Medium| 0.995-0.997 | Balanced |
| Slow  | 0.998-0.999 | Thorough search |

**Rule of thumb:** Higher = slower but better

### Max Iterations
| Quality | Iterations |
|---------|-----------|
| Quick   | 1000-2000 |
| Normal  | 5000-10000|
| High    | 20000+    |

**Rule of thumb:** More = better but slower

## 🎨 Visualization Tips

### Plot Cost Over Time
```python
import matplotlib.pyplot as plt

costs = [h['best_cost'] for h in sa.iteration_history]
plt.plot(costs)
plt.xlabel('Iteration')
plt.ylabel('Best Cost (km)')
plt.title('SA Convergence')
plt.show()
```

### Plot Acceptance Rate
```python
# Calculate rolling acceptance
window = 100
acceptance = [
    sum(sa.acceptance_history[i:i+window]) / window
    for i in range(0, len(sa.acceptance_history) - window)
]
plt.plot(acceptance)
plt.xlabel('Iteration')
plt.ylabel('Acceptance Rate')
plt.show()
```

## 🔄 Common Patterns

### Start from Greedy Solution
```python
from src.algorithms import GreedyNearestNeighbor

# Get greedy solution
greedy = GreedyNearestNeighbor()
greedy_routes, _ = greedy.solve(vehicles, orders)

# Convert to SA format
initial_solution = [route.orders for route in greedy_routes]

# Optimize with SA
routes, cost, stats = sa.solve(
    vehicles, 
    orders,
    initial_solution=initial_solution
)
```

### Multiple Runs
```python
import random

best_cost = float('inf')
best_routes = None

for seed in range(10):
    random.seed(seed)
    routes, cost, _ = sa.solve(vehicles, orders)
    
    if cost < best_cost:
        best_cost = cost
        best_routes = routes

print(f"Best of 10 runs: {best_cost:.2f} km")
```

### Custom Initial Solution
```python
# Manually assign orders
initial_solution = [
    [orders[0], orders[2], orders[4]],  # Vehicle 0
    [orders[1], orders[3]],             # Vehicle 1
]

routes, cost, stats = sa.solve(
    vehicles,
    orders,
    initial_solution=initial_solution
)
```

## 📋 Expected Results

### Typical Improvements Over Greedy
- **Small instances** (< 20 orders): 10-20%
- **Medium instances** (20-50 orders): 15-25%
- **Large instances** (50+ orders): 20-35%

### Typical Runtime
- **10 orders**: < 1 second
- **50 orders**: 5-10 seconds
- **100 orders**: 20-40 seconds
- **500 orders**: 2-5 minutes

### Typical Acceptance Rates
- **Start (high temp)**: 95-100%
- **Middle**: 70-90%
- **End (low temp)**: 30-60%

## 🎯 Performance Tuning

### For Speed Priority
```python
SimulatedAnnealing(
    initial_temp=500,
    cooling_rate=0.985,
    max_iterations=1000
)
```

### For Quality Priority
```python
SimulatedAnnealing(
    initial_temp=3000,
    cooling_rate=0.999,
    max_iterations=50000
)
```

### For Large Problems (500+ orders)
```python
SimulatedAnnealing(
    initial_temp=5000,
    cooling_rate=0.999,
    max_iterations=100000,
    verbose=True  # Monitor progress
)
```

## 💡 Pro Tips

1. **Always compare with greedy**: SA should beat it
2. **Run multiple times**: SA is stochastic
3. **Log verbose for debugging**: See what's happening
4. **Start with high temp**: Better exploration
5. **Cool slowly**: Better convergence
6. **Track best solution**: Don't lose it!
7. **Validate neighbors**: Ensure integrity
8. **Test incrementally**: Build up complexity

## 🔗 Related Files

- **Implementation**: `src/algorithms/simulated_annealing.py`
- **Tests**: `test_simulated_annealing.py`
- **Example**: `example_simulated_annealing.py`
- **Documentation**: `docs/simulated_annealing.md`
- **Summary**: `SIMULATED_ANNEALING_COMPLETE.md`

## 📚 Further Reading

- [Algorithm Documentation](docs/simulated_annealing.md)
- [Complete Summary](SIMULATED_ANNEALING_COMPLETE.md)
- [Greedy Baseline](docs/greedy_algorithm.md)

---

**Need help?** Check the comprehensive documentation in `docs/simulated_annealing.md`
