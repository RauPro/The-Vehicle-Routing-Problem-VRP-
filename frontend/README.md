# VRP Frontend Visualization

A beautiful, interactive web interface for visualizing Vehicle Routing Problem solutions using Leaflet.js maps.

## 🚀 Features

- **Interactive Map Visualization**: View routes, vehicles, and orders on an interactive Leaflet.js map
- **Real-time Route Optimization**: Connect to the FastAPI backend to solve routing problems
- **Algorithm Selection**: Choose between Greedy and Simulated Annealing algorithms
- **Customizable Parameters**: Fine-tune Simulated Annealing parameters
- **Beautiful UI**: Modern, responsive design with gradient backgrounds and smooth animations
- **Detailed Results**: View comprehensive statistics and route details
- **Color-coded Routes**: Each vehicle route displayed in a different color
- **Custom Markers**: Distinct icons for vehicles (📍), pickups (📦), and dropoffs (🏁)

## 📁 Files

- **index.html**: Main HTML structure with semantic markup
- **styles.css**: Modern CSS with gradients, animations, and responsive design
- **script.js**: JavaScript logic for map interaction and API communication
- **README.md**: This file

## 🛠️ Setup

### Prerequisites

1. **Backend API Running**: Ensure the FastAPI backend is running on `http://localhost:8000`
   ```bash
   cd ..
   uvicorn api.main:app --reload
   ```

2. **Modern Web Browser**: Chrome, Firefox, Safari, or Edge (latest version)

### Option 1: Simple HTTP Server (Recommended)

```bash
# Using Python 3
python3 -m http.server 8080

# Then open browser to:
# http://localhost:8080
```

### Option 2: Live Server (VS Code Extension)

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Direct File Opening

Simply open `index.html` in your web browser (double-click the file)

**Note**: Some features may require a proper HTTP server due to CORS policies.

## 🎯 Usage

### Basic Workflow

1. **Open the Application**
   - Launch the frontend in your browser
   - The map will center on San Francisco by default

2. **Configure Settings**
   - **Algorithm**: Choose between Simulated Annealing (best quality) or Greedy (fastest)
   - **Distance Unit**: Select km, miles, or meters
   - **SA Parameters** (if using SA): Adjust temperature, cooling rate, and iterations

3. **Solve Routes**
   - Click the "🚀 Solve Routes" button
   - Wait for optimization (typically 1-10 seconds)
   - Routes will appear on the map with colored lines

4. **Explore Results**
   - Click markers to see details
   - View statistics in the results panel
   - Compare different algorithm settings

5. **Clear and Retry**
   - Click "🗑️ Clear Map" to reset
   - Try different algorithms or parameters

### Understanding the Map

**Markers:**
- 📍 **Vehicle Start**: Where each vehicle begins its route
- 📦 **Pickup**: Order pickup locations
- 🏁 **Dropoff**: Order delivery locations

**Routes:**
- Colored polylines connecting all stops for each vehicle
- Click on a line to see route details
- Different colors for different vehicles

**Popups:**
- Click any marker or route line to see details
- Shows coordinates, order sequence, and distances

## 🔧 Customization

### Change Sample Data

Edit `script.js` to modify the `SAMPLE_DATA` object:

```javascript
const SAMPLE_DATA = {
    vehicles: [
        {
            id: "VEH001",
            current_lat: 37.7749,
            current_lon: -122.4194
        }
    ],
    orders: [
        {
            id: "ORD001",
            pickup_lat: 37.7849,
            pickup_lon: -122.4094,
            dropoff_lat: 37.7949,
            dropoff_lon: -122.3994
        }
    ]
};
```

### Change Map Center

In `script.js`, modify the `initMap()` function:

```javascript
// Change from San Francisco to New York
map = L.map('map').setView([40.7128, -74.0060], 13);
```

### Customize Colors

Edit the `ROUTE_COLORS` array in `script.js`:

```javascript
const ROUTE_COLORS = [
    '#3388ff',  // Blue
    '#ff6b6b',  // Red
    // Add more colors...
];
```

### Change API URL

If your backend is on a different host/port, update `script.js`:

```javascript
const API_BASE_URL = 'http://your-server:8000';
```

## 🐛 Debugging

### Browser Developer Tools (F12)

#### Console Tab
- Check for JavaScript errors
- View detailed logs of all operations
- Look for API request/response data

Example console output:
```
=== VRP Visualizer Initializing ===
API Base URL: http://localhost:8000
Initializing map...
Map initialized successfully
Checking API health...
API health check: {status: 'healthy', message: '...', version: '1.0.0'}
```

#### Network Tab
- Monitor API requests to `/solve` endpoint
- Check request payload and response data
- Verify status codes (should be 200)

Common issues:
- **404 Not Found**: Backend not running
- **CORS errors**: Need to enable CORS on backend (already configured)
- **500 Internal Server Error**: Check backend logs

### Common Issues

#### Map is Blank
- **Check coordinates**: Ensure lat/lon are in correct format
- **Verify Leaflet loaded**: Check browser console for errors
- **Internet connection**: Leaflet tiles load from OpenStreetMap

#### Cannot Connect to API
```
Error: Cannot connect to API. Please ensure the backend is running on port 8000.
```

**Solutions:**
1. Start the backend: `uvicorn api.main:app --reload`
2. Verify backend health: `curl http://localhost:8000/health`
3. Check firewall settings
4. Ensure port 8000 is not in use

#### No Routes Displayed
- **Check sample data**: Verify vehicles and orders are defined
- **API response**: Check Network tab for `/solve` response
- **Coordinates format**: Must be [latitude, longitude]

#### Algorithm Not Working
- **SA parameters**: Ensure values are within valid ranges
- **Backend errors**: Check terminal running uvicorn for errors
- **Request validation**: Backend validates all inputs

## 📊 Sample Data

The frontend includes 5 sample orders and 2 vehicles in the San Francisco area:

**Vehicles:**
- VEH001: Downtown SF (37.7749°N, 122.4194°W)
- VEH002: Mission District (37.7849°N, 122.4094°W)

**Orders:**
- 5 orders spread across San Francisco
- Each with pickup and dropoff locations
- Realistic spacing for testing

## 🎨 UI Components

### Control Panel
- Algorithm selection dropdown
- Distance unit selector
- SA parameter inputs (collapsible)
- Action buttons (Solve, Clear)
- Results display
- Map legend
- Status bar

### Map View
- Full interactive Leaflet map
- Zoom controls
- Pan/drag navigation
- Marker clustering (for many orders)
- Route polylines
- Popup tooltips

## 🚦 Status Indicators

The status bar shows different states:

- **Ready** (Blue): Initial state, ready to solve
- **Processing** (Yellow): Solving routes...
- **Success** (Green): Routes optimized successfully
- **Error** (Red): Something went wrong

## 📱 Responsive Design

The interface adapts to different screen sizes:

- **Desktop** (>1024px): Side-by-side layout
- **Tablet** (768-1024px): Stacked layout with full-width map
- **Mobile** (<768px): Optimized touch interactions

## 🔗 Integration with Backend

### API Endpoints Used

1. **GET /health**
   - Check if backend is running
   - Called on initialization

2. **POST /solve**
   - Main route optimization endpoint
   - Sends vehicles, orders, and parameters
   - Returns optimized routes and statistics

### Request Format

```json
{
  "vehicles": [...],
  "orders": [...],
  "algorithm": "simulated_annealing",
  "distance_unit": "km",
  "sa_params": {
    "initial_temp": 1000,
    "cooling_rate": 0.995,
    "max_iterations": 10000
  }
}
```

### Response Format

```json
{
  "status": "success",
  "algorithm_used": "Simulated Annealing",
  "total_distance": 25.47,
  "distance_unit": "km",
  "routes": [
    {
      "vehicle_id": "VEH001",
      "orders": ["ORD001", "ORD002"],
      "total_distance": 12.34
    }
  ],
  "statistics": {
    "iterations_completed": 10000,
    "improvement_percentage": 23.5
  }
}
```

## 🎓 Learning Resources

### Leaflet.js Documentation
- [Leaflet Quick Start](https://leafletjs.com/examples/quick-start/)
- [Leaflet API Reference](https://leafletjs.com/reference.html)

### JavaScript Fetch API
- [MDN Fetch Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

### CSS Grid & Flexbox
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

## 🤝 Contributing

To add features:

1. **Edit HTML** (`index.html`): Add new UI elements
2. **Style CSS** (`styles.css`): Add visual styling
3. **Logic JS** (`script.js`): Implement functionality

Example - Add a new button:

```html
<!-- index.html -->
<button id="exportBtn" class="btn btn-secondary">
    📥 Export Results
</button>
```

```javascript
// script.js
document.getElementById('exportBtn').addEventListener('click', () => {
    console.log('Export clicked');
    // Your export logic here
});
```

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

- **Leaflet.js**: Interactive map library
- **OpenStreetMap**: Map tile provider
- **FastAPI**: Backend framework
- **Font**: Segoe UI system font

---

**Need Help?** Check the browser console (F12) for detailed logs and error messages.
