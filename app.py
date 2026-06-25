import json
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {"price": "100", "upi": "your@upi"}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        data['price'] = request.form['price']
        data['upi'] = request.form['upi']
        save_data(data)
    return render_template_string('''
        <h2>Simple Panel</h2>
        <form method="POST">
            Price: <input type="text" name="price" value="{{ data.price }}"><br>
            UPI: <input type="text" name="upi" value="{{ data.upi }}"><br>
            <button type="submit">Save</button>
        </form>
    ''', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
