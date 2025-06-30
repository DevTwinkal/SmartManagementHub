from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from decimal import Decimal
import os
from dotenv import load_dotenv
from models import db, Business, Plan, Customer, Subscription, Payment
from routes import *

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartmanagementhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Business.query.get(int(user_id))

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

# Initialize database on startup
init_db()

# Basic routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_route()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_route()

@app.route('/logout')
@login_required
def logout():
    return logout_route()

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return dashboard_route()

# Plan management
@app.route('/plans')
@login_required
def plans():
    return plans_route()

@app.route('/plans/new', methods=['GET', 'POST'])
@login_required
def new_plan():
    return new_plan_route()

@app.route('/plans/<int:plan_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plan(plan_id):
    return edit_plan_route(plan_id)

@app.route('/plans/<int:plan_id>/delete')
@login_required
def delete_plan(plan_id):
    return delete_plan_route(plan_id)

# Customer management
@app.route('/customers')
@login_required
def customers():
    return customers_route()

@app.route('/customers/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    return new_customer_route()

@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    return edit_customer_route(customer_id)

# Subscription management
@app.route('/subscriptions')
@login_required
def subscriptions():
    return subscriptions_route()

@app.route('/subscriptions/new', methods=['GET', 'POST'])
@login_required
def new_subscription():
    return new_subscription_route()

@app.route('/subscriptions/<int:subscription_id>/cancel')
@login_required
def cancel_subscription(subscription_id):
    return cancel_subscription_route(subscription_id)

# API routes
@app.route('/api/v1/metrics')
@login_required
def api_metrics():
    return api_metrics_route()

# Billing
@app.route('/billing/run')
@login_required
def run_billing():
    return run_billing_route()

if __name__ == '__main__':
    app.run(debug=True) 