from flask import Flask, request, render_template
import os
from werkzeug.security import generate_password_hash  # For basic security demo

app = Flask(__name__, template_folder='templates')

# Environment-based configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')  # Change in production!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Basic validation
    if not username or not password:
        return "Username and password required", 400
        
    # SECURITY WARNING: This is just for demo - never store passwords like this in production!
    hashed_pw = generate_password_hash(password)  # Demo of hashing (not fully secure alone)
    
    # Write to temporary file (Render has ephemeral storage)
    with open('credentials.txt', 'a') as f:
        f.write(f'Username: {username}, Hashed PW: {hashed_pw}\n')
    
    return 'Login received! (Demo only - not production-ready)'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
