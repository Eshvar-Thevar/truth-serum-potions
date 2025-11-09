# Truth Serum: Potion Factory Fraud Detection

**HackUTD 2025**

A magical dashboard that detects dishonest courier witches and optimizes potion delivery routes using real-time data analysis and AI.

## What This Project Does

1. **Fraud Detection**: Analyzes cauldron drainage patterns and compares them with witch-reported tickets to catch liars
2. **Trust Scoring**: Tracks each witch's honesty over time
3. **Route Optimization**: (Bonus) Finds the minimum number of witches needed to prevent cauldron overflows
4. **Interactive Dashboard**: Beautiful visualization of the potion factory operations

## Project Structure

```
truth-serum-potions/
├── backend/               # Python fraud detection engine
│   ├── fraud_detector.py  # Main logic for detecting dishonest tickets
│   ├── data_processor.py  # Calculate fill/drain rates from historical data
│   ├── api.py            # Flask API server
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # React dashboard
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.jsx       # Main app
│   │   └── ...
│   └── package.json      # Node dependencies
│
├── data/                 # Static data files
│   └── background_data.json  # Cauldrons, witches, network map
│
└── README.md            # You are here!
```

## How to Run This Project

### Prerequisites
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Git** (already have it!)

### Step 1: Start the Backend (Python API)

Open a terminal in VS Code:
```bash
cd backend
pip install -r requirements.txt
python api.py
```

The backend will start at `http://localhost:5000`

### Step 2: Start the Frontend (React Dashboard)

Open a NEW terminal in VS Code:
```bash
cd frontend
npm install
npm start
```

The dashboard will open at `http://localhost:3000`

## How It Works

### The Fraud Detection Algorithm

1. **Calculate Fill Rates**: Analyzes historical data to determine how fast each cauldron fills
2. **Detect Drain Events**: Finds sudden drops in cauldron levels (when witches collect potion)
3. **Account for Continuous Filling**: While a witch drains, potion keeps flowing in!
   - `Expected Amount = Drain Volume + (Fill Rate × Drain Duration)`
4. **Match Tickets to Drains**: Links each ticket to its corresponding drain event by date
5. **Flag Suspicious Tickets**: If reported amount doesn't match expected amount → 🚨 FRAUD!

### Trust Scoring System

Each witch starts with 100 trust points:
- ✅ **Accurate ticket**: +0 points (maintaining trust)
- 🟡 **Minor discrepancy** (±5%): -5 points
- 🔴 **Major fraud** (>10% off): -20 points

## API Endpoints

The backend provides these endpoints:

- `GET /api/analysis` - Full fraud analysis results
- `GET /api/tickets` - All tickets with validation status
- `GET /api/witches` - Witch trust scores
- `GET /api/cauldrons` - Cauldron statistics

## Technologies Used

**Backend:**
- Python 3
- Flask (API server)
- NumPy (data analysis)
- Requests (API calls)

**Frontend:**
- React
- Recharts (beautiful charts)
- Leaflet (interactive maps)
- Tailwind CSS (styling)

## What Makes This Impressive

1. **Real Data Science**: Proper time-series analysis with derivative calculations
2. **Robust Algorithm**: Handles edge cases (continuous filling, multiple drains per day)
3. **Beautiful Visualization**: Judges love seeing data come to life
4. **Storytelling**: Not just "fraud detection" — it's catching dishonest witches! 🧙‍♀️
5. **Bonus Challenge**: Route optimization to minimize witch count

## Troubleshooting

**Backend won't start?**
- Make sure you're in the `backend` folder
- Try: `pip install --upgrade pip` then reinstall requirements

**Frontend won't start?**
- Make sure you're in the `frontend` folder
- Try: `npm install` again
- Check if port 3000 is already in use

**API errors?**
- The HackUTD API might be rate-limited
- Check your internet connection

## Presentation Tips

1. **Start with the story**: "Witches are stealing potions, we caught them!"
2. **Show the dashboard first**: Live demo is most impressive
3. **Explain the algorithm**: Show you understand the math
4. **Highlight creativity**: Trust scores, witch names, magic theme
5. **Connect to real-world**: "This same system detects fraud in supply chains"

## Learning Resources

Since this is your first time coding, here are the key concepts:

- **API**: A way for programs to talk to each other
- **Frontend**: What the user sees (the website)
- **Backend**: The smart logic running behind the scenes
- **JSON**: A format for storing data (looks like JavaScript objects)
- **Endpoint**: A URL that returns data (like a vending machine button)

---
