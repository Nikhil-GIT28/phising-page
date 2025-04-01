from flask import Flask, request, render_template
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__, template_folder='templates')

# Safe default for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password required", 400
            
        hashed_pw = generate_password_hash(password)
        print(f"Login attempt: {username}")  # View in Render logs
        
        # Option 1: In-memory storage (recommended)
        global last_login
        last_login = {'username': username, 'hashed_pw': hashed_pw}
        
        # Option 2: Temporary file (ephemeral on Render)
        with open('/tmp/credentials.txt', 'a') as f:
            f.write(f"{username}:{hashed_pw}\n")
            
        return "Login processed successfully!"
        
    except Exception as e:
        print(f"ERROR: {str(e)}")  # Debug in logs
        return f"Server error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
