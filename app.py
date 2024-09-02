from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hameed:hameed%4028@localhost/login_credentials'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the tables within application context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return jsonify({"message": "Login Successful!","redirect_url": "https://console.dialogflow.com/api-client/demo/embedded/1b190f1a-2aad-4376-b4ea-4e1aa46b0db0"})
    else:
        return jsonify({"message": "Login Failed. Please check your username and password."})

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists. Please choose a different one."})

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user instance
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User Registered Successfully!","redirect_url": "http://127.0.0.1:5000/"})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
