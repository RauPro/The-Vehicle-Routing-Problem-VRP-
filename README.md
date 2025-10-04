# Vehicle Routing Problem (VRP)

A comprehensive solution for vehicle routing optimization.

## Project Structure

```
The Vehicle Routing Problem (VRP)/
├── src/
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       ├── order.py      # Order data structure
│       ├── vehicle.py    # Vehicle data structure
│       └── route.py      # Route data structure
├── main.py               # Main entry point
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Core Data Structures

### Order
Represents a delivery order with pickup and dropoff locations.

**Attributes:**
- `id` (str): Unique identifier for the order
- `pickup_lat` (float): Latitude of pickup location
- `pickup_lon` (float): Longitude of pickup location
- `dropoff_lat` (float): Latitude of dropoff location
- `dropoff_lon` (float): Longitude of dropoff location

### Vehicle
Represents a delivery vehicle with its current location.

**Attributes:**
- `id` (str): Unique identifier for the vehicle
- `current_lat` (float): Current latitude position
- `current_lon` (float): Current longitude position

### Route
Represents a route containing orders assigned to a vehicle.

**Attributes:**
- `vehicle` (Vehicle): The assigned vehicle
- `orders` (List[Order]): List of orders in the route

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using UV (recommended):
```bash
uv pip install -r requirements.txt
```

## Usage

Run the demonstration:
```bash
python main.py
```

### Example Usage

```python
from src.models import Order, Vehicle, Route

# Create an order
order = Order(
    id="ORD001",
    pickup_lat=40.7128,
    pickup_lon=-74.0060,
    dropoff_lat=40.7589,
    dropoff_lon=-73.9851
)

# Create a vehicle
vehicle = Vehicle(
    id="VEH001",
    current_lat=40.7128,
    current_lon=-74.0060
)

# Create a route
route = Route(vehicle=vehicle)
route.add_order(order)

print(f"Total orders: {route.get_total_orders()}")
```

## Features

- ✅ Type-safe data structures with full type hints
- ✅ Coordinate validation for all geographic points
- ✅ Clean, modular architecture
- ✅ Comprehensive documentation
- ✅ Edge case handling

## Development

This project follows PEP 8 style guidelines and uses Python dataclasses for clean, maintainable code.

## License

MIT License
