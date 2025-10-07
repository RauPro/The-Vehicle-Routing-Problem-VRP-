# 🚀 Frontend Quick Start Guide

## Step 1: Start the Backend

Open a terminal and run:

```bash
cd "/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)"
source .venv/bin/activate
uvicorn api.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Backend is ready when you see this!

---

## Step 2: Start the Frontend

**Option A: Using the Quick Start Script**

Open a **NEW** terminal and run:

```bash
cd "/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)/frontend"
bash start_frontend.sh
```

**Option B: Manual Python Server**

```bash
cd "/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)/frontend"
python3 -m http.server 8080
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

✅ Frontend is ready!

---

## Step 3: Open in Browser

Open your web browser and go to:

```
http://localhost:8080
```

You should see:
- 🎨 Beautiful gradient header "VRP Route Visualizer"
- 🗺️ Interactive map of San Francisco
- ⚙️ Control panel on the left
- 📊 Status bar showing "Connected to API. Ready to solve routes."

---

## Step 4: Solve Your First Route!

1. **Select Algorithm**: Choose "Simulated Annealing" (default)
2. **Select Distance Unit**: Choose "Kilometers" (default)
3. **Click "🚀 Solve Routes"**

Watch the magic happen:
- Loading spinner appears
- API processes the request (1-10 seconds)
- Map updates with:
  - 📍 Vehicle starting positions (2 vehicles)
  - 📦 Pickup locations (5 orders)
  - 🏁 Dropoff locations (5 orders)
  - Colored routes connecting all points

---

## Step 5: Explore the Results

### Click on Markers
- Click any marker to see details
- Popup shows coordinates and order info

### Click on Routes
- Click route lines to see distance
- Each route has a different color

### View Statistics
- Results panel shows:
  - Total distance
  - Number of routes
  - Improvement percentage
  - Iterations completed
  - Per-route details

---

## Troubleshooting

### ❌ "Cannot connect to API"

**Problem:** Backend is not running

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it:
cd "/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)"
uvicorn api.main:app --reload
```

### ❌ Map is blank

**Problem:** Internet connection or browser issue

**Solution:**
- Check internet (map tiles come from OpenStreetMap)
- Open browser console (F12) and check for errors
- Try refreshing the page (Ctrl+R)

### ❌ "Address already in use" (port 8080)

**Problem:** Another process is using port 8080

**Solution:**
```bash
# Use a different port
python3 -m http.server 8081

# Then open: http://localhost:8081
```

### ❌ Routes don't appear

**Problem:** API error or invalid data

**Solution:**
- Open browser console (F12 → Console tab)
- Check for error messages
- Look at Network tab for API response
- Verify backend logs

---

## Browser Developer Tools (F12)

### Console Tab
**What you should see:**
```
=== VRP Visualizer Initializing ===
API Base URL: http://localhost:8000
Initializing map...
Map initialized successfully
Checking API health...
[SUCCESS] Connected to API. Ready to solve routes.
```

### Network Tab
**When you click "Solve Routes":**
1. POST request to `http://localhost:8000/solve`
2. Status: 200 OK
3. Response: JSON with routes and statistics

---

## Sample Output

After solving, you should see:

**On the Map:**
- 2 colored routes (blue and red)
- 2 vehicle markers (📍)
- 10 markers total (5 pickups 📦 + 5 dropoffs 🏁)
- Polylines connecting all stops

**In Results Panel:**
```
📊 Results

Algorithm: Simulated Annealing
Total Distance: 25.47 km
Routes: 2
Improvement: 23.5%
Iterations: 10,000

Route Details:

Route 1 - VEH001
Distance: 12.34 km
Orders: 3
ORD001 → ORD002 → ORD003

Route 2 - VEH002
Distance: 13.13 km
Orders: 2
ORD004 → ORD005
```

---

## Testing Different Algorithms

### Greedy Algorithm
1. Select "Greedy Nearest Neighbor" from dropdown
2. Click "🚀 Solve Routes"
3. Results appear in ~1 second (very fast!)
4. Good baseline solution

### Simulated Annealing
1. Select "Simulated Annealing" from dropdown
2. Optionally adjust parameters:
   - Initial Temperature: 1000 (default)
   - Cooling Rate: 0.995 (default)
   - Max Iterations: 10000 (default)
3. Click "🚀 Solve Routes"
4. Takes 5-10 seconds (more thorough)
5. Usually 15-30% better than Greedy!

---

## Customizing Sample Data

Edit `frontend/script.js` around line 10:

```javascript
const SAMPLE_DATA = {
    vehicles: [
        {
            id: "VEH001",
            current_lat: 37.7749,  // Change to your city
            current_lon: -122.4194
        }
    ],
    orders: [
        {
            id: "ORD001",
            pickup_lat: 37.7849,   // Your coordinates
            pickup_lon: -122.4094,
            dropoff_lat: 37.7949,
            dropoff_lon: -122.3994
        }
    ]
};
```

**Tips:**
- Use [Google Maps](https://maps.google.com) to get coordinates
- Right-click on a location → Copy coordinates
- Format: latitude, longitude (in that order!)

---

## Changing the Map Location

Edit `frontend/script.js` around line 115:

```javascript
function initMap() {
    // Change coordinates and zoom level
    map = L.map('map').setView([YOUR_LAT, YOUR_LON], ZOOM);
    
    // Examples:
    // New York: [40.7128, -74.0060], 13
    // London: [51.5074, -0.1278], 13
    // Tokyo: [35.6762, 139.6503], 13
}
```

---

## Performance Tips

### For Many Orders (>20)
1. Increase SA iterations: 15000-20000
2. Adjust cooling rate: 0.997-0.999
3. Expect 30-60 second solve time

### For Quick Testing
1. Use Greedy algorithm
2. Reduce sample orders to 3-5
3. Results in < 1 second

### For Best Quality
1. Use Simulated Annealing
2. Set iterations: 20000+
3. Set cooling rate: 0.999
4. Be patient (may take 1-2 minutes)

---

## Next Steps

1. ✅ **You've completed Milestone 4!**
2. 🎯 Try different algorithms and compare
3. 📝 Modify sample data for your use case
4. 🎨 Customize colors and styles
5. 🚀 Add more features (see FRONTEND_MILESTONE_COMPLETE.md)

---

## Full Command Reference

### Start Backend
```bash
cd "/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)"
source .venv/bin/activate
uvicorn api.main:app --reload
```

### Start Frontend
```bash
cd frontend
python3 -m http.server 8080
```

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### Stop Backend
```
Press Ctrl+C in the backend terminal
```

### Stop Frontend
```
Press Ctrl+C in the frontend terminal
```

---

## 🎉 Success!

You now have a fully functional VRP visualization system!

- ✅ Backend API running on port 8000
- ✅ Frontend UI running on port 8080
- ✅ Interactive map with route visualization
- ✅ Two algorithms to choose from
- ✅ Beautiful, responsive design

**Enjoy optimizing your routes! 🚚📦🗺️**
