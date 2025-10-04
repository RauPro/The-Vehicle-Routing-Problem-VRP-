"""
Unit tests for the Greedy Nearest Neighbor algorithm.

This module contains comprehensive tests for the GreedyNearestNeighbor
algorithm implementation.
"""

import pytest
from src.models import Order, Vehicle, Route
from src.algorithms.greedy_nearest_neighbor import GreedyNearestNeighbor


class TestGreedyNearestNeighbor:
    """
    Test suite for the GreedyNearestNeighbor algorithm.
    """
    
    def test_initialization(self):
        """Test algorithm initialization with different units."""
        # Test default initialization
        algorithm = GreedyNearestNeighbor()
        assert algorithm.distance_unit == 'km'
        
        # Test custom unit
        algorithm_miles = GreedyNearestNeighbor(distance_unit='miles')
        assert algorithm_miles.distance_unit == 'miles'
    
    def test_solve_single_vehicle_single_order(self):
        """Test solving with one vehicle and one order."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = [Vehicle("V1", 40.7128, -74.0060)]
        orders = [Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)]
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # Verify results
        assert len(routes) == 1
        assert len(unassigned) == 0
        assert routes[0].get_total_orders() == 1
        assert routes[0].orders[0].id == "O1"
    
    def test_solve_single_vehicle_multiple_orders(self):
        """Test solving with one vehicle and multiple orders."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = [Vehicle("V1", 40.7128, -74.0060)]
        orders = [
            Order("O1", 40.7580, -73.9855, 40.7614, -73.9776),
            Order("O2", 40.7831, -73.9712, 40.7489, -73.9680),
            Order("O3", 40.7061, -73.9969, 40.7306, -73.9866),
        ]
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # Verify all orders are assigned
        assert len(routes) == 1
        assert len(unassigned) == 0
        assert routes[0].get_total_orders() == 3
        
        # Verify all order IDs are present
        assigned_ids = {order.id for order in routes[0].orders}
        expected_ids = {"O1", "O2", "O3"}
        assert assigned_ids == expected_ids
    
    def test_solve_multiple_vehicles_multiple_orders(self):
        """Test solving with multiple vehicles and orders."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = [
            Vehicle("V1", 40.7128, -74.0060),
            Vehicle("V2", 40.7580, -73.9855),
        ]
        orders = [
            Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
            Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
            Order("O3", 40.7831, -73.9712, 40.7489, -73.9680),
            Order("O4", 40.7061, -73.9969, 40.7306, -73.9866),
        ]
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # Verify all orders are assigned
        assert len(routes) == 2
        assert len(unassigned) == 0
        
        total_assigned = sum(route.get_total_orders() for route in routes)
        assert total_assigned == 4
        
        # Verify all order IDs are present
        all_assigned_ids = set()
        for route in routes:
            for order in route.orders:
                all_assigned_ids.add(order.id)
        
        expected_ids = {"O1", "O2", "O3", "O4"}
        assert all_assigned_ids == expected_ids
    
    def test_solve_empty_vehicles_raises_error(self):
        """Test that empty vehicle list raises ValueError."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = []
        orders = [Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)]
        
        with pytest.raises(ValueError, match="Vehicles list cannot be empty"):
            algorithm.solve(vehicles, orders)
    
    def test_solve_empty_orders_raises_error(self):
        """Test that empty orders list raises ValueError."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = [Vehicle("V1", 40.7128, -74.0060)]
        orders = []
        
        with pytest.raises(ValueError, match="Orders list cannot be empty"):
            algorithm.solve(vehicles, orders)
    
    def test_calculate_total_distance_empty_route(self):
        """Test distance calculation for an empty route."""
        algorithm = GreedyNearestNeighbor()
        
        vehicle = Vehicle("V1", 40.7128, -74.0060)
        route = Route(vehicle=vehicle)
        
        distance = algorithm.calculate_total_distance(route)
        assert distance == 0.0
    
    def test_calculate_total_distance_single_order(self):
        """Test distance calculation for a route with one order."""
        algorithm = GreedyNearestNeighbor()
        
        vehicle = Vehicle("V1", 40.7128, -74.0060)
        route = Route(vehicle=vehicle)
        
        order = Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)
        route.add_order(order)
        
        distance = algorithm.calculate_total_distance(route)
        
        # Distance should be positive and reasonable
        assert distance > 0
        # Should be less than 100 km for NYC area
        assert distance < 100
    
    def test_calculate_total_distance_multiple_orders(self):
        """Test distance calculation for a route with multiple orders."""
        algorithm = GreedyNearestNeighbor()
        
        vehicle = Vehicle("V1", 40.7128, -74.0060)
        route = Route(vehicle=vehicle)
        
        orders = [
            Order("O1", 40.7580, -73.9855, 40.7614, -73.9776),
            Order("O2", 40.7831, -73.9712, 40.7489, -73.9680),
        ]
        
        for order in orders:
            route.add_order(order)
        
        distance = algorithm.calculate_total_distance(route)
        
        # Distance should increase with more orders
        assert distance > 0
        assert distance < 200  # Reasonable for NYC area
    
    def test_get_solution_summary(self):
        """Test generation of solution summary."""
        algorithm = GreedyNearestNeighbor()
        
        vehicles = [
            Vehicle("V1", 40.7128, -74.0060),
            Vehicle("V2", 40.7580, -73.9855),
        ]
        orders = [
            Order("O1", 40.7128, -74.0060, 40.7589, -73.9851),
            Order("O2", 40.7580, -73.9855, 40.7614, -73.9776),
        ]
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        summary = algorithm.get_solution_summary(routes, unassigned)
        
        # Verify summary structure
        assert 'total_vehicles' in summary
        assert 'total_orders' in summary
        assert 'assigned_orders' in summary
        assert 'unassigned_orders' in summary
        assert 'routes_used' in summary
        assert 'total_distance' in summary
        assert 'average_distance_per_route' in summary
        assert 'distance_unit' in summary
        assert 'route_details' in summary
        
        # Verify summary values
        assert summary['total_vehicles'] == 2
        assert summary['total_orders'] == 2
        assert summary['assigned_orders'] == 2
        assert summary['unassigned_orders'] == 0
        assert summary['distance_unit'] == 'km'
        
        # Verify route details
        assert len(summary['route_details']) == 2
        for detail in summary['route_details']:
            assert 'vehicle_id' in detail
            assert 'orders_count' in detail
            assert 'total_distance' in detail
            assert 'order_sequence' in detail
    
    def test_greedy_selection_nearest_order(self):
        """Test that the algorithm selects the nearest order."""
        algorithm = GreedyNearestNeighbor()
        
        # Vehicle at Lower Manhattan
        vehicles = [Vehicle("V1", 40.7128, -74.0060)]
        
        # Order close to vehicle
        close_order = Order("O1", 40.7150, -74.0050, 40.7200, -74.0000)
        
        # Order far from vehicle
        far_order = Order("O2", 40.8500, -73.8500, 40.8600, -73.8400)
        
        orders = [far_order, close_order]  # Intentionally reverse order
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # The first order assigned should be the closer one
        assert routes[0].orders[0].id == "O1"
        assert routes[0].orders[1].id == "O2"
    
    def test_distance_units(self):
        """Test that different distance units work correctly."""
        # Test with kilometers
        algorithm_km = GreedyNearestNeighbor(distance_unit='km')
        
        vehicle = Vehicle("V1", 40.7128, -74.0060)
        route_km = Route(vehicle=vehicle)
        order = Order("O1", 40.7580, -73.9855, 40.7614, -73.9776)
        route_km.add_order(order)
        
        distance_km = algorithm_km.calculate_total_distance(route_km)
        
        # Test with miles
        algorithm_miles = GreedyNearestNeighbor(distance_unit='miles')
        route_miles = Route(vehicle=Vehicle("V2", 40.7128, -74.0060))
        route_miles.add_order(Order("O2", 40.7580, -73.9855, 40.7614, -73.9776))
        
        distance_miles = algorithm_miles.calculate_total_distance(route_miles)
        
        # Miles should be less than kilometers (approximately 0.621 ratio)
        assert distance_miles < distance_km
        assert 0.6 < (distance_miles / distance_km) < 0.65
    
    def test_round_robin_assignment(self):
        """Test that orders are distributed across vehicles in round-robin."""
        algorithm = GreedyNearestNeighbor()
        
        # Create 3 vehicles at the same location
        vehicles = [
            Vehicle("V1", 40.7128, -74.0060),
            Vehicle("V2", 40.7128, -74.0060),
            Vehicle("V3", 40.7128, -74.0060),
        ]
        
        # Create 6 orders all at similar distances
        orders = [
            Order(f"O{i}", 40.7150 + i*0.001, -74.0050, 40.7200, -74.0000)
            for i in range(1, 7)
        ]
        
        routes, unassigned = algorithm.solve(vehicles, orders)
        
        # Each vehicle should get approximately equal orders
        order_counts = [route.get_total_orders() for route in routes]
        assert len(unassigned) == 0
        assert sum(order_counts) == 6
        
        # All vehicles should have at least one order
        assert all(count > 0 for count in order_counts)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
