from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/sign_up')
def sign_up():
    return render_template('register.html')  

if __name__ == '__main__':
    app.run(debug=True)