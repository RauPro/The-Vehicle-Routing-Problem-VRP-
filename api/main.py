"""
VRP API - FastAPI Application

This module provides a REST API for solving the Vehicle Routing Problem
using both Greedy and Simulated Annealing algorithms.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.append(str(Path(__file__).parent.parent))

from src.models import Order, Vehicle
from src.algorithms import GreedyNearestNeighbor, SimulatedAnnealing


# Pydantic models for request/response validation
class OrderRequest(BaseModel):
    """
    Model for an order in the API request.
    
    Attributes:
        id (str): Unique identifier for the order.
        pickup_lat (float): Latitude of pickup location (-90 to 90).
        pickup_lon (float): Longitude of pickup location (-180 to 180).
        dropoff_lat (float): Latitude of dropoff location (-90 to 90).
        dropoff_lon (float): Longitude of dropoff location (-180 to 180).
    """
    id: str = Field(..., description="Unique order identifier", example="ORD001")
    pickup_lat: float = Field(..., ge=-90, le=90, description="Pickup latitude", example=40.7128)
    pickup_lon: float = Field(..., ge=-180, le=180, description="Pickup longitude", example=-74.0060)
    dropoff_lat: float = Field(..., ge=-90, le=90, description="Dropoff latitude", example=40.7589)
    dropoff_lon: float = Field(..., ge=-180, le=180, description="Dropoff longitude", example=-73.9851)
    
    @validator('id')
    def validate_id(cls, v):
        """Validate that ID is not empty."""
        if not v or not v.strip():
            raise ValueError('Order ID cannot be empty')
        return v.strip()


class VehicleRequest(BaseModel):
    """
    Model for a vehicle in the API request.
    
    Attributes:
        id (str): Unique identifier for the vehicle.
        current_lat (float): Current latitude position (-90 to 90).
        current_lon (float): Current longitude position (-180 to 180).
    """
    id: str = Field(..., description="Unique vehicle identifier", example="VEH001")
    current_lat: float = Field(..., ge=-90, le=90, description="Current latitude", example=40.7128)
    current_lon: float = Field(..., ge=-180, le=180, description="Current longitude", example=-74.0060)
    
    @validator('id')
    def validate_id(cls, v):
        """Validate that ID is not empty."""
        if not v or not v.strip():
            raise ValueError('Vehicle ID cannot be empty')
        return v.strip()


class SolveRequest(BaseModel):
    """
    Model for the /solve endpoint request.
    
    Attributes:
        vehicles (List[VehicleRequest]): List of available vehicles.
        orders (List[OrderRequest]): List of orders to assign.
        algorithm (str): Algorithm to use ('greedy' or 'simulated_annealing').
        distance_unit (str): Unit for distance ('km', 'miles', 'meters', 'feet').
        sa_params (Optional[Dict]): Parameters for Simulated Annealing.
    """
    vehicles: List[VehicleRequest] = Field(..., min_items=1, description="List of vehicles")
    orders: List[OrderRequest] = Field(..., min_items=1, description="List of orders")
    algorithm: str = Field(
        default="simulated_annealing",
        description="Algorithm to use",
        example="simulated_annealing"
    )
    distance_unit: str = Field(
        default="km",
        description="Distance unit",
        example="km"
    )
    sa_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Simulated Annealing parameters"
    )
    
    @validator('algorithm')
    def validate_algorithm(cls, v):
        """Validate algorithm selection."""
        allowed = ['greedy', 'simulated_annealing', 'sa']
        if v.lower() not in allowed:
            raise ValueError(f'Algorithm must be one of: {allowed}')
        return v.lower()
    
    @validator('distance_unit')
    def validate_distance_unit(cls, v):
        """Validate distance unit."""
        allowed = ['km', 'kilometers', 'miles', 'meters', 'metres', 'm', 'feet', 'ft']
        if v.lower() not in allowed:
            raise ValueError(f'Distance unit must be one of: {allowed}')
        return v.lower()


class RouteResponse(BaseModel):
    """
    Model for a single route in the response.
    
    Attributes:
        vehicle_id (str): ID of the vehicle.
        orders (List[str]): List of order IDs in sequence.
        total_distance (float): Total distance for this route.
    """
    vehicle_id: str
    orders: List[str]
    total_distance: float


class SolveResponse(BaseModel):
    """
    Model for the /solve endpoint response.
    
    Attributes:
        status (str): Response status ('success' or 'error').
        algorithm_used (str): Algorithm that was used.
        total_distance (float): Total distance across all routes.
        distance_unit (str): Unit of distance.
        routes (List[RouteResponse]): List of vehicle routes.
        statistics (Optional[Dict]): Additional statistics.
        unassigned_orders (List[str]): IDs of unassigned orders.
    """
    status: str
    algorithm_used: str
    total_distance: float
    distance_unit: str
    routes: List[RouteResponse]
    statistics: Optional[Dict[str, Any]] = None
    unassigned_orders: List[str] = []


class HealthResponse(BaseModel):
    """Model for the health check response."""
    status: str
    message: str
    version: str


# Create FastAPI app
app = FastAPI(
    title="Vehicle Routing Problem API",
    description="REST API for solving Vehicle Routing Problems using Greedy and Simulated Annealing algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """
    Root endpoint - returns API information.
    
    Returns:
        HealthResponse: API status and version information.
    """
    return HealthResponse(
        status="online",
        message="Vehicle Routing Problem API is running",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: API health status.
    """
    return HealthResponse(
        status="healthy",
        message="All systems operational",
        version="1.0.0"
    )


@app.post(
    "/solve",
    response_model=SolveResponse,
    status_code=status.HTTP_200_OK,
    tags=["VRP Solver"],
    summary="Solve Vehicle Routing Problem",
    description="Solve a VRP instance using the specified algorithm"
)
async def solve_vrp(request: SolveRequest):
    """
    Solve a Vehicle Routing Problem instance.
    
    This endpoint accepts a list of vehicles and orders, applies the selected
    optimization algorithm, and returns the optimized routes.
    
    Args:
        request (SolveRequest): Request containing vehicles, orders, and parameters.
    
    Returns:
        SolveResponse: Optimized routes and statistics.
    
    Raises:
        HTTPException: If there's an error during solving.
    
    Examples:
        ```json
        {
            "vehicles": [
                {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060}
            ],
            "orders": [
                {
                    "id": "ORD001",
                    "pickup_lat": 40.7580,
                    "pickup_lon": -73.9855,
                    "dropoff_lat": 40.7614,
                    "dropoff_lon": -73.9776
                }
            ],
            "algorithm": "simulated_annealing",
            "distance_unit": "km"
        }
        ```
    """
    try:
        # Convert request models to domain models
        vehicles = [
            Vehicle(
                id=v.id,
                current_lat=v.current_lat,
                current_lon=v.current_lon
            )
            for v in request.vehicles
        ]
        
        orders = [
            Order(
                id=o.id,
                pickup_lat=o.pickup_lat,
                pickup_lon=o.pickup_lon,
                dropoff_lat=o.dropoff_lat,
                dropoff_lon=o.dropoff_lon
            )
            for o in request.orders
        ]
        
        # Validate unique IDs
        vehicle_ids = [v.id for v in request.vehicles]
        if len(vehicle_ids) != len(set(vehicle_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle IDs must be unique"
            )
        
        order_ids = [o.id for o in request.orders]
        if len(order_ids) != len(set(order_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order IDs must be unique"
            )
        
        # Solve based on selected algorithm
        if request.algorithm in ['greedy']:
            routes, total_distance, statistics, unassigned = solve_with_greedy(
                vehicles, orders, request.distance_unit
            )
            algorithm_used = "Greedy Nearest Neighbor"
        
        else:  # simulated_annealing or sa
            routes, total_distance, statistics, unassigned = solve_with_sa(
                vehicles, orders, request.distance_unit, request.sa_params
            )
            algorithm_used = "Simulated Annealing"
        
        # Build response
        return SolveResponse(
            status="success",
            algorithm_used=algorithm_used,
            total_distance=round(total_distance, 2),
            distance_unit=request.distance_unit,
            routes=routes,
            statistics=statistics,
            unassigned_orders=unassigned
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error solving VRP: {str(e)}"
        )


def solve_with_greedy(
    vehicles: List[Vehicle],
    orders: List[Order],
    distance_unit: str
) -> tuple:
    """
    Solve VRP using Greedy Nearest Neighbor algorithm.
    
    Args:
        vehicles (List[Vehicle]): List of vehicles.
        orders (List[Order]): List of orders.
        distance_unit (str): Distance unit.
    
    Returns:
        tuple: (routes, total_distance, statistics, unassigned_orders)
    """
    algorithm = GreedyNearestNeighbor(distance_unit=distance_unit)
    route_objects, unassigned = algorithm.solve(vehicles, orders)
    
    # Calculate total distance
    total_distance = sum(
        algorithm.calculate_total_distance(route)
        for route in route_objects
    )
    
    # Build route responses
    routes = [
        RouteResponse(
            vehicle_id=route.vehicle.id,
            orders=[order.id for order in route.orders],
            total_distance=round(algorithm.calculate_total_distance(route), 2)
        )
        for route in route_objects
    ]
    
    # Build statistics
    summary = algorithm.get_solution_summary(route_objects, unassigned)
    statistics = {
        "total_vehicles": summary['total_vehicles'],
        "total_orders": summary['total_orders'],
        "assigned_orders": summary['assigned_orders'],
        "routes_used": summary['routes_used'],
        "average_distance_per_route": summary['average_distance_per_route']
    }
    
    unassigned_ids = [order.id for order in unassigned]
    
    return routes, total_distance, statistics, unassigned_ids


def solve_with_sa(
    vehicles: List[Vehicle],
    orders: List[Order],
    distance_unit: str,
    sa_params: Optional[Dict[str, Any]]
) -> tuple:
    """
    Solve VRP using Simulated Annealing algorithm.
    
    Args:
        vehicles (List[Vehicle]): List of vehicles.
        orders (List[Order]): List of orders.
        distance_unit (str): Distance unit.
        sa_params (Optional[Dict]): SA parameters.
    
    Returns:
        tuple: (routes, total_distance, statistics, unassigned_orders)
    """
    # Set default parameters
    params = {
        'initial_temp': 1000.0,
        'final_temp': 1.0,
        'cooling_rate': 0.995,
        'max_iterations': 10000,
        'distance_unit': distance_unit,
        'verbose': False
    }
    
    # Override with provided parameters
    if sa_params:
        params.update(sa_params)
    
    algorithm = SimulatedAnnealing(**params)
    route_objects, total_cost, stats = algorithm.solve(vehicles, orders)
    
    # Build route responses
    routes = [
        RouteResponse(
            vehicle_id=route.vehicle.id,
            orders=[order.id for order in route.orders],
            total_distance=round(
                algorithm.calculate_total_cost([route.orders], [route.vehicle]),
                2
            )
        )
        for route in route_objects
    ]
    
    # Build statistics
    statistics = {
        "iterations_completed": stats['iterations_completed'],
        "acceptance_rate": stats['acceptance_rate'],
        "better_accepted": stats['better_accepted'],
        "worse_accepted": stats['worse_accepted'],
        "initial_cost": stats['initial_cost'],
        "final_cost": stats['final_cost'],
        "improvement": stats['improvement'],
        "improvement_percentage": stats['improvement_percentage'],
        "total_vehicles": len(vehicles),
        "total_orders": len(orders),
        "routes_used": sum(1 for r in route_objects if not r.is_empty())
    }
    
    # No unassigned orders with SA (all are always assigned)
    unassigned_ids = []
    
    return routes, total_cost, statistics, unassigned_ids


@app.get("/algorithms", tags=["Information"])
async def list_algorithms():
    """
    List available algorithms and their parameters.
    
    Returns:
        dict: Information about available algorithms.
    """
    return {
        "algorithms": [
            {
                "name": "greedy",
                "full_name": "Greedy Nearest Neighbor",
                "description": "Fast baseline algorithm that assigns nearest unassigned orders",
                "time_complexity": "O(v × o²)",
                "parameters": {}
            },
            {
                "name": "simulated_annealing",
                "aliases": ["sa"],
                "full_name": "Simulated Annealing",
                "description": "Advanced metaheuristic that escapes local optima",
                "time_complexity": "O(iterations × orders)",
                "typical_improvement": "18-61% better than greedy",
                "parameters": {
                    "initial_temp": {
                        "type": "float",
                        "default": 1000.0,
                        "description": "Starting temperature",
                        "range": "100-5000"
                    },
                    "final_temp": {
                        "type": "float",
                        "default": 1.0,
                        "description": "Ending temperature",
                        "range": "0.1-10"
                    },
                    "cooling_rate": {
                        "type": "float",
                        "default": 0.995,
                        "description": "Temperature decrease rate",
                        "range": "0.90-0.999"
                    },
                    "max_iterations": {
                        "type": "int",
                        "default": 10000,
                        "description": "Maximum iterations",
                        "range": "1000-50000"
                    }
                }
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
