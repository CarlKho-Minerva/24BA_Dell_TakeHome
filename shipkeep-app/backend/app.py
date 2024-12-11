from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # Using SQLite, file-based
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Silence a warning
db = SQLAlchemy(app)

# Secret Key (for session management)
app.secret_key = os.environ.get(
    "SECRET_KEY", "supersecretkey123!@#"
)  # Hardcoded secret key for development only


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


# --- Helper Functions ---
def is_strong_password(password):
    """Checks if the password meets complexity requirements."""
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[_@$!%*#?&]", password):
        return False
    return True


# --- API Routes ---
@app.route("/api/signup", methods=["POST"])
def signup():
    """Handles user registration."""
    data = request.get_json()

    # Basic Input Validation (you can add more)
    if (
        not data
        or "username" not in data
        or "email" not in data
        or "password" not in data
    ):
        return jsonify({"message": "Bad Request: Missing required fields"}), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]

    # Validate username
    if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", username):
        return (
            jsonify(
                {
                    "message": "Invalid username format. Use 3-20 alphanumeric characters, underscores, or hyphens."
                }
            ),
            400,
        )

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400

    # Check password strength
    if not is_strong_password(password):
        return (
            jsonify(
                {
                    "message": "Password is too weak. It must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one number, and one special character."
                }
            ),
            400,
        )

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409  # 409 Conflict

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already exists"}), 409  # 409 Conflict

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create new user
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201  # 201 Created
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"message": "Registration failed", "error": str(e)}),
            500,
        )  # 500 Internal Server Error


@app.route("/api/login", methods=["POST"])
def login():
    """Handles user login."""
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Bad Request: Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        # User authenticated, create a session
        session["logged_in"] = True
        session["user_id"] = user.id  # Store user ID in the session (optional)
        return jsonify({"message": "Login successful"}), 200
    else:
        return (
            jsonify({"message": "Invalid username or password"}),
            401,
        )  # 401 Unauthorized


# Create the database tables
with app.app_context():
    db.create_all()
