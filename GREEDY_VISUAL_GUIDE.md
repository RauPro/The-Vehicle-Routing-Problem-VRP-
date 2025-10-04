# Greedy Nearest Neighbor - Visual Guide

## Algorithm Visualization

### Step-by-Step Example

Consider this scenario:
- **2 Vehicles**: V1 at (40.71, -74.01), V2 at (40.76, -73.99)
- **4 Orders**: O1, O2, O3, O4 at various locations

```
Initial State:
┌─────────────────────────────────────┐
│                                     │
│    O3 (40.78, -73.97)              │
│                                     │
│       O2 (40.76, -73.99)           │
│       V2 ★                         │
│                                     │
│                O4 (40.73, -73.99)  │
│                                     │
│    V1 ★                            │
│    O1 (40.71, -74.01)              │
│                                     │
└─────────────────────────────────────┘
```

### Iteration 1: Vehicle 1

**Current Position**: V1 starting location (40.71, -74.01)
**Unassigned Orders**: O1, O2, O3, O4

Calculate distances to all unassigned pickup points:
```
V1 → O1 pickup: 0.0 km    ← NEAREST!
V1 → O2 pickup: 5.6 km
V1 → O3 pickup: 8.1 km
V1 → O4 pickup: 2.4 km
```

**Action**: Assign O1 to V1

```
After Iteration 1:
┌─────────────────────────────────────┐
│    O3                               │
│       O2                            │
│       V2 ★                         │
│                O4                   │
│                                     │
│    V1 ──→ O1 ──→ D1               │
│    Route: [O1]                     │
└─────────────────────────────────────┘
```

### Iteration 2: Vehicle 2

**Current Position**: V2 starting location (40.76, -73.99)
**Unassigned Orders**: O2, O3, O4

Calculate distances:
```
V2 → O2 pickup: 0.0 km    ← NEAREST!
V2 → O3 pickup: 2.5 km
V2 → O4 pickup: 3.3 km
```

**Action**: Assign O2 to V2

```
After Iteration 2:
┌─────────────────────────────────────┐
│    O3                               │
│       V2 ──→ O2 ──→ D2            │
│       Route: [O2]                  │
│                                     │
│                O4                   │
│                                     │
│    V1: [O1 ✓]                      │
└─────────────────────────────────────┘
```

### Iteration 3: Vehicle 1 (Round-Robin)

**Current Position**: O1 dropoff location (40.76, -73.99)
**Unassigned Orders**: O3, O4

Calculate distances from O1 dropoff:
```
O1.dropoff → O3 pickup: 2.5 km
O1.dropoff → O4 pickup: 3.3 km    ← NEAREST!
```

**Action**: Assign O4 to V1

```
After Iteration 3:
┌─────────────────────────────────────┐
│    O3                               │
│                                     │
│    V2: [O2 ✓]                      │
│                                     │
│    V1: [O1 ✓, O4]                 │
│         D1 ──→ O4 ──→ D4          │
└─────────────────────────────────────┘
```

### Iteration 4: Vehicle 2

**Current Position**: O2 dropoff location
**Unassigned Orders**: O3

Only one order left:
```
O2.dropoff → O3 pickup: 2.0 km    ← Only option
```

**Action**: Assign O3 to V2

```
Final State:
┌─────────────────────────────────────┐
│                                     │
│    V2: [O2 ✓, O3 ✓]               │
│         D2 ──→ O3 ──→ D3          │
│                                     │
│    V1: [O1 ✓, O4 ✓]               │
│         Complete route              │
│                                     │
└─────────────────────────────────────┘

All orders assigned! ✓
```

## Distance Calculation Visualization

### Route Distance Components

For a route with 2 orders:

```
Vehicle Start              Order 1              Order 2
    (VS)                 Pickup  Dropoff      Pickup  Dropoff
     ★                     P1      D1           P2      D2
     │                     │       │            │       │
     └─────(d1)────────→  ●───(d2)──→●         │       │
                                      └──(d3)──→●──(d4)──→●

Total Distance = d1 + d2 + d3 + d4

Where:
  d1 = distance from vehicle start to O1 pickup
  d2 = distance from O1 pickup to O1 dropoff
  d3 = distance from O1 dropoff to O2 pickup
  d4 = distance from O2 pickup to O2 dropoff
```

### Example Calculation

```python
Vehicle V1 at (40.7128, -74.0060)
Order O1: Pickup (40.7580, -73.9855), Dropoff (40.7614, -73.9776)
Order O2: Pickup (40.7831, -73.9712), Dropoff (40.7489, -73.9680)

d1 = haversine((40.7128, -74.0060), (40.7580, -73.9855)) = 5.42 km
d2 = haversine((40.7580, -73.9855), (40.7614, -73.9776)) = 0.77 km
d3 = haversine((40.7614, -73.9776), (40.7831, -73.9712)) = 2.47 km
d4 = haversine((40.7831, -73.9712), (40.7489, -73.9680)) = 3.81 km

Total = 5.42 + 0.77 + 2.47 + 3.81 = 12.47 km
```

## Round-Robin Assignment

### How Round-Robin Works

```
Vehicles: [V1, V2, V3]
Orders:   [O1, O2, O3, O4, O5, O6]

Round 1:  V1 → O1 (nearest to V1)
          V2 → O2 (nearest to V2)
          V3 → O3 (nearest to V3)

Round 2:  V1 → O4 (nearest to O1 dropoff)
          V2 → O5 (nearest to O2 dropoff)
          V3 → O6 (nearest to O3 dropoff)

All orders assigned!
```

### Visual Representation

```
Vehicle Queue: [V1] [V2] [V3] → back to [V1]
                 ↓    ↓    ↓         ↓
Orders:          O1   O2   O3       O4   ...

Assignment Pattern:
┌────────────────────────────────────────┐
│ Round │ Vehicle │ Assigned Order       │
├────────────────────────────────────────┤
│   1   │   V1    │       O1             │
│   1   │   V2    │       O2             │
│   1   │   V3    │       O3             │
│   2   │   V1    │       O4             │
│   2   │   V2    │       O5             │
│   2   │   V3    │       O6             │
└────────────────────────────────────────┘
```

## Greedy Selection Process

### Decision Tree for Each Assignment

```
                 [Current Vehicle]
                        │
                        ↓
           ┌────────────────────────┐
           │ Calculate distance to  │
           │ all unassigned orders  │
           └────────────────────────┘
                        │
                        ↓
              ╔═════════════════╗
              ║  Find Minimum   ║
              ║    Distance     ║
              ╚═════════════════╝
                        │
                        ↓
           ┌────────────────────────┐
           │  Assign that order to  │
           │   current vehicle      │
           └────────────────────────┘
                        │
                        ↓
           ┌────────────────────────┐
           │ Update current position│
           │  to order's dropoff    │
           └────────────────────────┘
                        │
                        ↓
           ┌────────────────────────┐
           │  Move to next vehicle  │
           │     (round-robin)      │
           └────────────────────────┘
```

## Data Flow Diagram

```
                        INPUT
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
   [Vehicles]                          [Orders]
   - id                                - id
   - current_lat                       - pickup_lat
   - current_lon                       - pickup_lon
        │                              - dropoff_lat
        │                              - dropoff_lon
        │                                   │
        └─────────────────┬─────────────────┘
                          │
                          ↓
            ╔═════════════════════════╗
            ║  GreedyNearestNeighbor  ║
            ║        .solve()         ║
            ╚═════════════════════════╝
                          │
                          ↓
              ┌───────────────────┐
              │  Assignment Loop  │
              │  - Find nearest   │
              │  - Assign order   │
              │  - Update position│
              └───────────────────┘
                          │
                          ↓
                       OUTPUT
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
    [Routes]                          [Unassigned]
    - vehicle                         - List of
    - orders[]                          unassigned
    - distances                         orders
```

## Solution Summary Structure

```
┌─────────────────────────────────────────────┐
│         SOLUTION SUMMARY                    │
├─────────────────────────────────────────────┤
│                                             │
│  Global Metrics:                            │
│  ├─ Total Vehicles: 2                       │
│  ├─ Total Orders: 5                         │
│  ├─ Assigned: 5                             │
│  ├─ Unassigned: 0                           │
│  ├─ Routes Used: 2                          │
│  ├─ Total Distance: 28.21 km                │
│  └─ Avg Distance: 14.11 km                  │
│                                             │
│  Per-Route Details:                         │
│  ┌──────────────────────────────────────┐  │
│  │ Vehicle: VEH001                      │  │
│  │ Orders: 3                            │  │
│  │ Distance: 21.16 km                   │  │
│  │ Sequence: ORD001→ORD005→ORD004      │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Vehicle: VEH002                      │  │
│  │ Orders: 2                            │  │
│  │ Distance: 7.05 km                    │  │
│  │ Sequence: ORD002→ORD003              │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

## State Transitions

```
State 0: INITIALIZATION
├─ Create empty routes for each vehicle
├─ Mark all orders as unassigned
└─ Set vehicle_index = 0

     │
     ↓

State 1: ASSIGNMENT LOOP
├─ Get current vehicle (vehicles[vehicle_index])
├─ Find nearest unassigned order
│  ├─ Calculate distances to all unassigned
│  └─ Select minimum distance order
├─ Assign order to vehicle
├─ Remove from unassigned set
└─ vehicle_index = (vehicle_index + 1) % num_vehicles

     │
     ↓

State 2: LOOP CHECK
├─ Are there unassigned orders? YES → Back to State 1
└─ NO → Continue to State 3

     │
     ↓

State 3: COMPLETION
├─ Collect unassigned orders (if any)
└─ Return (routes, unassigned)
```

## Comparison: Good vs. Suboptimal Solutions

### Scenario: 3 Orders, 1 Vehicle

#### Greedy Solution (May be suboptimal)
```
       V ────→ O1 ────→ O2 ────→ O3
       0km     5km      3km      4km
       
Total: 12 km
```

#### Optimal Solution (Not guaranteed by greedy)
```
       V ────→ O2 ────→ O1 ────→ O3
       0km     3km      5km      2km
       
Total: 10 km (Better!)
```

**Why?** Greedy chose O1 first (5km) because it was nearest, but didn't consider that O2→O1→O3 would be shorter overall.

## Performance Characteristics

### Time Complexity Growth

```
Orders (o)    Vehicles (v=1)    Operations    Time
─────────────────────────────────────────────────
    5              1              25          Fast ✓
   10              1             100          Fast ✓
   50              1            2,500         Fast ✓
  100              1           10,000         OK  ✓
  500              1          250,000         Slow ⚠
 1000              1        1,000,000         Slow ⚠

With v vehicles: multiply by v
```

### Space Complexity

```
Memory Usage:
├─ Vehicles:  O(v)
├─ Orders:    O(o)
├─ Routes:    O(v)
└─ Tracking:  O(o)

Total: O(v + o)  [Linear - Good!]
```

## Visual Debugging

### Trace Output Format

```
ITERATION 1
├─ Vehicle: VEH001
├─ Current Position: (40.7128, -74.0060)
├─ Unassigned: [ORD001, ORD002, ORD003, ORD004, ORD005]
├─ Distances:
│  ├─ ORD001: 0.00 km  ← NEAREST
│  ├─ ORD002: 5.60 km
│  ├─ ORD003: 8.10 km
│  ├─ ORD004: 2.40 km
│  └─ ORD005: 5.20 km
├─ ASSIGNED: ORD001
└─ Updated Position: (40.7589, -73.9851)
```

## Common Patterns Visualized

### Pattern 1: Hub-and-Spoke
```
       O2
        │
   O1───V───O3
        │
       O4

Greedy typically assigns: O1→O2→O3→O4
(Around the hub in order of discovery)
```

### Pattern 2: Linear Distribution
```
O1────O2────O3────O4────O5

Greedy assigns: O1→O2→O3→O4→O5
(Sequential - often optimal for linear!)
```

### Pattern 3: Clustered Orders
```
Cluster A        Cluster B
  O1  O2          O4  O5
  O3              O6

May jump between clusters if not careful
Greedy: V→O1→O2→O4→O5→O3→O6 (suboptimal)
Better: V→O1→O2→O3→O4→O5→O6 (cluster by cluster)
```

## See Also

- [Full Documentation](docs/greedy_algorithm.md)
- [Quick Reference](GREEDY_QUICK_REFERENCE.md)
- [Implementation Summary](GREEDY_ALGORITHM_SUMMARY.md)
