from flask import Flask, render_template_string, request
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv('MYSQLHOST'),
        user=os.getenv('MYSQLUSER'),
        password=os.getenv('MYSQLPASSWORD'),
        database=os.getenv('MYSQLDATABASE'),
        port=os.getenv('MYSQLPORT')
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        price = request.form['price']
        upi = request.form['upi']
        cursor.execute("UPDATE setting SET value=%s WHERE key_name='price'", (price,))
        cursor.execute("UPDATE setting SET value=%s WHERE key_name='upi'", (upi,))
        db.commit()
    
    cursor.execute("SELECT * FROM setting")
    data = {row['key_name']: row['value'] for row in cursor.fetchall()}
    db.close()
    
    return render_template_string('''
        <h2>VIAXOR Python Panel</h2>
        <form method="POST">
            Price: <input type="text" name="price" value="{{ data.get('price', '') }}"><br>
            UPI: <input type="text" name="upi" value="{{ data.get('upi', '') }}"><br>
            <button type="submit">Save Changes</button>
        </form>
    ''', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
