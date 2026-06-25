import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Railway dynamic port provide karta hai, wahi use karna zaroori hai
port = int(os.environ.get("PORT", 5000))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Simple logic to test
    return "<h1>Server is running successfully!</h1>"

if __name__ == '__main__':
    # Railway ke liye 0.0.0.0 aur host port zaroori hai
    app.run(host='0.0.0.0', port=port)
    
