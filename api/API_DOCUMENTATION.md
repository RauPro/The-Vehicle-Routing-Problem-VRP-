# Vehicle Routing Problem (VRP) REST API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Schemas](#requestresponse-schemas)
5. [Examples](#examples)
6. [Error Handling](#error-handling)
7. [Testing](#testing)

---

## Overview

The VRP REST API provides optimized vehicle routing solutions using advanced algorithms. The API accepts a problem definition (vehicles and orders) and returns optimized routes that minimize total travel distance.

### Features
- **Multiple Algorithms**: Greedy Nearest Neighbor and Simulated Annealing
- **Flexible Distance Units**: Kilometers or miles
- **Configurable SA Parameters**: Temperature, cooling rate, iterations
- **Comprehensive Error Handling**: Validation and detailed error messages
- **Auto-Documentation**: Interactive API docs at `/docs`

### Base URL
```
http://localhost:8000
```

---

## Getting Started

### Prerequisites
- Python 3.12+
- Virtual environment (recommended)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the server:**
```bash
# Method 1: Using uvicorn directly
uvicorn api.main:app --reload

# Method 2: Using Python
cd api
python main.py
```

3. **Verify server is running:**
```bash
curl http://localhost:8000/health
```

### Interactive Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Endpoints

### 1. Root Endpoint
**GET** `/`

Get API information and status.

**Response:**
```json
{
  "message": "Vehicle Routing Problem (VRP) API",
  "status": "operational",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "algorithms": "/algorithms",
    "solve": "/solve (POST)"
  }
}
```

---

### 2. Health Check
**GET** `/health`

Check if the API is healthy and operational.

**Response:**
```json
{
  "status": "healthy",
  "message": "All systems operational",
  "timestamp": "2025-01-29T12:34:56"
}
```

---

### 3. List Algorithms
**GET** `/algorithms`

Get information about available algorithms and their parameters.

**Response:**
```json
{
  "algorithms": [
    {
      "name": "greedy",
      "description": "Greedy Nearest Neighbor algorithm",
      "parameters": []
    },
    {
      "name": "simulated_annealing",
      "description": "Simulated Annealing metaheuristic",
      "parameters": [
        {
          "name": "initial_temp",
          "type": "float",
          "default": 1000.0,
          "description": "Initial temperature"
        },
        {
          "name": "cooling_rate",
          "type": "float",
          "default": 0.995,
          "description": "Temperature cooling rate"
        },
        {
          "name": "max_iterations",
          "type": "int",
          "default": 5000,
          "description": "Maximum iterations"
        }
      ]
    }
  ]
}
```

---

### 4. Solve VRP
**POST** `/solve`

Solve a Vehicle Routing Problem instance and return optimized routes.

**Request Body:**
```json
{
  "vehicles": [
    {
      "id": "string",
      "current_lat": "number (-90 to 90)",
      "current_lon": "number (-180 to 180)"
    }
  ],
  "orders": [
    {
      "id": "string",
      "pickup_lat": "number (-90 to 90)",
      "pickup_lon": "number (-180 to 180)",
      "dropoff_lat": "number (-90 to 90)",
      "dropoff_lon": "number (-180 to 180)"
    }
  ],
  "algorithm": "greedy | simulated_annealing (default: greedy)",
  "distance_unit": "km | miles (default: km)",
  "sa_params": {
    "initial_temp": "number (optional, default: 1000.0)",
    "cooling_rate": "number (optional, default: 0.995)",
    "max_iterations": "integer (optional, default: 5000)"
  }
}
```

**Response:**
```json
{
  "routes": [
    {
      "vehicle_id": "string",
      "stops": [
        {
          "order_id": "string",
          "type": "pickup | dropoff",
          "lat": "number",
          "lon": "number"
        }
      ],
      "total_distance": "number"
    }
  ],
  "total_distance": "number",
  "distance_unit": "string",
  "algorithm_used": "string",
  "computation_time_seconds": "number",
  "statistics": {
    "total_vehicles": "integer",
    "total_orders": "integer",
    "vehicles_used": "integer",
    "avg_distance_per_vehicle": "number"
  }
}
```

---

## Request/Response Schemas

### Vehicle Schema
```python
{
  "id": str,              # Unique vehicle identifier
  "current_lat": float,   # Current latitude (-90 to 90)
  "current_lon": float    # Current longitude (-180 to 180)
}
```

**Validation:**
- `id` must not be empty
- `current_lat` must be between -90 and 90
- `current_lon` must be between -180 and 180

---

### Order Schema
```python
{
  "id": str,              # Unique order identifier
  "pickup_lat": float,    # Pickup latitude (-90 to 90)
  "pickup_lon": float,    # Pickup longitude (-180 to 180)
  "dropoff_lat": float,   # Dropoff latitude (-90 to 90)
  "dropoff_lon": float    # Dropoff longitude (-180 to 180)
}
```

**Validation:**
- `id` must not be empty
- All latitude values must be between -90 and 90
- All longitude values must be between -180 and 180

---

### Solve Request Schema
```python
{
  "vehicles": List[Vehicle],           # At least 1 vehicle required
  "orders": List[Order],               # At least 1 order required
  "algorithm": str = "greedy",         # "greedy" or "simulated_annealing"
  "distance_unit": str = "km",         # "km" or "miles"
  "sa_params": Optional[SAParams]      # Only for simulated_annealing
}
```

**Validation:**
- `vehicles` list must not be empty
- `orders` list must not be empty
- `algorithm` must be "greedy" or "simulated_annealing"
- `distance_unit` must be "km" or "miles"

---

### SA Parameters Schema
```python
{
  "initial_temp": float = 1000.0,      # Initial temperature (> 0)
  "cooling_rate": float = 0.995,       # Cooling rate (0 < rate < 1)
  "max_iterations": int = 5000         # Maximum iterations (> 0)
}
```

**Validation:**
- `initial_temp` must be positive
- `cooling_rate` must be between 0 and 1 (exclusive)
- `max_iterations` must be positive

---

## Examples

### Example 1: Basic Greedy Solution

**Request:**
```bash
curl -X POST http://localhost:8000/solve \
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
    "algorithm": "greedy"
  }'
```

**Response:**
```json
{
  "routes": [
    {
      "vehicle_id": "VEH001",
      "stops": [
        {
          "order_id": "ORD001",
          "type": "pickup",
          "lat": 40.758,
          "lon": -73.9855
        },
        {
          "order_id": "ORD001",
          "type": "dropoff",
          "lat": 40.7614,
          "lon": -73.9776
        },
        {
          "order_id": "ORD002",
          "type": "pickup",
          "lat": 40.7831,
          "lon": -73.9712
        },
        {
          "order_id": "ORD002",
          "type": "dropoff",
          "lat": 40.7489,
          "lon": -73.968
        }
      ],
      "total_distance": 8.432
    }
  ],
  "total_distance": 8.432,
  "distance_unit": "km",
  "algorithm_used": "greedy",
  "computation_time_seconds": 0.002,
  "statistics": {
    "total_vehicles": 1,
    "total_orders": 2,
    "vehicles_used": 1,
    "avg_distance_per_vehicle": 8.432
  }
}
```

---

### Example 2: Simulated Annealing with Custom Parameters

**Request:**
```bash
curl -X POST http://localhost:8000/solve \
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
    "algorithm": "simulated_annealing",
    "distance_unit": "miles",
    "sa_params": {
      "initial_temp": 1000.0,
      "cooling_rate": 0.995,
      "max_iterations": 3000
    }
  }'
```

**Response:**
```json
{
  "routes": [
    {
      "vehicle_id": "VEH001",
      "stops": [
        {
          "order_id": "ORD001",
          "type": "pickup",
          "lat": 40.7128,
          "lon": -74.006
        },
        {
          "order_id": "ORD001",
          "type": "dropoff",
          "lat": 40.7589,
          "lon": -73.9851
        }
      ],
      "total_distance": 3.124
    },
    {
      "vehicle_id": "VEH002",
      "stops": [
        {
          "order_id": "ORD002",
          "type": "pickup",
          "lat": 40.758,
          "lon": -73.9855
        },
        {
          "order_id": "ORD002",
          "type": "dropoff",
          "lat": 40.7614,
          "lon": -73.9776
        },
        {
          "order_id": "ORD003",
          "type": "pickup",
          "lat": 40.7831,
          "lon": -73.9712
        },
        {
          "order_id": "ORD003",
          "type": "dropoff",
          "lat": 40.7489,
          "lon": -73.968
        }
      ],
      "total_distance": 2.891
    }
  ],
  "total_distance": 6.015,
  "distance_unit": "miles",
  "algorithm_used": "simulated_annealing",
  "computation_time_seconds": 0.847,
  "statistics": {
    "total_vehicles": 2,
    "total_orders": 3,
    "vehicles_used": 2,
    "avg_distance_per_vehicle": 3.008
  }
}
```

---

### Example 3: Multi-Vehicle Problem

**Request:**
```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "vehicles": [
      {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
      {"id": "VEH002", "current_lat": 40.7580, "current_lon": -73.9855},
      {"id": "VEH003", "current_lat": 40.7831, "current_lon": -73.9712}
    ],
    "orders": [
      {"id": "ORD001", "pickup_lat": 40.7128, "pickup_lon": -74.0060, "dropoff_lat": 40.7589, "dropoff_lon": -73.9851},
      {"id": "ORD002", "pickup_lat": 40.7580, "pickup_lon": -73.9855, "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
      {"id": "ORD003", "pickup_lat": 40.7831, "pickup_lon": -73.9712, "dropoff_lat": 40.7489, "dropoff_lon": -73.9680},
      {"id": "ORD004", "pickup_lat": 40.7061, "pickup_lon": -73.9969, "dropoff_lat": 40.7306, "dropoff_lon": -73.9866},
      {"id": "ORD005", "pickup_lat": 40.7549, "pickup_lon": -73.9840, "dropoff_lat": 40.7829, "dropoff_lon": -73.9654}
    ],
    "algorithm": "simulated_annealing",
    "sa_params": {
      "initial_temp": 1000.0,
      "cooling_rate": 0.995,
      "max_iterations": 5000
    }
  }'
```

**Key Points:**
- Uses 3 vehicles
- Distributes 5 orders optimally
- SA algorithm finds better load balancing than greedy
- Response shows which vehicles are used and their routes

---

## Error Handling

### HTTP Status Codes

| Status Code | Meaning | Example |
|-------------|---------|---------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid input data |
| 422 | Validation Error | Pydantic validation failed |
| 500 | Internal Server Error | Server-side error |

---

### Error Response Format

All errors return a consistent JSON format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

---

### Common Errors

#### 1. Empty Vehicles List
**Request:**
```json
{
  "vehicles": [],
  "orders": [...]
}
```

**Response (400):**
```json
{
  "detail": "At least one vehicle is required"
}
```

---

#### 2. Invalid Coordinates
**Request:**
```json
{
  "vehicles": [
    {
      "id": "VEH001",
      "current_lat": 100.0,
      "current_lon": -74.0060
    }
  ],
  "orders": [...]
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "vehicles", 0, "current_lat"],
      "msg": "Latitude must be between -90 and 90",
      "input": 100.0
    }
  ]
}
```

---

#### 3. Invalid Algorithm Name
**Request:**
```json
{
  "vehicles": [...],
  "orders": [...],
  "algorithm": "invalid_algorithm"
}
```

**Response (400):**
```json
{
  "detail": "Unknown algorithm: invalid_algorithm. Available: greedy, simulated_annealing"
}
```

---

#### 4. Missing Required Fields
**Request:**
```json
{
  "vehicles": [
    {
      "id": "VEH001"
    }
  ],
  "orders": [...]
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "vehicles", 0, "current_lat"],
      "msg": "Field required"
    },
    {
      "type": "missing",
      "loc": ["body", "vehicles", 0, "current_lon"],
      "msg": "Field required"
    }
  ]
}
```

---

## Testing

### Using cURL
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test solve endpoint
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

### Using Python `requests`
```python
import requests

# Test health endpoint
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test solve endpoint
data = {
    "vehicles": [...],
    "orders": [...]
}
response = requests.post("http://localhost:8000/solve", json=data)
print(response.json())
```

### Using Postman
1. Import the Postman collection: `VRP_API.postman_collection.json`
2. Set the `base_url` variable to `http://localhost:8000`
3. Run individual requests or the entire collection

### Automated Test Suite
```bash
# Run Python test suite
python api/test_api.py

# Run bash test suite
bash api/test_api.sh
```

---

## Performance Considerations

### Algorithm Comparison

| Algorithm | Speed | Quality | Best For |
|-----------|-------|---------|----------|
| Greedy | Fast (< 0.01s) | Good | Small problems, quick results |
| Simulated Annealing | Slower (0.5-5s) | Excellent | Larger problems, optimal solutions |

### Tuning SA Parameters

For better results with Simulated Annealing:

- **Small problems (< 5 orders)**: Use default parameters
- **Medium problems (5-10 orders)**: Increase `max_iterations` to 5000-10000
- **Large problems (> 10 orders)**: Use `initial_temp=1500`, `cooling_rate=0.997`, `max_iterations=10000+`

---

## API Versioning

Current version: **v1.0.0**

The API follows semantic versioning. Breaking changes will result in a major version increment.

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing rate limiting using middleware.

---

## CORS Configuration

CORS is currently configured to allow all origins. For production use, update the CORS configuration in `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Support

For issues, questions, or contributions, please refer to the project repository.

---

## License

This project is part of the Vehicle Routing Problem (VRP) implementation.
