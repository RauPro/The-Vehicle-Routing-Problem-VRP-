#!/bin/bash

# VRP API - Example cURL Commands
# 
# This script contains example cURL commands to test the VRP API.
# Make sure the API server is running before executing these commands.
#
# Start the server with:
#   cd api && python main.py
# Or:
#   uvicorn api.main:app --reload

API_URL="http://localhost:8000"

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                       VRP API - cURL Examples                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# Test 1: Health Check
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 1: Health Check"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X GET "${API_URL}/health" \
  -H "Content-Type: application/json" | jq '.'

echo ""
echo ""

# ============================================================================
# Test 2: List Available Algorithms
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 2: List Available Algorithms"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X GET "${API_URL}/algorithms" \
  -H "Content-Type: application/json" | jq '.'

echo ""
echo ""

# ============================================================================
# Test 3: Solve with Greedy Algorithm
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 3: Solve with Greedy Algorithm"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X POST "${API_URL}/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {
        "id": "VEH001",
        "current_lat": 40.7128,
        "current_lon": -74.0060
      },
      {
        "id": "VEH002",
        "current_lat": 40.7580,
        "current_lon": -73.9855
      }
    ],
    "orders": [
      {
        "id": "ORD001",
        "pickup_lat": 40.7128,
        "pickup_lon": -74.0060,
        "dropoff_lat": 40.7589,
        "dropoff_lon": -73.9851
      },
      {
        "id": "ORD002",
        "pickup_lat": 40.7580,
        "pickup_lon": -73.9855,
        "dropoff_lat": 40.7614,
        "dropoff_lon": -73.9776
      },
      {
        "id": "ORD003",
        "pickup_lat": 40.7831,
        "pickup_lon": -73.9712,
        "dropoff_lat": 40.7489,
        "dropoff_lon": -73.9680
      }
    ],
    "algorithm": "greedy",
    "distance_unit": "km"
  }' | jq '.'

echo ""
echo ""

# ============================================================================
# Test 4: Solve with Simulated Annealing
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 4: Solve with Simulated Annealing"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X POST "${API_URL}/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {
        "id": "VEH001",
        "current_lat": 40.7128,
        "current_lon": -74.0060
      },
      {
        "id": "VEH002",
        "current_lat": 40.7580,
        "current_lon": -73.9855
      }
    ],
    "orders": [
      {
        "id": "ORD001",
        "pickup_lat": 40.7128,
        "pickup_lon": -74.0060,
        "dropoff_lat": 40.7589,
        "dropoff_lon": -73.9851
      },
      {
        "id": "ORD002",
        "pickup_lat": 40.7580,
        "pickup_lon": -73.9855,
        "dropoff_lat": 40.7614,
        "dropoff_lon": -73.9776
      },
      {
        "id": "ORD003",
        "pickup_lat": 40.7831,
        "pickup_lon": -73.9712,
        "dropoff_lat": 40.7489,
        "dropoff_lon": -73.9680
      },
      {
        "id": "ORD004",
        "pickup_lat": 40.7061,
        "pickup_lon": -73.9969,
        "dropoff_lat": 40.7306,
        "dropoff_lon": -73.9866
      },
      {
        "id": "ORD005",
        "pickup_lat": 40.7549,
        "pickup_lon": -73.9840,
        "dropoff_lat": 40.7829,
        "dropoff_lon": -73.9654
      }
    ],
    "algorithm": "simulated_annealing",
    "distance_unit": "km",
    "sa_params": {
      "initial_temp": 1000.0,
      "cooling_rate": 0.995,
      "max_iterations": 3000
    }
  }' | jq '.'

echo ""
echo ""

# ============================================================================
# Test 5: Solve with SA (using miles)
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 5: Solve with Simulated Annealing (Miles)"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X POST "${API_URL}/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {
        "id": "VEH001",
        "current_lat": 40.7128,
        "current_lon": -74.0060
      }
    ],
    "orders": [
      {
        "id": "ORD001",
        "pickup_lat": 40.7580,
        "pickup_lon": -73.9855,
        "dropoff_lat": 40.7614,
        "dropoff_lon": -73.9776
      },
      {
        "id": "ORD002",
        "pickup_lat": 40.7831,
        "pickup_lon": -73.9712,
        "dropoff_lat": 40.7489,
        "dropoff_lon": -73.9680
      }
    ],
    "algorithm": "simulated_annealing",
    "distance_unit": "miles"
  }' | jq '.'

echo ""
echo ""

# ============================================================================
# Test 6: Error Handling - Invalid Coordinates
# ============================================================================

echo "─────────────────────────────────────────────────────────────────────────────"
echo "TEST 6: Error Handling - Invalid Coordinates"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""

curl -X POST "${API_URL}/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {
        "id": "VEH001",
        "current_lat": 100.0,
        "current_lon": -74.0060
      }
    ],
    "orders": [
      {
        "id": "ORD001",
        "pickup_lat": 40.7580,
        "pickup_lon": -73.9855,
        "dropoff_lat": 40.7614,
        "dropoff_lon": -73.9776
      }
    ]
  }' | jq '.'

echo ""
echo ""

echo "════════════════════════════════════════════════════════════════════════════"
echo "All cURL examples completed!"
echo "════════════════════════════════════════════════════════════════════════════"
