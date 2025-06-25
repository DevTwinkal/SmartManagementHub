from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date, timedelta
from decimal import Decimal

db = SQLAlchemy()

class Business(UserMixin, db.Model):
    __tablename__ = 'businesses'
    business_id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    owner_email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):
        return str(self.business_id)

class Plan(db.Model):
    __tablename__ = 'plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.business_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    billing_interval = db.Column(db.String(20), nullable=False)  # 'monthly' or 'yearly'
    
    business = db.relationship('Business', backref='plans')

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.business_id'), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    business = db.relationship('Business', backref='customers')
    subscriptions = db.relationship('Subscription', backref='customer', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'active', 'canceled', 'past_due', 'trial'
    start_date = db.Column(db.Date, nullable=False)
    next_billing_date = db.Column(db.Date, nullable=False)
    cancellation_date = db.Column(db.Date, nullable=True)
    
    plan = db.relationship('Plan', backref='subscriptions')
    payments = db.relationship('Payment', backref='subscription', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.subscription_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # 'paid', 'failed' 