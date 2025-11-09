"""
🔮 FLASK API SERVER
This serves the fraud detection results to the frontend dashboard
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
from fraud_detector import FraudDetector
from data_processor import DataProcessor

app = Flask(__name__)
CORS(app)  # Allow frontend to access API

# API Configuration
BASE_URL = "https://hackutd2025.eog.systems"
CACHE_FILE = "cached_data.json"

# Global cache for data (so we don't spam the API)
cached_analysis = None

def fetch_data_from_api():
    """Fetch all required data from HackUTD API"""
    print("📡 Fetching data from HackUTD API...")
    
    try:
        # Fetch historical cauldron data
        data_response = requests.get(f"{BASE_URL}/api/Data/?start_date=0&end_date=2000000000")
        data_response.raise_for_status()
        historical_data = data_response.json()
        print(f"✅ Fetched {len(historical_data)} historical data points")
        
        # Fetch tickets
        tickets_response = requests.get(f"{BASE_URL}/api/Tickets")
        tickets_response.raise_for_status()
        tickets_data = tickets_response.json()
        tickets = tickets_data['transport_tickets']
        print(f"✅ Fetched {len(tickets)} tickets")
        
        # Fetch background data (cauldrons, witches, network)
        with open('../data/background_data.json', 'r') as f:
            background_data = json.load(f)
        print(f"✅ Loaded background data")
        
        return {
            'historical_data': historical_data,
            'tickets': tickets,
            'background': background_data
        }
    
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def run_fraud_analysis():
    """Run the complete fraud detection analysis"""
    global cached_analysis
    
    # Check if we already have cached results
    if cached_analysis is not None:
        print("📦 Using cached analysis")
        return cached_analysis
    
    print("🔮 Running fraud detection analysis...")
    
    # Fetch data
    data = fetch_data_from_api()
    if data is None:
        return None
    
    # Run fraud detection
    detector = FraudDetector(
        historical_data=data['historical_data'],
        tickets=data['tickets']
    )
    
    analysis = detector.analyze_all_tickets()
    
    # Add background data to analysis
    analysis['background'] = data['background']
    
    # Cache the results
    cached_analysis = analysis
    
    print("✅ Fraud analysis complete!")
    print(f"   Total tickets: {analysis['summary']['total_tickets']}")
    print(f"   Valid: {analysis['summary']['valid_count']}")
    print(f"   Suspicious: {analysis['summary']['suspicious_count']}")
    print(f"   Fraudulent: {analysis['summary']['fraudulent_count']}")
    
    return analysis

# API Endpoints

@app.route('/api/health', methods=['GET'])
def health():
    """Check if API is running"""
    return jsonify({'status': 'healthy', 'message': 'Truth Serum API is running! 🔮'})

@app.route('/api/analysis', methods=['GET'])
def get_full_analysis():
    """Get complete fraud detection analysis"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    return jsonify(analysis)

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get just the summary statistics"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    return jsonify(analysis['summary'])

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all validated tickets"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    return jsonify(analysis['tickets'])

@app.route('/api/flagged', methods=['GET'])
def get_flagged_tickets():
    """Get only suspicious and fraudulent tickets"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    return jsonify(analysis['flagged_tickets'])

@app.route('/api/witches', methods=['GET'])
def get_witch_scores():
    """Get witch trust scores"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    return jsonify(analysis['witch_trust_scores'])

@app.route('/api/cauldrons', methods=['GET'])
def get_cauldron_info():
    """Get cauldron information and fill rates"""
    analysis = run_fraud_analysis()
    
    if analysis is None:
        return jsonify({'error': 'Failed to fetch or analyze data'}), 500
    
    cauldrons = analysis['background']['cauldrons']
    fill_rates = analysis['cauldron_fill_rates']
    
    # Combine cauldron info with calculated fill rates
    cauldron_data = []
    for cauldron in cauldrons:
        cauldron_copy = cauldron.copy()
        cauldron_copy['fill_rate'] = fill_rates.get(cauldron['id'], 0)
        cauldron_data.append(cauldron_copy)
    
    return jsonify(cauldron_data)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Force refresh of data (clear cache)"""
    global cached_analysis
    cached_analysis = None
    print("🔄 Cache cleared, will fetch fresh data on next request")
    return jsonify({'message': 'Cache cleared successfully'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔮 TRUTH SERUM - POTION FRAUD DETECTION API")
    print("="*60)
    print("Starting Flask server...")
    print("Frontend can access this API at: http://localhost:5000")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
