# 🚀 QUICK START GUIDE - Truth Serum Project

Hey Eshva! I've built your entire hackathon project. Here's how to run it!

## 📂 What I Built

I created a complete fraud detection system with:
- **Backend (Python)**: Smart algorithm that catches dishonest witches
- **Frontend (React)**: Beautiful dashboard with charts and maps
- **All the code you need** to win "Best Use of Claude"! 🏆

## 🎯 How to Run Your Project (Step by Step)

### STEP 1: Open VS Code

You should already have VS Code open with your project folder:
`C:\Users\Eshva\OneDrive\Desktop\truth-serum-potions`

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
   
   This might take 2-3 minutes. Be patient! ☕

4. **Start the React app**:
   ```bash
   npm start
   ```

   After a few seconds, your browser should automatically open to:
   `http://localhost:3000`

   You'll see your dashboard! 🎉

## 🎨 What You'll See

Your dashboard has 4 tabs:

1. **📊 Overview**: Summary stats and top fraudsters
2. **🎫 Tickets**: All transport tickets with validation
3. **🧙‍♀️ Witches**: Trust scores for each witch
4. **🗺️ Factory Map**: Interactive map of the potion factory

## 🐛 Troubleshooting

### "pip is not recognized"
Try: `python -m pip install -r requirements.txt`

### "npm is not recognized"
You need to install Node.js:
1. Go to https://nodejs.org/
2. Download and install the LTS version
3. Restart VS Code
4. Try again

### "Port 5000 already in use"
Another program is using that port. Either:
- Close other programs
- Or change the port in `backend/api.py` (line at the bottom: change `port=5000` to `port=5001`)

### Backend won't connect
Make sure:
1. The backend terminal is still running
2. You see "Running on http://0.0.0.0:5000"
3. Your internet is working (needs to fetch data from HackUTD API)

## 📸 Taking Screenshots for Presentation

The judges will want to see:
1. The **Overview tab** with fraud statistics
2. The **Tickets tab** showing flagged tickets
3. The **Witches tab** with trust scores
4. The **Map tab** showing the factory layout

## 🎤 Presentation Tips

### Opening (30 seconds):
"Hi! We built Truth Serum, a fraud detection system that catches dishonest witches in a potion factory. Witches were reporting incorrect amounts on their transport tickets, and we used data analysis and AI to expose them."

### Demo (2 minutes):
1. Show the Overview - point out fraud statistics
2. Click Tickets tab - show a fraudulent ticket in red
3. Explain: "Our algorithm accounts for continuous potion flow during drainage, which is why witches collect MORE than just the visible drain"
4. Click Witches tab - show trust scores
5. Click Map tab - show the factory network

### Technical Explanation (1 minute):
"We built this with:
- Python backend using time-series analysis to detect drain events
- Machine learning-style fraud detection comparing expected vs reported amounts
- React frontend with interactive visualizations
- Real-time data from the HackUTD API"

### Why It's Impressive:
"What makes this special is:
1. It's not just simple comparisons - we calculate fill rates, detect drains, and account for continuous flow
2. Dynamic trust scoring system that updates with each ticket
3. Beautiful storytelling - we made data analysis feel like catching criminals
4. Real-world applicable - same system works for logistics, supply chains, or manufacturing"

## 🔥 Advanced: If You Have Extra Time

Want to add more features? Here are some ideas:

### 1. Add Sound Effects
When you click a fraudulent ticket, play an alarm sound!

### 2. Dark Mode Toggle
Add a button to switch between light/dark themes

### 3. Export Reports
Add a button to download fraud reports as PDF

### 4. Real-time Updates
Make the dashboard refresh every 30 seconds automatically

### 5. Witch Names
Replace "Witch A" with fantasy names like "Morgana", "Eudora", etc.

Just ask me and I'll help you add any of these!

## ✅ Checklist Before Judging

- [ ] Backend is running (terminal 1 shows Flask server)
- [ ] Frontend is running (browser shows dashboard at localhost:3000)
- [ ] You can navigate between all 4 tabs
- [ ] You tested the search and filter features on Tickets tab
- [ ] You took screenshots of each tab
- [ ] You practiced your 3-minute presentation
- [ ] You know how to explain the fraud detection algorithm
- [ ] Your laptop is fully charged! 🔋

## 💡 Remember

- You built this with Claude (me!) - that's the whole point!
- The judges want to see creative use of AI, not just coding skill
- Storytelling matters: "catching dishonest witches" is more fun than "anomaly detection"
- Be confident - you have a working, impressive project!

## 🆘 Need Help?

If something breaks or you want to add features:
1. Don't panic! 
2. Ask me (Claude) for help
3. I can fix bugs or add features quickly

---

# 🎉 YOU'VE GOT THIS!

Your project is complete and ready to demo. Just follow the steps above, practice your presentation, and you'll crush it!

Good luck at HackUTD! Now go get some sleep before the presentation! 😴✨

---

Built with ❤️ by Claude (Anthropic) for Eshva's HackUTD 2025 submission
