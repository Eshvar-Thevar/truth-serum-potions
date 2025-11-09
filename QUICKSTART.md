# QUICK START GUIDE - Truth Serum Project

## What I Built

I created a complete fraud detection system with:
- **Backend (Python)**: Smart algorithm that catches dishonest witches
- **Frontend (React)**: Beautiful dashboard with charts and maps

## How to Run The Project (Step by Step)

### STEP 1: Open VS Code

### STEP 2: Start the Backend (Python Server)

1. **Open a terminal in VS Code**:
   - Click `Terminal` in the top menu
   - Click `New Terminal`
   - You'll see a terminal window at the bottom

2. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```

3. **Install Python dependencies** (only need to do this once):
   ```bash
   pip install -r requirements.txt
   ```
   
   If that doesn't work, try:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Start the server**:
   ```bash
   python api.py
   ```

   You should see:
   ```
   🔮 TRUTH SERUM - POTION FRAUD DETECTION API
   Starting Flask server...
   ```

   **LEAVE THIS TERMINAL OPEN!** The server needs to keep running.

### STEP 3: Start the Frontend (React Dashboard)

1. **Open a SECOND terminal** (keep the first one running!):
   - Click the `+` button in the terminal tab
   - Or: `Terminal` → `New Terminal`

2. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```

3. **Install Node dependencies** (only need to do this once):
   ```bash
   npm install
   ```
   
   This might take 2-3 minutes. Be patient!

4. **Start the React app**:
   ```bash
   npm start
   ```

   After a few seconds, your browser should automatically open to:
   `http://localhost:3000`

   You'll see your dashboard! 

## What You'll See

Your dashboard has 4 tabs:

1. **Overview**: Summary stats and top fraudsters
2. **Tickets**: All transport tickets with validation
3. **Witches**: Trust scores for each witch
4. **Factory Map**: Interactive map of the potion factory
