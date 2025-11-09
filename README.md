# Truth Serum: Potion Factory Fraud Detection

**HackUTD 2025 - Best Use of Claude**

A magical dashboard that detects dishonest courier witches and optimizes potion delivery routes using real-time data analysis and AI.

---

## Quick Start

**First time running this project?** Check out [QUICKSTART.md](QUICKSTART.md) for:
- Step-by-step setup instructions
- Troubleshooting tips
- Presentation guide for judges
- Pre-demo checklist

**TL;DR:**
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python api.py

# Terminal 2 - Frontend  
cd frontend
npm install
npm start
```

Then open `http://localhost:3000` in your browser!

---

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
├── README.md            # You are here!
└── QUICKSTART.md        # Detailed setup & presentation guide
```

---

## How It Works

### The Fraud Detection Algorithm

Our algorithm validates transport tickets by comparing reported amounts against actual cauldron drainage data.

#### Step 1: Calculate Per-Cauldron Fill Rates
Each cauldron has a unique fill rate, calculated from historical data:
- Analyzes minute-by-minute level changes from the API
- Identifies periods of steady increase (no drains)
- Calculates median fill rate (units per minute)
- Example rates: 0.08 - 0.22 units/min depending on cauldron

#### Step 2: Detect Daily Drain Events
For each ticket's date and cauldron:
- Finds the peak level (highest point of the day)
- Finds the valley level (lowest point after peak)
- Calculates visible drain = peak - valley
- Measures drain duration (peak time to valley time)

#### Step 3: Account for Continuous Filling (CRITICAL!)
**Key Insight**: While a witch is draining, potion KEEPS FLOWING into the cauldron!

The witch actually collects:
```
Expected Amount = Visible Drain + (Fill Rate × Drain Duration)
```

#### Step 4: Handle Multiple Tickets Per Day
When multiple witches visit the same cauldron on one day:
- Calculate total expected from the daily drain
- Divide equally among all tickets for that day
- Each witch gets their fair share

#### Step 5: Validate and Classify Tickets
Compare reported amount to expected amount:

**Thresholds (Balanced for Realism)**:
- **< 10% error** → ✅ **Valid** (honest reporting)
- **10-25% error** → 🟡 **Suspicious** (worth investigating)
- **> 25% error** → 🚨 **Fraudulent** (clear dishonesty)

### Trust Scoring System

Each witch starts with **100 trust points** and loses points for dishonest tickets:

**Penalties (Balanced)**:
- ✅ **Valid ticket** (< 10% error): No penalty
- 🟡 **Suspicious ticket** (10-25% error): **-2 points**
- 🚨 **Fraudulent ticket** (> 25% error): **-8 points**

### Why Our Algorithm Works

1. **Uses Real Data**: All fill rates calculated from actual API data, not assumed
2. **Per-Cauldron Rates**: Each cauldron analyzed individually (they fill at different speeds!)
3. **Accounts for Physics**: Continuous inflow during drainage (as required by challenge)
4. **Handles Edge Cases**: Multiple witches per day, missing drains, capacity limits
5. **Balanced Thresholds**: Realistic fraud detection that doesn't over-flag honest witches

---

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

---

## Key Implementation Details

### Data Sources
- **Historical cauldron levels**: Live from `https://hackutd2025.eog.systems/api/Data`
- **Transport tickets**: Live from `https://hackutd2025.eog.systems/api/Tickets`
- **Cauldron metadata**: Static from `background_data.json`

---

## Dashboard Features

### Overview Tab
- Summary statistics (total tickets, fraud rate)
- Pie chart visualization
- Top fraudsters preview
- Recent suspicious activity

### Tickets Tab
- Complete ticket validation table
- Search and filter functionality
- Color-coded status (green/yellow/red)
- Detailed error percentages

### Witches Tab
- Trust scores ranked (worst first)
- Accuracy percentages
- Fraud amount totals
- Bar chart comparison

### Factory Map
- Interactive Leaflet map
- Cauldron locations with purple glow effect
- Market location (central hub)
- Travel routes visualization
- Factory-themed background (no city streets!)

---

*Need help running the project? See [QUICKSTART.md](QUICKSTART.md)*
