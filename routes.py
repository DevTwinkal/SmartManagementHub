from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from decimal import Decimal
from models import db, Business, Plan, Customer, Subscription, Payment

# Authentication Routes
def register_route():
    if request.method == 'POST':
        business_name = request.form['business_name']
        owner_email = request.form['owner_email']
        password = request.form['password']
        
        if Business.query.filter_by(owner_email=owner_email).first():
            flash('Email registered already. Please use a different email.')
            return render_template('register.html')
        
        business = Business(
            business_name=business_name,
            owner_email=owner_email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(business)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

def login_route():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        business = Business.query.filter_by(owner_email=email).first()
        if business and check_password_hash(business.password_hash, password):
            login_user(business)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

def logout_route():
    logout_user()
    return redirect(url_for('index'))

# Dashboard Routes
def dashboard_route():
    # Calculate metrics
    active_subscriptions = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id,
        Subscription.status == 'active'
    ).count()
    
    # Calculate MRR (Monthly Recurring Revenue)
    active_subs = Subscription.query.join(Customer).join(Plan).filter(
        Customer.business_id == current_user.business_id,
        Subscription.status == 'active'
    ).all()
    
    mrr = Decimal('0.0')
    for sub in active_subs:
        if sub.plan.billing_interval == 'monthly':
            mrr += sub.plan.price
        else:  # yearly
            mrr += sub.plan.price / 12
    
    # Calculate churn rate
    current_month = date.today().replace(day=1)
    canceled_this_month = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id,
        Subscription.cancellation_date >= current_month
    ).count()
    
    total_subscribers_ever = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id
    ).count()
    
    churn_rate = (canceled_this_month / total_subscribers_ever * 100) if total_subscribers_ever > 0 else 0
    
    return render_template('dashboard.html', 
                         mrr=mrr, 
                         active_subscribers=active_subscriptions,
                         churn_rate=round(churn_rate, 2))

# Plan Management Routes
def plans_route():
    plans = Plan.query.filter_by(business_id=current_user.business_id).all()
    return render_template('plans.html', plans=plans)

def new_plan_route():
    if request.method == 'POST':
        name = request.form['name']
        price = Decimal(request.form['price'])
        billing_interval = request.form['billing_interval']
        
        plan = Plan(
            business_id=current_user.business_id,
            name=name,
            price=price,
            billing_interval=billing_interval
        )
        db.session.add(plan)
        db.session.commit()
        
        flash('Plan created successfully!')
        return redirect(url_for('plans'))
    
    return render_template('new_plan.html')

def edit_plan_route(plan_id):
    plan = Plan.query.filter_by(plan_id=plan_id, business_id=current_user.business_id).first_or_404()
    
    if request.method == 'POST':
        plan.name = request.form['name']
        plan.price = Decimal(request.form['price'])
        plan.billing_interval = request.form['billing_interval']
        db.session.commit()
        
        flash('Plan updated successfully!')
        return redirect(url_for('plans'))
    
    return render_template('edit_plan.html', plan=plan)

def delete_plan_route(plan_id):
    plan = Plan.query.filter_by(plan_id=plan_id, business_id=current_user.business_id).first_or_404()
    db.session.delete(plan)
    db.session.commit()
    
    flash('Plan deleted successfully!')
    return redirect(url_for('plans'))

# Customer Management Routes
def customers_route():
    customers = Customer.query.filter_by(business_id=current_user.business_id).all()
    return render_template('customers.html', customers=customers)

def new_customer_route():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        
        customer = Customer(
            business_id=current_user.business_id,
            full_name=full_name,
            email=email
        )
        db.session.add(customer)
        db.session.commit()
        
        flash('Customer added successfully!')
        return redirect(url_for('customers'))
    
    return render_template('new_customer.html')

def edit_customer_route(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id, business_id=current_user.business_id).first_or_404()
    
    if request.method == 'POST':
        customer.full_name = request.form['full_name']
        customer.email = request.form['email']
        db.session.commit()
        
        flash('Customer updated successfully!')
        return redirect(url_for('customers'))
    
    return render_template('edit_customer.html', customer=customer)

# Subscription Management Routes
def subscriptions_route():
    subscriptions = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id
    ).all()
    return render_template('subscriptions.html', subscriptions=subscriptions)

def new_subscription_route():
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        plan_id = int(request.form['plan_id'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        
        # Verify customer and plan belong to current business
        customer = Customer.query.filter_by(customer_id=customer_id, business_id=current_user.business_id).first_or_404()
        plan = Plan.query.filter_by(plan_id=plan_id, business_id=current_user.business_id).first_or_404()
        
        # Calculate next billing date
        if plan.billing_interval == 'monthly':
            next_billing_date = start_date + timedelta(days=30)
        else:  # yearly
            next_billing_date = start_date + timedelta(days=365)
        
        subscription = Subscription(
            customer_id=customer_id,
            plan_id=plan_id,
            status='active',
            start_date=start_date,
            next_billing_date=next_billing_date
        )
        db.session.add(subscription)
        db.session.commit()
        
        flash('Subscription created successfully!')
        return redirect(url_for('subscriptions'))
    
    customers = Customer.query.filter_by(business_id=current_user.business_id).all()
    plans = Plan.query.filter_by(business_id=current_user.business_id).all()
    return render_template('new_subscription.html', customers=customers, plans=plans)

def cancel_subscription_route(subscription_id):
    subscription = Subscription.query.join(Customer).filter(
        Subscription.subscription_id == subscription_id,
        Customer.business_id == current_user.business_id
    ).first_or_404()
    
    subscription.status = 'canceled'
    subscription.cancellation_date = date.today()
    db.session.commit()
    
    flash('Subscription canceled successfully!')
    return redirect(url_for('subscriptions'))

# API Routes
def api_metrics_route():
    # Calculate metrics for API
    active_subscriptions = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id,
        Subscription.status == 'active'
    ).count()
    
    active_subs = Subscription.query.join(Customer).join(Plan).filter(
        Customer.business_id == current_user.business_id,
        Subscription.status == 'active'
    ).all()
    
    mrr = Decimal('0.0')
    for sub in active_subs:
        if sub.plan.billing_interval == 'monthly':
            mrr += sub.plan.price
        else:  # yearly
            mrr += sub.plan.price / 12
    
    current_month = date.today().replace(day=1)
    canceled_this_month = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id,
        Subscription.cancellation_date >= current_month
    ).count()
    
    total_subscribers_ever = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id
    ).count()
    
    churn_rate = (canceled_this_month / total_subscribers_ever * 100) if total_subscribers_ever > 0 else 0
    
    return jsonify({
        'mrr': float(mrr),
        'active_subscribers': active_subscriptions,
        'churn_rate': round(churn_rate, 2)
    })

# Billing Routes
def run_billing_route():
    """Simulate billing cycle for all active subscriptions"""
    today = date.today()
    
    # Find all active subscriptions that need billing
    subscriptions_to_bill = Subscription.query.join(Customer).filter(
        Customer.business_id == current_user.business_id,
        Subscription.status == 'active',
        Subscription.next_billing_date <= today
    ).all()
    
    processed_count = 0
    for subscription in subscriptions_to_bill:
        # Create payment record
        payment = Payment(
            subscription_id=subscription.subscription_id,
            amount=subscription.plan.price,
            status='paid'
        )
        db.session.add(payment)
        
        # Update next billing date
        if subscription.plan.billing_interval == 'monthly':
            subscription.next_billing_date = subscription.next_billing_date + timedelta(days=30)
        else:  # yearly
            subscription.next_billing_date = subscription.next_billing_date + timedelta(days=365)
        
        processed_count += 1
    
    db.session.commit()
    
    flash(f'Billing cycle completed! Processed {processed_count} subscriptions.')
    return redirect(url_for('dashboard')) 