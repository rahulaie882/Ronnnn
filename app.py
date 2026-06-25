import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Dummy data jo tum database ya JSON se fetch kar sakte ho
data = {
    "total_users": "4,507",
    "active_subs": "25",
    "pending_payments": "0",
    "open_reports": "1",
    "total_revenue": "6,267",
    "license_expiry": "5 days left"
}

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #121212; color: white; font-family: sans-serif; }
            .card { background-color: #1e1e1e; border: none; border-radius: 15px; color: white; margin-bottom: 15px; padding: 15px; }
            .card-icon { font-size: 20px; }
            .value { font-size: 24px; font-weight: bold; }
        </style>
    </head>
    <body class="p-3">
        <h4 class="mb-4">Dashboard</h4>
        <div class="card">
            <div class="value">{{ data.total_users }}</div>
            <div>Total Users</div>
        </div>
        <div class="card">
            <div class="value">{{ data.active_subs }}</div>
            <div>Active Subs</div>
        </div>
        <div class="card">
            <div class="value">{{ data.pending_payments }}</div>
            <div>Pending Payments</div>
        </div>
        <div class="card">
            <div class="value">{{ data.open_reports }}</div>
            <div>Open Reports</div>
        </div>
        <div class="card">
            <div class="value">₹{{ data.total_revenue }}</div>
            <div>Total Revenue</div>
        </div>
        <div class="card text-danger">
            <div class="value">{{ data.license_expiry }}</div>
            <div>Licence Expiry</div>
        </div>
    </body>
    </html>
    ''', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
