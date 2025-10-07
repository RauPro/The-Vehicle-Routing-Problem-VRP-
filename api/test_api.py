"""
API Test Suite

This module contains tests for the VRP API endpoints.
"""

import requests
import json
from typing import Dict, Any


# API base URL (change if running on different host/port)
BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("=" * 80)
    print("TEST 1: Health Check")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    
    print("✓ Health check passed")
    print()


def test_root_endpoint():
    """Test the root endpoint."""
    print("=" * 80)
    print("TEST 2: Root Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'online'
    
    print("✓ Root endpoint test passed")
    print()


def test_list_algorithms():
    """Test the algorithms listing endpoint."""
    print("=" * 80)
    print("TEST 3: List Algorithms")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/algorithms")
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    print(f"\nAvailable Algorithms:")
    for algo in data['algorithms']:
        print(f"  • {algo['name']}: {algo['full_name']}")
    
    assert response.status_code == 200
    assert len(data['algorithms']) >= 2
    
    print("\n✓ Algorithm listing test passed")
    print()


def test_solve_with_greedy():
    """Test solving VRP with Greedy algorithm."""
    print("=" * 80)
    print("TEST 4: Solve with Greedy Algorithm")
    print("=" * 80)
    
    payload = {
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
    }
    
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    print(f"\nResponse:")
    print(f"  Algorithm: {data['algorithm_used']}")
    print(f"  Total Distance: {data['total_distance']} {data['distance_unit']}")
    print(f"  Status: {data['status']}")
    print()
    
    print("Routes:")
    for route in data['routes']:
        if route['orders']:
            print(f"  {route['vehicle_id']}: {' -> '.join(route['orders'])}")
            print(f"    Distance: {route['total_distance']} {data['distance_unit']}")
    
    print()
    print("Statistics:")
    for key, value in data['statistics'].items():
        print(f"  {key}: {value}")
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['total_distance'] > 0
    assert len(data['routes']) == 2
    
    print("\n✓ Greedy algorithm test passed")
    print()


def test_solve_with_sa():
    """Test solving VRP with Simulated Annealing."""
    print("=" * 80)
    print("TEST 5: Solve with Simulated Annealing")
    print("=" * 80)
    
    payload = {
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
            }
        ],
        "algorithm": "simulated_annealing",
        "distance_unit": "km",
        "sa_params": {
            "initial_temp": 1000.0,
            "cooling_rate": 0.995,
            "max_iterations": 2000
        }
    }
    
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    print(f"\nResponse:")
    print(f"  Algorithm: {data['algorithm_used']}")
    print(f"  Total Distance: {data['total_distance']} {data['distance_unit']}")
    print(f"  Status: {data['status']}")
    print()
    
    print("Routes:")
    for route in data['routes']:
        if route['orders']:
            print(f"  {route['vehicle_id']}: {' -> '.join(route['orders'])}")
            print(f"    Distance: {route['total_distance']} {data['distance_unit']}")
    
    print()
    print("Optimization Statistics:")
    stats = data['statistics']
    print(f"  Iterations: {stats['iterations_completed']}")
    print(f"  Acceptance Rate: {stats['acceptance_rate']:.1%}")
    print(f"  Initial Cost: {stats['initial_cost']} {data['distance_unit']}")
    print(f"  Final Cost: {stats['final_cost']} {data['distance_unit']}")
    print(f"  Improvement: {stats['improvement']} {data['distance_unit']} "
          f"({stats['improvement_percentage']:.1f}%)")
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['total_distance'] > 0
    assert len(data['routes']) == 2
    assert stats['improvement_percentage'] >= 0
    
    print("\n✓ Simulated Annealing test passed")
    print()


def test_compare_algorithms():
    """Test comparing both algorithms on the same problem."""
    print("=" * 80)
    print("TEST 6: Algorithm Comparison")
    print("=" * 80)
    
    # Same problem for both algorithms
    base_payload = {
        "vehicles": [
            {"id": "VEH001", "current_lat": 40.7128, "current_lon": -74.0060},
            {"id": "VEH002", "current_lat": 40.7580, "current_lon": -73.9855}
        ],
        "orders": [
            {"id": "ORD001", "pickup_lat": 40.7128, "pickup_lon": -74.0060,
             "dropoff_lat": 40.7589, "dropoff_lon": -73.9851},
            {"id": "ORD002", "pickup_lat": 40.7580, "pickup_lon": -73.9855,
             "dropoff_lat": 40.7614, "dropoff_lon": -73.9776},
            {"id": "ORD003", "pickup_lat": 40.7831, "pickup_lon": -73.9712,
             "dropoff_lat": 40.7489, "dropoff_lon": -73.9680},
            {"id": "ORD004", "pickup_lat": 40.7061, "pickup_lon": -73.9969,
             "dropoff_lat": 40.7306, "dropoff_lon": -73.9866},
            {"id": "ORD005", "pickup_lat": 40.7549, "pickup_lon": -73.9840,
             "dropoff_lat": 40.7829, "dropoff_lon": -73.9654}
        ],
        "distance_unit": "km"
    }
    
    # Test with Greedy
    print("Solving with Greedy...")
    greedy_payload = {**base_payload, "algorithm": "greedy"}
    greedy_response = requests.post(f"{BASE_URL}/solve", json=greedy_payload)
    greedy_data = greedy_response.json()
    greedy_cost = greedy_data['total_distance']
    
    # Test with SA
    print("Solving with Simulated Annealing...")
    sa_payload = {
        **base_payload,
        "algorithm": "simulated_annealing",
        "sa_params": {"max_iterations": 2000}
    }
    sa_response = requests.post(f"{BASE_URL}/solve", json=sa_payload)
    sa_data = sa_response.json()
    sa_cost = sa_data['total_distance']
    
    # Compare results
    print()
    print("Comparison Results:")
    print("-" * 80)
    print(f"{'Algorithm':<30} {'Total Distance':<20} {'Status':<10}")
    print("-" * 80)
    print(f"{'Greedy Nearest Neighbor':<30} {greedy_cost:<20.2f} "
          f"{greedy_data['status']:<10}")
    print(f"{'Simulated Annealing':<30} {sa_cost:<20.2f} "
          f"{sa_data['status']:<10}")
    print("-" * 80)
    
    improvement = greedy_cost - sa_cost
    improvement_pct = (improvement / greedy_cost * 100) if greedy_cost > 0 else 0
    
    print()
    if improvement > 0:
        print(f"✓ SA improved by {improvement:.2f} km ({improvement_pct:.1f}%)")
    elif improvement == 0:
        print(f"= Both algorithms found the same solution")
    else:
        print(f"⚠ Greedy performed better by {-improvement:.2f} km")
    
    print("\n✓ Algorithm comparison test passed")
    print()


def test_error_handling():
    """Test API error handling."""
    print("=" * 80)
    print("TEST 7: Error Handling")
    print("=" * 80)
    
    # Test 1: Empty vehicles
    print("Test 7.1: Empty vehicles list")
    payload = {
        "vehicles": [],
        "orders": [
            {"id": "ORD001", "pickup_lat": 40.7, "pickup_lon": -74.0,
             "dropoff_lat": 40.8, "dropoff_lon": -73.9}
        ]
    }
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    print(f"  Status Code: {response.status_code}")
    assert response.status_code == 422  # Validation error
    print("  ✓ Empty vehicles validation works")
    print()
    
    # Test 2: Invalid coordinates
    print("Test 7.2: Invalid coordinates")
    payload = {
        "vehicles": [{"id": "VEH001", "current_lat": 100, "current_lon": -74.0}],
        "orders": [
            {"id": "ORD001", "pickup_lat": 40.7, "pickup_lon": -74.0,
             "dropoff_lat": 40.8, "dropoff_lon": -73.9}
        ]
    }
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    print(f"  Status Code: {response.status_code}")
    assert response.status_code == 422  # Validation error
    print("  ✓ Invalid coordinates validation works")
    print()
    
    # Test 3: Invalid algorithm
    print("Test 7.3: Invalid algorithm name")
    payload = {
        "vehicles": [{"id": "VEH001", "current_lat": 40.7, "current_lon": -74.0}],
        "orders": [
            {"id": "ORD001", "pickup_lat": 40.7, "pickup_lon": -74.0,
             "dropoff_lat": 40.8, "dropoff_lon": -73.9}
        ],
        "algorithm": "invalid_algo"
    }
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    print(f"  Status Code: {response.status_code}")
    assert response.status_code == 422  # Validation error
    print("  ✓ Invalid algorithm validation works")
    print()
    
    print("✓ All error handling tests passed")
    print()


def run_all_tests():
    """Run all API tests."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "VRP API TEST SUITE" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    try:
        test_health_check()
        test_root_endpoint()
        test_list_algorithms()
        test_solve_with_greedy()
        test_solve_with_sa()
        test_compare_algorithms()
        test_error_handling()
        
        print("=" * 80)
        print("ALL API TESTS PASSED ✓")
        print("=" * 80)
        print("\nThe API is working correctly!")
        print("All endpoints validated:")
        print("  ✓ Health check")
        print("  ✓ Algorithm listing")
        print("  ✓ Greedy solver")
        print("  ✓ Simulated Annealing solver")
        print("  ✓ Algorithm comparison")
        print("  ✓ Error handling")
        print()
        
    except requests.exceptions.ConnectionError:
        print("\n")
        print("=" * 80)
        print("CONNECTION ERROR ✗")
        print("=" * 80)
        print("Could not connect to the API server.")
        print()
        print("Please make sure the server is running:")
        print("  cd api")
        print("  python main.py")
        print()
        print("Or:")
        print("  uvicorn api.main:app --reload")
        print()
    
    except AssertionError as e:
        print("\n")
        print("=" * 80)
        print("TEST FAILED ✗")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        raise
    
    except Exception as e:
        print("\n")
        print("=" * 80)
        print("TEST ERROR ✗")
        print("=" * 80)
        print(f"Unexpected error: {e}")
        print()
        raise


if __name__ == "__main__":
    run_all_tests()
