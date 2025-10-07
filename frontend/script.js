// ====================
// Configuration
// ====================

const API_BASE_URL = 'http://localhost:8000';

// Predefined sample data for demonstration
const SAMPLE_DATA = {
    vehicles: [
        {
            id: "VEH001",
            current_lat: 37.7749,
            current_lon: -122.4194
        },
        {
            id: "VEH002",
            current_lat: 37.7849,
            current_lon: -122.4094
        }
    ],
    orders: [
        {
            id: "ORD001",
            pickup_lat: 37.7849,
            pickup_lon: -122.4094,
            dropoff_lat: 37.7949,
            dropoff_lon: -122.3994
        },
        {
            id: "ORD002",
            pickup_lat: 37.7649,
            pickup_lon: -122.4294,
            dropoff_lat: 37.7749,
            dropoff_lon: -122.4194
        },
        {
            id: "ORD003",
            pickup_lat: 37.7949,
            pickup_lon: -122.3994,
            dropoff_lat: 37.8049,
            dropoff_lon: -122.3894
        },
        {
            id: "ORD004",
            pickup_lat: 37.7549,
            pickup_lon: -122.4394,
            dropoff_lat: 37.7649,
            dropoff_lon: -122.4294
        },
        {
            id: "ORD005",
            pickup_lat: 37.8049,
            pickup_lon: -122.3894,
            dropoff_lat: 37.7749,
            dropoff_lon: -122.4094
        }
    ]
};

// Route colors for visualization
const ROUTE_COLORS = [
    '#3388ff',  // Blue
    '#ff6b6b',  // Red
    '#51cf66',  // Green
    '#ffd93d',  // Yellow
    '#a78bfa',  // Purple
    '#fb923c',  // Orange
    '#06b6d4',  // Cyan
    '#ec4899'   // Pink
];

// ====================
// Global State
// ====================

let map = null;
let markers = [];
let polylines = [];
let currentSolution = null;

// ====================
// Map Initialization
// ====================

/**
 * Initialize the Leaflet map
 */
function initMap() {
    console.log('Initializing map...');
    
    // Create map centered on San Francisco
    map = L.map('map').setView([37.7749, -122.4194], 13);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    console.log('Map initialized successfully');
    updateStatus('Map loaded. Ready to solve routes.', 'success');
}

// ====================
// UI Helper Functions
// ====================

/**
 * Update the status bar
 */
function updateStatus(message, type = 'info') {
    const statusBar = document.getElementById('statusBar');
    statusBar.textContent = message;
    statusBar.className = 'status-bar';
    
    if (type === 'success') {
        statusBar.classList.add('success');
    } else if (type === 'error') {
        statusBar.classList.add('error');
    } else if (type === 'processing') {
        statusBar.classList.add('processing');
    }
    
    console.log(`[${type.toUpperCase()}] ${message}`);
}

/**
 * Show/hide loading overlay
 */
function setLoading(isLoading) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = isLoading ? 'flex' : 'none';
    
    const solveBtn = document.getElementById('solveBtn');
    solveBtn.disabled = isLoading;
}

/**
 * Show/hide SA parameters based on algorithm selection
 */
function toggleSAParams() {
    const algorithm = document.getElementById('algorithm').value;
    const saParams = document.getElementById('saParams');
    saParams.style.display = algorithm === 'simulated_annealing' ? 'block' : 'none';
}

// ====================
// Map Visualization
// ====================

/**
 * Clear all markers and polylines from the map
 */
function clearMap() {
    console.log('Clearing map...');
    
    // Remove all markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Remove all polylines
    polylines.forEach(polyline => map.removeLayer(polyline));
    polylines = [];
    
    // Hide results panel
    document.getElementById('resultsPanel').style.display = 'none';
    
    updateStatus('Map cleared. Ready to solve routes.', 'info');
    console.log('Map cleared successfully');
}

/**
 * Create a custom icon for markers
 */
function createIcon(type, color = null) {
    const icons = {
        vehicle: '📍',
        pickup: '📦',
        dropoff: '🏁'
    };
    
    return L.divIcon({
        html: `<div style="font-size: 24px;">${icons[type]}</div>`,
        className: 'custom-marker',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
    });
}

/**
 * Add a marker to the map
 */
function addMarker(lat, lon, type, title, popupContent) {
    console.log(`Adding ${type} marker at [${lat}, ${lon}]: ${title}`);
    
    const marker = L.marker([lat, lon], {
        icon: createIcon(type)
    }).addTo(map);
    
    marker.bindPopup(`
        <div class="popup-title">${title}</div>
        <div class="popup-coords">
            Lat: ${lat.toFixed(6)}<br>
            Lon: ${lon.toFixed(6)}
        </div>
        ${popupContent ? `<div style="margin-top: 8px;">${popupContent}</div>` : ''}
    `);
    
    markers.push(marker);
    return marker;
}

/**
 * Add a polyline (route) to the map
 */
function addPolyline(coordinates, color, label) {
    console.log(`Adding polyline with ${coordinates.length} points: ${label}`);
    console.log('Coordinates:', coordinates);
    
    const polyline = L.polyline(coordinates, {
        color: color,
        weight: 4,
        opacity: 0.7,
        smoothFactor: 1
    }).addTo(map);
    
    polyline.bindPopup(`<div class="popup-title">${label}</div>`);
    
    polylines.push(polyline);
    return polyline;
}

/**
 * Visualize the solution on the map
 */
function visualizeSolution(solution) {
    console.log('Visualizing solution:', solution);
    
    clearMap();
    
    if (!solution || !solution.routes) {
        console.error('Invalid solution data');
        updateStatus('Error: Invalid solution data', 'error');
        return;
    }
    
    const allCoordinates = [];
    
    // Process each route
    solution.routes.forEach((route, routeIndex) => {
        const color = ROUTE_COLORS[routeIndex % ROUTE_COLORS.length];
        console.log(`Processing Route ${routeIndex + 1} for vehicle ${route.vehicle_id}`);
        
        // Find vehicle data
        const vehicle = SAMPLE_DATA.vehicles.find(v => v.id === route.vehicle_id);
        if (!vehicle) {
            console.error(`Vehicle ${route.vehicle_id} not found`);
            return;
        }
        
        // Add vehicle marker
        const vehicleCoords = [vehicle.current_lat, vehicle.current_lon];
        addMarker(
            vehicle.current_lat,
            vehicle.current_lon,
            'vehicle',
            `Vehicle ${route.vehicle_id}`,
            `Starting location<br>${route.orders.length} orders assigned`
        );
        allCoordinates.push(vehicleCoords);
        
        // Build route coordinates
        const routeCoordinates = [vehicleCoords];
        
        // Process each order in the route
        route.orders.forEach((orderId, orderIndex) => {
            const order = SAMPLE_DATA.orders.find(o => o.id === orderId);
            if (!order) {
                console.error(`Order ${orderId} not found`);
                return;
            }
            
            console.log(`  Order ${orderIndex + 1}/${route.orders.length}: ${orderId}`);
            
            // Add pickup marker
            const pickupCoords = [order.pickup_lat, order.pickup_lon];
            addMarker(
                order.pickup_lat,
                order.pickup_lon,
                'pickup',
                `Pickup ${orderId}`,
                `Order ${orderIndex + 1} of ${route.orders.length}<br>Route ${routeIndex + 1}`
            );
            routeCoordinates.push(pickupCoords);
            allCoordinates.push(pickupCoords);
            
            // Add dropoff marker
            const dropoffCoords = [order.dropoff_lat, order.dropoff_lon];
            addMarker(
                order.dropoff_lat,
                order.dropoff_lon,
                'dropoff',
                `Dropoff ${orderId}`,
                `Order ${orderIndex + 1} of ${route.orders.length}<br>Route ${routeIndex + 1}`
            );
            routeCoordinates.push(dropoffCoords);
            allCoordinates.push(dropoffCoords);
        });
        
        // Draw the route polyline
        if (routeCoordinates.length > 1) {
            addPolyline(
                routeCoordinates,
                color,
                `Route ${routeIndex + 1} - ${route.vehicle_id}<br>Distance: ${route.total_distance.toFixed(2)} ${solution.distance_unit}`
            );
        }
    });
    
    // Fit map to show all markers
    if (allCoordinates.length > 0) {
        console.log(`Fitting map to ${allCoordinates.length} coordinates`);
        const bounds = L.latLngBounds(allCoordinates);
        map.fitBounds(bounds, { padding: [50, 50] });
    }
    
    console.log('Visualization complete');
}

/**
 * Display the solution results in the results panel
 */
function displayResults(solution) {
    console.log('Displaying results:', solution);
    
    const resultsPanel = document.getElementById('resultsPanel');
    const resultsContent = document.getElementById('resultsContent');
    
    if (!solution) {
        resultsPanel.style.display = 'none';
        return;
    }
    
    let html = `
        <div class="result-item">
            <strong>Algorithm:</strong> ${solution.algorithm_used}
        </div>
        <div class="result-item">
            <strong>Total Distance:</strong> ${solution.total_distance.toFixed(2)} ${solution.distance_unit}
        </div>
        <div class="result-item">
            <strong>Routes:</strong> ${solution.routes.length}
        </div>
    `;
    
    // Add statistics if available
    if (solution.statistics) {
        const stats = solution.statistics;
        
        if (stats.improvement_percentage !== undefined) {
            html += `
                <div class="result-item">
                    <strong>Improvement:</strong> ${stats.improvement_percentage.toFixed(1)}%
                </div>
            `;
        }
        
        if (stats.iterations_completed !== undefined) {
            html += `
                <div class="result-item">
                    <strong>Iterations:</strong> ${stats.iterations_completed.toLocaleString()}
                </div>
            `;
        }
        
        if (stats.acceptance_rate !== undefined) {
            html += `
                <div class="result-item">
                    <strong>Acceptance Rate:</strong> ${(stats.acceptance_rate * 100).toFixed(1)}%
                </div>
            `;
        }
    }
    
    // Add route details
    html += '<h3 style="margin-top: 15px; margin-bottom: 10px;">Route Details:</h3>';
    
    solution.routes.forEach((route, index) => {
        const color = ROUTE_COLORS[index % ROUTE_COLORS.length];
        html += `
            <div class="route-detail">
                <div class="route-header" style="color: ${color};">
                    Route ${index + 1} - ${route.vehicle_id}
                </div>
                <div><strong>Distance:</strong> ${route.total_distance.toFixed(2)} ${solution.distance_unit}</div>
                <div><strong>Orders:</strong> ${route.orders.length}</div>
                <div class="route-orders">
                    ${route.orders.join(' → ')}
                </div>
            </div>
        `;
    });
    
    resultsContent.innerHTML = html;
    resultsPanel.style.display = 'block';
}

// ====================
// API Communication
// ====================

/**
 * Solve the VRP by calling the backend API
 */
async function solveVRP() {
    console.log('Starting VRP solve process...');
    
    try {
        setLoading(true);
        updateStatus('Solving routes...', 'processing');
        
        // Gather form data
        const algorithm = document.getElementById('algorithm').value;
        const distanceUnit = document.getElementById('distanceUnit').value;
        
        console.log('Selected algorithm:', algorithm);
        console.log('Distance unit:', distanceUnit);
        
        // Build request payload
        const requestData = {
            vehicles: SAMPLE_DATA.vehicles,
            orders: SAMPLE_DATA.orders,
            algorithm: algorithm,
            distance_unit: distanceUnit
        };
        
        // Add SA parameters if using SA
        if (algorithm === 'simulated_annealing') {
            requestData.sa_params = {
                initial_temp: parseFloat(document.getElementById('initialTemp').value),
                cooling_rate: parseFloat(document.getElementById('coolingRate').value),
                max_iterations: parseInt(document.getElementById('maxIterations').value)
            };
            console.log('SA parameters:', requestData.sa_params);
        }
        
        console.log('Sending request to API:', requestData);
        
        // Call the API
        const response = await fetch(`${API_BASE_URL}/solve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('API error:', errorData);
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        // Parse response
        const solution = await response.json();
        console.log('Solution received:', solution);
        
        if (solution.status !== 'success') {
            throw new Error('Solution status is not success');
        }
        
        // Store and visualize solution
        currentSolution = solution;
        visualizeSolution(solution);
        displayResults(solution);
        
        updateStatus(
            `Routes optimized! Total distance: ${solution.total_distance.toFixed(2)} ${solution.distance_unit}`,
            'success'
        );
        
    } catch (error) {
        console.error('Error solving VRP:', error);
        updateStatus(`Error: ${error.message}`, 'error');
        
        // Show detailed error in console
        console.error('Full error details:', error);
        
    } finally {
        setLoading(false);
    }
}

/**
 * Check API health
 */
async function checkAPIHealth() {
    console.log('Checking API health...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const health = await response.json();
        console.log('API health check:', health);
        
        if (health.status === 'healthy') {
            updateStatus('Connected to API. Ready to solve routes.', 'success');
            return true;
        } else {
            updateStatus('API is not healthy', 'error');
            return false;
        }
        
    } catch (error) {
        console.error('API health check failed:', error);
        updateStatus('Cannot connect to API. Please ensure the backend is running on port 8000.', 'error');
        return false;
    }
}

// ====================
// Event Listeners
// ====================

/**
 * Initialize event listeners
 */
function initEventListeners() {
    console.log('Initializing event listeners...');
    
    // Solve button
    document.getElementById('solveBtn').addEventListener('click', () => {
        console.log('Solve button clicked');
        solveVRP();
    });
    
    // Clear button
    document.getElementById('clearBtn').addEventListener('click', () => {
        console.log('Clear button clicked');
        clearMap();
    });
    
    // Algorithm selection change
    document.getElementById('algorithm').addEventListener('change', () => {
        console.log('Algorithm changed');
        toggleSAParams();
    });
    
    console.log('Event listeners initialized');
}

// ====================
// Initialization
// ====================

/**
 * Initialize the application
 */
async function init() {
    console.log('=== VRP Visualizer Initializing ===');
    console.log('API Base URL:', API_BASE_URL);
    console.log('Sample Data:', SAMPLE_DATA);
    
    // Initialize map
    initMap();
    
    // Initialize event listeners
    initEventListeners();
    
    // Set initial UI state
    toggleSAParams();
    
    // Check API health
    await checkAPIHealth();
    
    console.log('=== Initialization Complete ===');
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
