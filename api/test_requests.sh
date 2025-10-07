#!/bin/bash

# VRP API Testing Script
# This script tests all endpoints of the VRP API

echo "=========================================="
echo "VRP API Testing Script"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local test_name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_status="$5"
    
    echo "----------------------------------------"
    echo "Test: $test_name"
    echo "----------------------------------------"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n 1)
    # Extract body (everything except last line)
    body=$(echo "$response" | sed '$d')
    
    echo "Status Code: $status_code"
    
    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ Status Code Check PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ Status Code Check FAILED (Expected: $expected_status, Got: $status_code)${NC}"
        FAILED=$((FAILED + 1))
    fi
    
    # Pretty print JSON if valid
    if echo "$body" | python3 -m json.tool &>/dev/null; then
        echo "Response Body:"
        echo "$body" | python3 -m json.tool
        echo -e "${GREEN}✓ Valid JSON Response${NC}"
    else
        echo "Response Body (Raw):"
        echo "$body"
        if [ ! -z "$body" ]; then
            echo -e "${RED}✗ Invalid JSON Response${NC}"
        fi
    fi
    
    echo ""
}

echo "=========================================="
echo "1. Testing Health Endpoints"
echo "=========================================="
echo ""

# Test 1: Root endpoint
test_endpoint "Root Endpoint" "GET" "/" "" "200"

# Test 2: Health check
test_endpoint "Health Check" "GET" "/health" "" "200"

# Test 3: List algorithms
test_endpoint "List Algorithms" "GET" "/algorithms" "" "200"

echo "=========================================="
echo "2. Testing Greedy Algorithm"
echo "=========================================="
echo ""

# Test 4: Single vehicle, 2 orders (Greedy)
test_endpoint "Greedy: Single Vehicle, 2 Orders" "POST" "/solve" '{
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
  "algorithm": "greedy",
  "distance_unit": "km"
}' "200"

# Test 5: Multi-vehicle, 3 orders (Greedy)
test_endpoint "Greedy: Multi-Vehicle, 3 Orders" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
    {"id": "VEH002", "current_lat": 40.7580, "current_lon": -73.9855}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
    {"id": "ORD002", "pickup_lat": 40.7831, "pickup_lon": -73.9712, "dropoff_lat": 40.7489, "dropoff_lon": -73.9680},
    {"id": "ORD003", "pickup_lat": 40.7061, "pickup_lon": -73.9969, "dropoff_lat": 40.7306, "dropoff_lon": -73.9866}
  ],
  "algorithm": "greedy",
  "distance_unit": "miles"
}' "200"

echo "=========================================="
echo "3. Testing Simulated Annealing Algorithm"
echo "=========================================="
echo ""

# Test 6: Single vehicle, 2 orders (SA default params)
test_endpoint "SA (Default): Single Vehicle, 2 Orders" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
    {"id": "ORD002", "pickup_lat": 40.7831, "pickup_lon": -73.9712, "dropoff_lat": 40.7489, "dropoff_lon": -73.9680}
  ],
  "algorithm": "simulated_annealing",
  "distance_unit": "km"
}' "200"

# Test 7: Multi-vehicle with custom SA params
test_endpoint "SA (Custom Params): Multi-Vehicle, 4 Orders" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
    {"id": "VEH002", "current_lat": 40.7580, "current_lon": -73.9855}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
    {"id": "ORD002", "pickup_lat": 40.7831, "pickup_lon": -73.9712, "dropoff_lat": 40.7489, "dropoff_lon": -73.9680},
    {"id": "ORD003", "pickup_lat": 40.7061, "pickup_lon": -73.9969, "dropoff_lat": 40.7306, "dropoff_lon": -73.9866},
    {"id": "ORD004", "pickup_lat": 40.7549, "pickup_lon": -73.9840, "dropoff_lat": 40.7829, "dropoff_lon": -73.9654}
  ],
  "algorithm": "simulated_annealing",
  "distance_unit": "km",
  "sa_params": {
    "initial_temp": 1000.0,
    "cooling_rate": 0.995,
    "max_iterations": 5000
  }
}' "200"

echo "=========================================="
echo "4. Testing Error Handling"
echo "=========================================="
echo ""

# Test 8: Empty vehicles array
test_endpoint "Error: Empty Vehicles Array" "POST" "/solve" '{
  "vehicles": [],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
  ],
  "algorithm": "greedy"
}' "422"

# Test 9: Invalid coordinates
test_endpoint "Error: Invalid Latitude" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 100.0, "current_lon": -74.0060}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
  ],
  "algorithm": "greedy"
}' "422"

# Test 10: Invalid algorithm
test_endpoint "Error: Invalid Algorithm" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
  ],
  "algorithm": "invalid_algo"
}' "422"

# Test 11: Duplicate vehicle IDs
test_endpoint "Error: Duplicate Vehicle IDs" "POST" "/solve" '{
  "vehicles": [
    {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
    {"id": "VEH001", "current_lat": 40.7580, "current_lon": -73.9855}
  ],
  "orders": [
    {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
  ],
  "algorithm": "greedy"
}' "400"

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
