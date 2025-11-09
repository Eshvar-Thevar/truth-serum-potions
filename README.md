# Truth Serum: Potion Factory Fraud Detection

**HackUTD 2025**

A magical dashboard that detects dishonest courier witches and optimizes potion delivery routes using real-time data analysis and AI.

## What This Project Does

1. **Fraud Detection**: Analyzes cauldron drainage patterns and compares them with witch-reported tickets to catch liars
2. **Trust Scoring**: Tracks each witch's honesty over time
3. **Interactive Dashboard**: Beautiful visualization of the potion factory operations

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
- **Git**

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

---
