# Simulated Annealing - Visual Understanding Guide

## 🎯 Core Concept

Think of SA as **cooling molten metal**:
- **Hot metal** → atoms move freely → **exploration**
- **Cool metal** → atoms settle → **exploitation**
- **Result** → strong, optimized crystal structure → **good solution**

```
Temperature:  HIGH ═══════════════════════════════════▶ LOW
Behavior:     Exploration (accept worse)             Exploitation (best only)
Acceptance:   [████████████████████] 100%            [████▓▓▓▓▓▓▓▓▓▓] 40%
Phase:        "Let's try anything!"                   "Only improvements!"
```

## 📊 How SA Works (Step by Step)

### Step 1: Start with Initial Solution

```
Initial Random Solution:
Vehicle 0: [Order A, Order B, Order C]
Vehicle 1: [Order D, Order E]
Cost: 100 km
Temperature: 1000°C 🔥
```

### Step 2: Generate Neighbor

Pick a random move:
```
INTRA-ROUTE SWAP: Swap B and C in Vehicle 0

Neighbor Solution:
Vehicle 0: [Order A, Order C, Order B]  ← Swapped!
Vehicle 1: [Order D, Order E]
Cost: 105 km (worse!)
```

### Step 3: Decide to Accept

```
ΔE = 105 - 100 = +5 (worse)
Temperature = 1000°C

Acceptance Probability:
P = exp(-5/1000) = exp(-0.005) ≈ 0.995 = 99.5%

Random number: 0.234
0.234 < 0.995 → ACCEPT! ✓
```

**Why?** High temperature allows exploration!

### Step 4: Cool Down

```
Temperature = 1000 × 0.995 = 995°C
(Still hot, still exploring)
```

### Step 5: Repeat...

After many iterations:
```
Iteration 500:
Temperature: 82°C (medium)
Current Cost: 87 km (improved!)
Acceptance: ~70% (more selective)

Iteration 1000:
Temperature: 6.7°C (cool)
Current Cost: 78 km (much better!)
Acceptance: ~35% (very selective)

Iteration 1379:
Temperature: 1.0°C (cold)
Best Cost: 75 km (optimized!)
Acceptance: ~25% (almost frozen)
```

## 🎲 The Three Neighborhood Moves

### 1. Intra-Route Swap (40% chance)

**Before:**
```
Vehicle 0: [A → B → C → D]
                 ↕
                swap
```

**After:**
```
Vehicle 0: [A → C → B → D]
```

**Use:** Optimize order within a route

---

### 2. Inter-Route Move (40% chance)

**Before:**
```
Vehicle 0: [A → B → C]
Vehicle 1: [D → E]
              ↓
            move B
```

**After:**
```
Vehicle 0: [A → C]
Vehicle 1: [B → D → E]
```

**Use:** Rebalance workload between vehicles

---

### 3. Inter-Route Swap (20% chance)

**Before:**
```
Vehicle 0: [A → B → C]
Vehicle 1: [D → E → F]
              ↕     ↕
            swap B and E
```

**After:**
```
Vehicle 0: [A → E → C]
Vehicle 1: [D → B → F]
```

**Use:** Try different distributions

## 📈 Temperature Schedule

### Exponential Cooling

```
T(iteration) = T_initial × α^iteration

Where α = cooling_rate (e.g., 0.995)
```

**Visual:**
```
Temp
1000 │█
     │█
 750 │ █
     │  █
 500 │   ██
     │     ███
 250 │        ████
     │            ████████
   0 │___________________████████████████▁▁▁▁
     0        500      1000     1500    2000
                    Iteration
```

### Acceptance Probability Over Time

```
P(accept worse) = exp(-ΔE / T)

When ΔE = +10:

Temp 1000: P ≈ 99% │████████████████████│ Almost certain
Temp  500: P ≈ 98% │███████████████████ │ Very likely
Temp  100: P ≈ 90% │█████████████████   │ Likely
Temp   50: P ≈ 82% │████████████████    │ Probable
Temp   10: P ≈ 37% │███████             │ Maybe
Temp    5: P ≈ 13% │██                  │ Unlikely
Temp    1: P ≈ 0%  │                    │ Rare
```

## 🎬 Complete Example Run

### Initial State
```
Orders: A, B, C, D, E, F
Vehicles: V1, V2

Random Initial:
V1: [A, C, E]
V2: [B, D, F]
Cost: 95 km
```

### Iteration History (Sample)

```
Iter  Temp    Current  Neighbor  ΔE     Accept  Best    Action
───────────────────────────────────────────────────────────────
0     1000    95.0     98.0      +3.0   Y       95.0    Started
10    950     98.0     92.0      -6.0   Y       92.0    Better! ✓
50    778     92.0     97.0      +5.0   Y       92.0    Explore
100   605     97.0     89.0      -8.0   Y       89.0    Better! ✓
200   366     89.0     94.0      +5.0   Y       89.0    Explore
300   221     94.0     87.0      -7.0   Y       87.0    Better! ✓
500   82      87.0     91.0      +4.0   N       87.0    Reject
700   30      87.0     85.0      -2.0   Y       85.0    Better! ✓
1000  6.7     85.0     88.0      +3.0   N       85.0    Reject
1200  2.5     85.0     84.0      -1.0   Y       84.0    Better! ✓
1379  1.0     84.0     86.0      +2.0   N       84.0    Done!
```

### Final Solution
```
V1: [A, D, B]
V2: [C, E, F]
Cost: 84 km

Improvement: 95 → 84 = -11 km (11.6% better!)
```

## 📉 Cost Convergence Graph

```
Cost
(km)
100 │  •
    │   •  •
 95 │      • •
    │        •  •
 90 │          •   ••
    │             •  •  •
 85 │                •  •  ••••
    │                          •••••
 80 │                               •••••••••••••••
    │___________________________________________________
    0    200   400   600   800  1000  1200  1400
                        Iteration

Legend: • = Current Cost
Best cost shown by lowest point
```

## 🎲 Acceptance Pattern

### Early Phase (High Temp)

```
Accept Better:  ✓✓✓✓✓✓✓✓✓✓ (100%)
Accept Worse:   ✓✓✓✓✓✓✓✓✓✓ (98%)

Behavior: "Let's explore everything!"
```

### Middle Phase (Medium Temp)

```
Accept Better:  ✓✓✓✓✓✓✓✓✓✓ (100%)
Accept Worse:   ✓✓✓✓✓✗✗✓✗✗ (60%)

Behavior: "Getting pickier..."
```

### Late Phase (Low Temp)

```
Accept Better:  ✓✓✓✓✓✓✓✓✓✓ (100%)
Accept Worse:   ✓✗✗✗✗✗✗✗✗✗ (20%)

Behavior: "Only improvements!"
```

## 🆚 SA vs Greedy Comparison

### Greedy Algorithm
```
Start
  ↓
Choose nearest → Choose nearest → Choose nearest → Done
                                                     ↓
                                            Local Optimum ✗
                                            Cost: 95 km
```

### Simulated Annealing
```
Start (Random)
  ↓
Try move → Accept? → Cool → Try move → Accept? → Cool → ...
    ↓         ↓        ↓        ↓         ↓        ↓
  Better    Maybe    95°C    Better     Maybe    50°C
    ↓         ↓               ↓          ↓
  Accept    Accept          Accept     Reject
                                          ↓
                                  Global Optimum ✓
                                  Cost: 84 km
```

**Key Difference:** SA can **escape valleys** by accepting worse moves!

## 🗺️ Solution Space Landscape

```
Cost
120 │    ╱╲                 ╱╲
    │   ╱  ╲               ╱  ╲
100 │  ╱    ╲    ╱╲      ╱    ╲
    │ ╱      ╲  ╱  ╲    ╱      ╲
 80 │╱        ╲╱    ╲  ╱        ╲
    │          ○      ●●          
 60 │                  ╲        ╱
    │                   ╲      ╱
 40 │                    ╲    ╱
    │                     ╲  ╱
 20 │                      ╲╱ ← Global Optimum
    └──────────────────────────────────
         Solution Space

○ = Greedy gets stuck (local optimum)
● = SA explores and finds better (global optimum)
```

## 💡 Key Insights

### Why SA Works

1. **High Temperature → Exploration**
   - Accepts almost anything
   - Explores widely
   - Finds promising regions

2. **Medium Temperature → Balance**
   - Accepts selectively
   - Balances exploration/exploitation
   - Refines solutions

3. **Low Temperature → Exploitation**
   - Accepts only better
   - Fine-tunes solution
   - Converges to optimum

### The Magic Formula

```python
# Accept if better
if new_cost < current_cost:
    accept = True

# Sometimes accept if worse (magic!)
else:
    probability = exp(-(new_cost - current_cost) / temperature)
    accept = random() < probability
```

**This one formula enables:**
- Escaping local optima
- Exploring solution space
- Converging to good solutions

## 🎯 Quick Tuning Guide

### Problem: Not Improving

```
❌ Before:
initial_temp = 100
cooling_rate = 0.99
max_iterations = 1000

✅ After:
initial_temp = 2000    ← Higher exploration
cooling_rate = 0.998   ← Slower cooling
max_iterations = 10000 ← More time
```

### Problem: Takes Too Long

```
❌ Before:
initial_temp = 5000
cooling_rate = 0.999
max_iterations = 50000

✅ After:
initial_temp = 1000    ← Start lower
cooling_rate = 0.990   ← Cool faster
max_iterations = 5000  ← Less iterations
```

## 📚 Summary

**Simulated Annealing is like:**
- 🔥 Heating metal to let atoms explore
- ❄️ Cooling slowly to let them settle
- 💎 Getting a strong, optimized structure

**Key Points:**
1. Starts with high temperature (exploration)
2. Gradually cools down (exploitation)
3. Accepts worse solutions probabilistically
4. Escapes local optima
5. Finds better solutions than greedy

**Remember:**
- **Hot** = Try everything
- **Warm** = Try most things
- **Cool** = Try good things
- **Cold** = Try best things only

This balance of exploration and exploitation is what makes SA powerful! 🚀
