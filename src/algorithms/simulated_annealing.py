"""
Simulated Annealing Algorithm for the Vehicle Routing Problem.

This module implements a Simulated Annealing (SA) metaheuristic for optimizing
vehicle routes. SA is a probabilistic technique that mimics the annealing process
in metallurgy, allowing the algorithm to escape local optima by occasionally
accepting worse solutions with a probability that decreases over time.

The algorithm iteratively improves a solution by making small random changes
and accepting or rejecting them based on the cost difference and current temperature.
"""

import math
import random
import copy
from typing import List, Tuple, Dict, Any, Optional
from ..models import Order, Vehicle, Route
from ..utils import haversine_distance


class SimulatedAnnealing:
    """
    Implements Simulated Annealing algorithm for the Vehicle Routing Problem.
    
    The algorithm uses a temperature-based acceptance criterion to explore the
    solution space and find near-optimal vehicle routes.
    
    Solution Representation:
        A solution is represented as a list of lists, where each inner list
        contains Order objects assigned to a vehicle.
        Example: [[Order1, Order3], [Order2, Order4, Order5]]
        This means Vehicle 0 handles Orders 1 and 3, Vehicle 1 handles Orders 2, 4, and 5.
    
    Key Parameters:
        - initial_temp: Starting temperature (higher = more exploration)
        - final_temp: Ending temperature (determines stopping point)
        - cooling_rate: Rate at which temperature decreases (0 < alpha < 1)
        - max_iterations: Maximum number of iterations to run
    """
    
    def __init__(
        self,
        initial_temp: float = 1000.0,
        final_temp: float = 1.0,
        cooling_rate: float = 0.995,
        max_iterations: int = 10000,
        distance_unit: str = 'km',
        verbose: bool = False
    ):
        """
        Initialize the Simulated Annealing algorithm.
        
        Parameters:
            initial_temp (float): Initial temperature for SA. Higher values allow
                more exploration. Defaults to 1000.0.
            final_temp (float): Final temperature at which to stop. Defaults to 1.0.
            cooling_rate (float): Rate at which temperature decreases (alpha).
                Should be between 0 and 1, typically 0.95-0.999. Defaults to 0.995.
            max_iterations (int): Maximum number of iterations. Defaults to 10000.
            distance_unit (str): Unit for distance calculations ('km', 'miles', etc.).
                Defaults to 'km'.
            verbose (bool): If True, prints detailed iteration logs. Defaults to False.
        """
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.distance_unit = distance_unit
        self.verbose = verbose
        
        # Statistics tracking
        self.iteration_history: List[Dict[str, Any]] = []
        self.best_cost_history: List[float] = []
        self.current_cost_history: List[float] = []
        self.acceptance_history: List[bool] = []
    
    def solve(
        self,
        vehicles: List[Vehicle],
        orders: List[Order],
        initial_solution: Optional[List[List[Order]]] = None
    ) -> Tuple[List[Route], float, Dict[str, Any]]:
        """
        Find an optimized solution using Simulated Annealing.
        
        Parameters:
            vehicles (List[Vehicle]): List of available vehicles.
            orders (List[Order]): List of orders to be assigned.
            initial_solution (Optional[List[List[Order]]]): Starting solution.
                If None, a random solution is generated.
        
        Returns:
            Tuple[List[Route], float, Dict[str, Any]]: A tuple containing:
                - List of optimized routes (one per vehicle)
                - Total cost (distance) of the best solution
                - Dictionary of statistics and metrics from the optimization
        
        Raises:
            ValueError: If vehicles or orders lists are empty.
        """
        # Validate input
        if not vehicles:
            raise ValueError("Vehicles list cannot be empty")
        if not orders:
            raise ValueError("Orders list cannot be empty")
        
        # Generate or use provided initial solution
        if initial_solution is None:
            current_solution = self._generate_initial_solution(vehicles, orders)
        else:
            current_solution = copy.deepcopy(initial_solution)
        
        # Calculate initial cost
        current_cost = self.calculate_total_cost(current_solution, vehicles)
        
        # Track the best solution found
        best_solution = copy.deepcopy(current_solution)
        best_cost = current_cost
        
        # Initialize temperature
        temperature = self.initial_temp
        
        # Reset statistics
        self.iteration_history = []
        self.best_cost_history = []
        self.current_cost_history = []
        self.acceptance_history = []
        
        iteration = 0
        
        if self.verbose:
            print("=" * 80)
            print("Simulated Annealing - Iteration Log")
            print("=" * 80)
            print(f"{'Iter':<8} {'Temp':<10} {'Current':<12} {'Neighbor':<12} "
                  f"{'ΔE':<12} {'Accept':<8} {'Best':<12}")
            print("-" * 80)
        
        # Main SA loop
        while temperature > self.final_temp and iteration < self.max_iterations:
            # Generate a neighbor solution
            neighbor_solution = self.get_neighbor(current_solution)
            
            # Calculate neighbor cost
            neighbor_cost = self.calculate_total_cost(neighbor_solution, vehicles)
            
            # Calculate cost difference (delta E)
            delta_e = neighbor_cost - current_cost
            
            # Decide whether to accept the neighbor
            accepted = False
            if delta_e < 0:
                # Better solution - always accept
                accepted = True
            else:
                # Worse solution - accept with probability
                acceptance_probability = math.exp(-delta_e / temperature)
                if random.random() < acceptance_probability:
                    accepted = True
            
            # Update current solution if accepted
            if accepted:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                
                # Update best solution if this is the best so far
                if current_cost < best_cost:
                    best_solution = copy.deepcopy(current_solution)
                    best_cost = current_cost
            
            # Track statistics
            self.best_cost_history.append(best_cost)
            self.current_cost_history.append(current_cost)
            self.acceptance_history.append(accepted)
            
            # Log iteration details
            if self.verbose:
                print(f"{iteration:<8} {temperature:<10.2f} {current_cost:<12.2f} "
                      f"{neighbor_cost:<12.2f} {delta_e:<12.2f} "
                      f"{'Y' if accepted else 'N':<8} {best_cost:<12.2f}")
            
            # Store detailed iteration info
            self.iteration_history.append({
                'iteration': iteration,
                'temperature': temperature,
                'current_cost': current_cost,
                'neighbor_cost': neighbor_cost,
                'delta_e': delta_e,
                'accepted': accepted,
                'best_cost': best_cost
            })
            
            # Cool down temperature
            temperature *= self.cooling_rate
            iteration += 1
        
        if self.verbose:
            print("=" * 80)
            print(f"Optimization Complete: {iteration} iterations")
            print(f"Best Cost: {best_cost:.2f} {self.distance_unit}")
            print("=" * 80)
        
        # Convert best solution to Route objects
        routes = self._solution_to_routes(best_solution, vehicles)
        
        # Generate statistics
        statistics = self._generate_statistics(iteration, best_cost)
        
        return routes, best_cost, statistics
    
    def calculate_total_cost(
        self,
        solution: List[List[Order]],
        vehicles: List[Vehicle]
    ) -> float:
        """
        Calculate the total cost (distance) for a complete solution.
        
        The cost includes:
        1. Distance from each vehicle's start to first order's pickup
        2. Distance from each pickup to its dropoff
        3. Distance between consecutive orders (previous dropoff to next pickup)
        
        Parameters:
            solution (List[List[Order]]): Solution to evaluate. Each inner list
                contains orders assigned to a vehicle.
            vehicles (List[Vehicle]): List of vehicles with starting positions.
        
        Returns:
            float: Total distance across all vehicle routes in the solution.
        
        Examples:
            >>> sa = SimulatedAnnealing()
            >>> solution = [[order1, order2], [order3]]
            >>> vehicles = [vehicle1, vehicle2]
            >>> cost = sa.calculate_total_cost(solution, vehicles)
        """
        total_cost = 0.0
        
        for vehicle_idx, route_orders in enumerate(solution):
            if not route_orders:
                # Empty route contributes no cost
                continue
            
            vehicle = vehicles[vehicle_idx]
            current_position = vehicle.get_current_coordinates()
            
            for order in route_orders:
                pickup_coords = order.get_pickup_coordinates()
                dropoff_coords = order.get_dropoff_coordinates()
                
                # Distance from current position to pickup
                total_cost += haversine_distance(
                    current_position,
                    pickup_coords,
                    unit=self.distance_unit
                )
                
                # Distance from pickup to dropoff
                total_cost += haversine_distance(
                    pickup_coords,
                    dropoff_coords,
                    unit=self.distance_unit
                )
                
                # Update current position to dropoff location
                current_position = dropoff_coords
        
        return total_cost
    
    def get_neighbor(self, solution: List[List[Order]]) -> List[List[Order]]:
        """
        Generate a neighbor solution by making a small random change.
        
        This function implements multiple neighborhood operators:
        1. Intra-route swap: Swap two orders within the same route
        2. Inter-route move: Move an order from one route to another
        3. Inter-route swap: Swap an order between two different routes
        
        The operator is selected randomly with configurable probabilities.
        
        Parameters:
            solution (List[List[Order]]): Current solution to modify.
        
        Returns:
            List[List[Order]]: A new neighbor solution with a small modification.
        """
        # Create a deep copy to avoid modifying the original
        neighbor = copy.deepcopy(solution)
        
        # Get non-empty routes
        non_empty_routes = [i for i, route in enumerate(neighbor) if route]
        
        if not non_empty_routes:
            # No orders to move, return original
            return neighbor
        
        # Choose an operator randomly
        # 40% intra-route swap, 40% inter-route move, 20% inter-route swap
        operator = random.choices(
            ['intra_swap', 'inter_move', 'inter_swap'],
            weights=[0.4, 0.4, 0.2],
            k=1
        )[0]
        
        if operator == 'intra_swap' and non_empty_routes:
            # Intra-route swap: swap two orders within the same route
            neighbor = self._intra_route_swap(neighbor, non_empty_routes)
        
        elif operator == 'inter_move' and non_empty_routes:
            # Inter-route move: move an order from one route to another
            neighbor = self._inter_route_move(neighbor, non_empty_routes)
        
        elif operator == 'inter_swap' and len(non_empty_routes) >= 2:
            # Inter-route swap: swap orders between two different routes
            neighbor = self._inter_route_swap(neighbor, non_empty_routes)
        
        return neighbor
    
    def _intra_route_swap(
        self,
        solution: List[List[Order]],
        non_empty_routes: List[int]
    ) -> List[List[Order]]:
        """
        Swap two orders within the same route.
        
        Parameters:
            solution (List[List[Order]]): Current solution.
            non_empty_routes (List[int]): Indices of routes with orders.
        
        Returns:
            List[List[Order]]: Modified solution with swapped orders.
        """
        # Select a random non-empty route with at least 2 orders
        routes_with_multiple = [
            i for i in non_empty_routes if len(solution[i]) >= 2
        ]
        
        if not routes_with_multiple:
            return solution
        
        route_idx = random.choice(routes_with_multiple)
        route = solution[route_idx]
        
        # Select two different positions to swap
        pos1, pos2 = random.sample(range(len(route)), 2)
        
        # Swap the orders
        route[pos1], route[pos2] = route[pos2], route[pos1]
        
        return solution
    
    def _inter_route_move(
        self,
        solution: List[List[Order]],
        non_empty_routes: List[int]
    ) -> List[List[Order]]:
        """
        Move an order from one route to another.
        
        Parameters:
            solution (List[List[Order]]): Current solution.
            non_empty_routes (List[int]): Indices of routes with orders.
        
        Returns:
            List[List[Order]]: Modified solution with moved order.
        """
        # Select a random non-empty route to take from
        from_route_idx = random.choice(non_empty_routes)
        from_route = solution[from_route_idx]
        
        # Select a random order to move
        order_idx = random.randint(0, len(from_route) - 1)
        order = from_route.pop(order_idx)
        
        # Select a random route to move to (can be different or same)
        to_route_idx = random.randint(0, len(solution) - 1)
        to_route = solution[to_route_idx]
        
        # Insert at a random position in the destination route
        if to_route:
            insert_pos = random.randint(0, len(to_route))
        else:
            insert_pos = 0
        
        to_route.insert(insert_pos, order)
        
        return solution
    
    def _inter_route_swap(
        self,
        solution: List[List[Order]],
        non_empty_routes: List[int]
    ) -> List[List[Order]]:
        """
        Swap orders between two different routes.
        
        Parameters:
            solution (List[List[Order]]): Current solution.
            non_empty_routes (List[int]): Indices of routes with orders.
        
        Returns:
            List[List[Order]]: Modified solution with swapped orders.
        """
        # Select two different non-empty routes
        if len(non_empty_routes) < 2:
            return solution
        
        route1_idx, route2_idx = random.sample(non_empty_routes, 2)
        route1 = solution[route1_idx]
        route2 = solution[route2_idx]
        
        # Select random positions in each route
        pos1 = random.randint(0, len(route1) - 1)
        pos2 = random.randint(0, len(route2) - 1)
        
        # Swap the orders
        route1[pos1], route2[pos2] = route2[pos2], route1[pos1]
        
        return solution
    
    def _generate_initial_solution(
        self,
        vehicles: List[Vehicle],
        orders: List[Order]
    ) -> List[List[Order]]:
        """
        Generate a random initial solution.
        
        This method randomly assigns all orders to vehicles, ensuring each
        order is assigned exactly once.
        
        Parameters:
            vehicles (List[Vehicle]): List of available vehicles.
            orders (List[Order]): List of orders to assign.
        
        Returns:
            List[List[Order]]: Random initial solution.
        """
        # Create empty routes for each vehicle
        solution = [[] for _ in vehicles]
        
        # Shuffle orders to randomize assignment
        shuffled_orders = orders.copy()
        random.shuffle(shuffled_orders)
        
        # Assign orders to vehicles in round-robin fashion
        for i, order in enumerate(shuffled_orders):
            vehicle_idx = i % len(vehicles)
            solution[vehicle_idx].append(order)
        
        return solution
    
    def _solution_to_routes(
        self,
        solution: List[List[Order]],
        vehicles: List[Vehicle]
    ) -> List[Route]:
        """
        Convert a solution representation to Route objects.
        
        Parameters:
            solution (List[List[Order]]): Solution to convert.
            vehicles (List[Vehicle]): List of vehicles.
        
        Returns:
            List[Route]: List of Route objects.
        """
        routes = []
        
        for vehicle_idx, route_orders in enumerate(solution):
            vehicle = vehicles[vehicle_idx]
            route = Route(vehicle=vehicle, orders=route_orders.copy())
            routes.append(route)
        
        return routes
    
    def _generate_statistics(
        self,
        iterations: int,
        best_cost: float
    ) -> Dict[str, Any]:
        """
        Generate statistics about the optimization process.
        
        Parameters:
            iterations (int): Number of iterations completed.
            best_cost (float): Best cost found.
        
        Returns:
            Dict[str, Any]: Dictionary containing optimization statistics.
        """
        if not self.acceptance_history:
            return {}
        
        total_attempts = len(self.acceptance_history)
        total_accepted = sum(self.acceptance_history)
        acceptance_rate = total_accepted / total_attempts if total_attempts > 0 else 0
        
        # Calculate improvement statistics
        initial_cost = self.current_cost_history[0] if self.current_cost_history else 0
        improvement = initial_cost - best_cost
        improvement_pct = (improvement / initial_cost * 100) if initial_cost > 0 else 0
        
        # Count better vs worse acceptances
        better_accepted = sum(
            1 for i, accepted in enumerate(self.acceptance_history)
            if accepted and self.iteration_history[i]['delta_e'] < 0
        )
        worse_accepted = total_accepted - better_accepted
        
        return {
            'iterations_completed': iterations,
            'total_attempts': total_attempts,
            'total_accepted': total_accepted,
            'acceptance_rate': round(acceptance_rate, 4),
            'better_accepted': better_accepted,
            'worse_accepted': worse_accepted,
            'initial_cost': round(initial_cost, 2),
            'final_cost': round(best_cost, 2),
            'improvement': round(improvement, 2),
            'improvement_percentage': round(improvement_pct, 2),
            'distance_unit': self.distance_unit,
            'initial_temperature': self.initial_temp,
            'final_temperature': self.final_temp,
            'cooling_rate': self.cooling_rate,
        }
    
    def get_solution_summary(
        self,
        routes: List[Route],
        total_cost: float
    ) -> Dict[str, Any]:
        """
        Generate a summary of the routing solution.
        
        Parameters:
            routes (List[Route]): List of routes with assigned orders.
            total_cost (float): Total cost of the solution.
        
        Returns:
            Dict[str, Any]: Summary statistics about the solution.
        """
        total_orders = sum(route.get_total_orders() for route in routes)
        routes_used = sum(1 for route in routes if not route.is_empty())
        
        avg_distance = (
            total_cost / routes_used if routes_used > 0 else 0.0
        )
        
        # Build detailed route information
        route_details = []
        for route in routes:
            route_details.append({
                'vehicle_id': route.vehicle.id,
                'orders_count': route.get_total_orders(),
                'order_sequence': [order.id for order in route.orders]
            })
        
        return {
            'total_vehicles': len(routes),
            'total_orders': total_orders,
            'routes_used': routes_used,
            'total_distance': round(total_cost, 2),
            'average_distance_per_route': round(avg_distance, 2),
            'distance_unit': self.distance_unit,
            'route_details': route_details
        }
