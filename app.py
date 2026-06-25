import json
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATA_FILE = 'data.json'

# Data load/save functions
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"price": "100", "upi": "your@upi"}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        data['price'] = request.form.get('price', data['price'])
        data['upi'] = request.form.get('upi', data['upi'])
        save_data(data)
    
    # HTML Panel
    return render_template_string('''
        <h2>BABA Control Panel</h2>
        <form method="POST">
            Price: <input type="text" name="price" value="{{ data.price }}"><br><br>
            UPI: <input type="text" name="upi" value="{{ data.upi }}"><br><br>
            <button type="submit">Save Changes</button>
        </form>
        <hr>
        <p>Current Price: {{ data.price }}</p>
        <p>Current UPI: {{ data.upi }}</p>
    ''', data=data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
