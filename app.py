from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__, template_folder='templates')

# Environment-based configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

# In-memory storage for the last attempt (avoids file system issues on Render)
last_attempt = {
    'username': None,
    'hashed_password': None,
    'timestamp': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        return "Username and password required", 400
        
    # Store the attempt in memory
    last_attempt['username'] = username
    last_attempt['hashed_password'] = generate_password_hash(password)
    last_attempt['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Optional: Still write to file for temporary logging (ephemeral on Render)
    with open('credentials.txt', 'a') as f:
        f.write(f"{last_attempt['timestamp']} - User: {username}, Hashed PW: {last_attempt['hashed_password']}\n")
    
    return redirect(url_for('show_last_attempt'))  # Redirect to view the attempt

@app.route('/last_attempt')
def show_last_attempt():
    if not last_attempt['username']:
        return "No login attempts yet."
    
    return f"""
    <h2>Last Login Attempt</h2>
    <p><strong>Timestamp:</strong> {last_attempt['timestamp']}</p>
    <p><strong>Username:</strong> {last_attempt['username']}</p>
    <p><strong>Hashed Password:</strong> {last_attempt['hashed_password']}</p>
    <p><em>Note: Passwords are securely hashed and not stored in plaintext.</em></p>
    <a href="/">Back to login</a>
    """

if __name__ == '__main__':
    import datetime  # For timestamp handling
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
