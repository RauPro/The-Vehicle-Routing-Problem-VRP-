# VRP API - Quick Testing Guide

## 🚀 Quick Start

### 1. Start the Server
```bash
cd '/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)'
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 2. Verify Server is Running
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
    "status": "healthy",
    "message": "All systems operational",
    "version": "1.0.0"
}
```

---

## 🧪 Run All Tests

```bash
bash api/test_requests.sh
```

Expected: **11/11 tests PASSED** ✅

---

## 📋 Quick Test Examples

### Test 1: Simple Greedy Solution
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060}
    ],
    "orders": [
      {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, 
       "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
    ],
    "algorithm": "greedy"
  }' | python3 -m json.tool
```

✅ **Expected**: HTTP 200, valid routes with distance calculation

### Test 2: Advanced Simulated Annealing
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
      {"id": "VEH002", "current_lat": 40.7580, "current_lon": -73.9855}
    ],
    "orders": [
      {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, 
       "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
      {"id": "ORD002", "pickup_lat": 40.7831, "pickup_lon": -73.9712, 
       "dropoff_lat": 40.7489, "dropoff_lon": -73.9680},
      {"id": "ORD003", "pickup_lat": 40.7061, "pickup_lon": -73.9969, 
       "dropoff_lat": 40.7306, "dropoff_lon": -73.9866}
    ],
    "algorithm": "simulated_annealing",
    "distance_unit": "km",
    "sa_params": {
      "initial_temp": 1000.0,
      "cooling_rate": 0.995,
      "max_iterations": 5000
    }
  }' | python3 -m json.tool
```

✅ **Expected**: HTTP 200, optimized routes with improvement statistics

### Test 3: Error Handling - Duplicate IDs
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
      {"id": "VEH001", "current_lat": 40.7580, "current_lon": -73.9855}
    ],
    "orders": [
      {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, 
       "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
    ],
    "algorithm": "greedy"
  }' | python3 -m json.tool
```

✅ **Expected**: HTTP 400, error message "Vehicle IDs must be unique"

### Test 4: Invalid Coordinates
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {"id": "VEH001", "current_lat": 100.0, "current_lon": -74.0060}
    ],
    "orders": [
      {"id": "ORD001", "pickup_lat": 40.7580, "pickup_lon": -73.9855, 
       "dropoff_lat": 40.7614, "dropoff_lon": -73.9776}
    ],
    "algorithm": "greedy"
  }' | python3 -m json.tool
```

✅ **Expected**: HTTP 422, validation error for latitude > 90

---

## 🔍 Verify Response Quality

### Check 1: HTTP Status Code
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health
```
✅ Should return: `200`

### Check 2: Valid JSON
```bash
curl -s http://localhost:8000/health | python3 -m json.tool > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```
✅ Should print: `Valid JSON`

### Check 3: Routes Contain Required Fields
Check that response includes:
- `status`: "success"
- `algorithm_used`: Algorithm name
- `total_distance`: Number
- `distance_unit`: "km" or "miles"
- `routes`: Array of route objects
- `statistics`: Object with metrics
- `unassigned_orders`: Array (may be empty)

---

## 📊 Expected Performance

| Test Case | Algorithm | Response Time | Distance Improvement |
|-----------|-----------|---------------|---------------------|
| 1 vehicle, 2 orders | Greedy | < 10ms | Baseline |
| 1 vehicle, 2 orders | SA | ~500ms | 0-10% |
| 2 vehicles, 4 orders | Greedy | < 20ms | Baseline |
| 2 vehicles, 4 orders | SA | ~800ms | 18-61% better |

---

## ✅ Success Criteria

Your API is working correctly if:

1. ✅ Health check returns 200 OK
2. ✅ All endpoints return valid JSON
3. ✅ Greedy algorithm returns routes with distances
4. ✅ SA algorithm returns routes with improvement stats
5. ✅ Error cases return proper HTTP status codes (400, 422)
6. ✅ Duplicate IDs return 400 (not 500)
7. ✅ Invalid coordinates return 422
8. ✅ Routes contain all required order IDs
9. ✅ Statistics are correctly calculated
10. ✅ No unhandled exceptions (500 errors for valid inputs)

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000
# Kill any process on port 8000
kill -9 $(lsof -t -i:8000)
```

### "Connection refused" errors
```bash
# Verify server is running
ps aux | grep uvicorn
# Check server logs for errors
```

### Tests failing
```bash
# Restart server
pkill -f uvicorn
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 &
sleep 3
# Run tests again
bash api/test_requests.sh
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **Full Test Results**: `API_TEST_RESULTS.md`
- **API Reference**: `api/API_DOCUMENTATION.md`
- **Postman Collection**: `api/VRP_API.postman_collection.json`

---

## 🎯 Current Status

**Date**: October 7, 2025  
**Tests Passed**: 11/11 (100%)  
**Status**: ✅ **PRODUCTION READY**

All endpoints tested and verified:
- ✅ Health checks working
- ✅ Greedy algorithm functional
- ✅ Simulated Annealing optimizing correctly
- ✅ Error handling proper
- ✅ JSON responses valid
- ✅ Bug fixes applied and tested

**Ready for integration!** 🚀
