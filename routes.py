from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from decimal import Decimal
from models import db, Business, Plan, Customer, Subscription, Payment

# Authentication Routes
def register_route():
    if request.method == 'POST':
        try:
            business_name = request.form['business_name']
            owner_email = request.form['owner_email']
            password = request.form['password']
            
            # Check if email already exists
            existing_business = Business.query.filter_by(owner_email=owner_email).first()
            if existing_business:
                flash('Email already registered')
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
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.')
            print(f"Registration error: {e}")
            return render_template('register.html')
    
    return render_template('register.html')

def login_route():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            
            business = Business.query.filter_by(owner_email=email).first()
            if business and check_password_hash(business.password_hash, password):
                login_user(business)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password')
        except Exception as e:
            flash('Login failed. Please try again.')
            print(f"Login error: {e}")
    
    return render_template('login.html')

def logout_route():
    logout_user()
    return redirect(url_for('index'))

# Dashboard Routes
def dashboard_route():
    try:
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
    except Exception as e:
        flash('Error loading dashboard. Please try again.')
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', mrr=0, active_subscribers=0, churn_rate=0)

# Plan Management Routes
def plans_route():
    try:
        plans = Plan.query.filter_by(business_id=current_user.business_id).all()
        return render_template('plans.html', plans=plans)
    except Exception as e:
        flash('Error loading plans. Please try again.')
        print(f"Plans error: {e}")
        return render_template('plans.html', plans=[])

def new_plan_route():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            db.session.rollback()
            flash('Error creating plan. Please try again.')
            print(f"New plan error: {e}")
    
    return render_template('new_plan.html')

def edit_plan_route(plan_id):
    try:
        plan = Plan.query.filter_by(plan_id=plan_id, business_id=current_user.business_id).first_or_404()
        
        if request.method == 'POST':
            try:
                plan.name = request.form['name']
                plan.price = Decimal(request.form['price'])
                plan.billing_interval = request.form['billing_interval']
                db.session.commit()
                
                flash('Plan updated successfully!')
                return redirect(url_for('plans'))
            except Exception as e:
                db.session.rollback()
                flash('Error updating plan. Please try again.')
                print(f"Edit plan error: {e}")
        
        return render_template('edit_plan.html', plan=plan)
    except Exception as e:
        flash('Plan not found.')
        return redirect(url_for('plans'))

def delete_plan_route(plan_id):
    try:
        plan = Plan.query.filter_by(plan_id=plan_id, business_id=current_user.business_id).first_or_404()
        db.session.delete(plan)
        db.session.commit()
        
        flash('Plan deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting plan. Please try again.')
        print(f"Delete plan error: {e}")
    
    return redirect(url_for('plans'))

# Customer Management Routes
def customers_route():
    try:
        customers = Customer.query.filter_by(business_id=current_user.business_id).all()
        return render_template('customers.html', customers=customers)
    except Exception as e:
        flash('Error loading customers. Please try again.')
        print(f"Customers error: {e}")
        return render_template('customers.html', customers=[])

def new_customer_route():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            db.session.rollback()
            flash('Error adding customer. Please try again.')
            print(f"New customer error: {e}")
    
    return render_template('new_customer.html')

def edit_customer_route(customer_id):
    try:
        customer = Customer.query.filter_by(customer_id=customer_id, business_id=current_user.business_id).first_or_404()
        
        if request.method == 'POST':
            try:
                customer.full_name = request.form['full_name']
                customer.email = request.form['email']
                db.session.commit()
                
                flash('Customer updated successfully!')
                return redirect(url_for('customers'))
            except Exception as e:
                db.session.rollback()
                flash('Error updating customer. Please try again.')
                print(f"Edit customer error: {e}")
        
        return render_template('edit_customer.html', customer=customer)
    except Exception as e:
        flash('Customer not found.')
        return redirect(url_for('customers'))

# Subscription Management Routes
def subscriptions_route():
    try:
        subscriptions = Subscription.query.join(Customer).filter(
            Customer.business_id == current_user.business_id
        ).all()
        return render_template('subscriptions.html', subscriptions=subscriptions)
    except Exception as e:
        flash('Error loading subscriptions. Please try again.')
        print(f"Subscriptions error: {e}")
        return render_template('subscriptions.html', subscriptions=[])

def new_subscription_route():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            db.session.rollback()
            flash('Error creating subscription. Please try again.')
            print(f"New subscription error: {e}")
    
    try:
        customers = Customer.query.filter_by(business_id=current_user.business_id).all()
        plans = Plan.query.filter_by(business_id=current_user.business_id).all()
        return render_template('new_subscription.html', customers=customers, plans=plans)
    except Exception as e:
        flash('Error loading form data. Please try again.')
        print(f"New subscription form error: {e}")
        return render_template('new_subscription.html', customers=[], plans=[])

def cancel_subscription_route(subscription_id):
    try:
        subscription = Subscription.query.join(Customer).filter(
            Subscription.subscription_id == subscription_id,
            Customer.business_id == current_user.business_id
        ).first_or_404()
        
        subscription.status = 'canceled'
        subscription.cancellation_date = date.today()
        db.session.commit()
        
        flash('Subscription canceled successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error canceling subscription. Please try again.')
        print(f"Cancel subscription error: {e}")
    
    return redirect(url_for('subscriptions'))

# API Routes
def api_metrics_route():
    try:
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
    except Exception as e:
        print(f"API metrics error: {e}")
        return jsonify({
            'mrr': 0.0,
            'active_subscribers': 0,
            'churn_rate': 0.0
        })

# Billing Routes
def run_billing_route():
    """Simulate billing cycle for all active subscriptions"""
    try:
        today = date.today()
        
        # Find all active subscriptions that need billing
        subscriptions_to_bill = Subscription.query.join(Customer).filter(
            Customer.business_id == current_user.business_id,
            Subscription.status == 'active',
            Subscription.next_billing_date <= today
        ).all()
        
        processed_count = 0
        for subscription in subscriptions_to_bill:
            try:
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
            except Exception as e:
                print(f"Error processing subscription {subscription.subscription_id}: {e}")
                continue
        
        db.session.commit()
        
        flash(f'Billing cycle completed! Processed {processed_count} subscriptions.')
    except Exception as e:
        db.session.rollback()
        flash('Error running billing cycle. Please try again.')
        print(f"Billing error: {e}")
    
    return redirect(url_for('dashboard')) 