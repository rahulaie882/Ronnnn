import json
import os

# Ye file tumhare data ko store karegi
DB_FILE = 'settings.json'

def load_settings():
    # Agar file nahi bani hai, toh default values set kar do
    if not os.path.exists(DB_FILE):
        return {
            "price_desi": 69, "price_child": 99, 
            "price_mom": 149, "price_rape": 199,
            "upi": "Q691189350@ybl"
        }
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_settings(data):
    # Jab tum Panel (app.py) se Save dabaoge, ye file update ho jayegi
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)
      
