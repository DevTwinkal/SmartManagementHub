# Smart Management Hub

A comprehensive multi-tenant subscription management system for small businesses to manage customer subscriptions, plans, and billing.

## Features

### Core Features
- **Multi-Tenant Business Accounts**: Isolated business data with secure authentication
- **Dashboard with Key Metrics**: MRR, active subscriber count, and churn rate tracking
- **Plan Management**: Create, view, update, and delete subscription plans
- **Customer Management**: Add, view, and update customer details
- **Subscription Lifecycle**: Manage subscription creation, activation, and cancellation
- **Automated Billing Simulation**: Run billing cycles to process payments and update billing dates

### Advanced Features
- **REST API**: Access dashboard metrics via secure API endpoints
- **Multi-tenant Architecture**: Complete data isolation between businesses
- **Modern UI**: Responsive design with Bootstrap 5 and Font Awesome icons

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (simple file-based database)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Authentication**: Flask-Login with password hashing
- **ORM**: SQLAlchemy

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartManagementHub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

**Note**: The SQLite database file (`smartmanagementhub.db`) will be automatically created when you first run the application.

## Database

This application uses **SQLite**, a lightweight, file-based database that requires no server setup. The database file (`smartmanagementhub.db`) will be created automatically in your project directory when you first run the application.

### Database Schema

The system uses the following core tables:

- **businesses**: Multi-tenant business accounts
- **plans**: Subscription plans created by each business
- **customers**: Customers belonging to each business
- **subscriptions**: Links customers to plans with lifecycle management
- **payments**: Records of all billing attempts

## API Endpoints

### Authentication Required
- `GET /api/v1/metrics` - Get dashboard metrics (MRR, subscribers, churn rate)

## User Stories Implementation

### Multi-Tenant Business Accounts ✅
- Business owners can sign up and log in
- Complete data isolation between businesses
- Secure authentication with password hashing

### Dashboard with Key Metrics ✅
- **Monthly Recurring Revenue (MRR)**: Calculated from active subscriptions
- **Active Subscriber Count**: Total customers with active subscriptions
- **Churn Rate**: Percentage of subscribers who canceled this month

### Plan Management (CRUD) ✅
- Create, view, update, and delete subscription plans
- Each plan has name, price, and billing interval (monthly/yearly)

### Customer Management (CRUD) ✅
- Add, view, and update customer details (name, email)
- Customer data is isolated per business

### Subscription Lifecycle Management ✅
- Assign customers to plans creating subscriptions
- Track start_date, next_billing_date, and status
- Cancel subscriptions with cancellation date recording

### Automated Billing Simulation ✅
- Manual billing script that can be run from the dashboard
- Identifies subscriptions due for billing
- Creates payment records and updates next billing dates

## Usage Guide

### Getting Started
1. Run the application: `python app.py`
2. Visit `http://localhost:5000`
3. Register a new business account
4. Create subscription plans (e.g., Basic $29/month, Premium $99/month)
5. Add customers to your business
6. Create subscriptions linking customers to plans
7. Use the dashboard to monitor metrics
8. Run billing cycles to simulate payments

### Running Billing Cycles
1. Navigate to the Dashboard
2. Click "Run Billing Cycle" button
3. The system will process all active subscriptions due for billing
4. Payment records will be created and next billing dates updated

## Security Features

- Password hashing using Werkzeug
- Multi-tenant data isolation
- Session-based authentication
- CSRF protection (via Flask-WTF)

## Development

### Project Structure
```
SmartManagementHub/
├── app.py              # Main Flask application
├── models.py           # Database models
├── routes.py           # Route handlers
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── smartmanagementhub.db  # SQLite database file (created automatically)
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── plans.html
│   ├── customers.html
│   └── subscriptions.html
└── README.md
```

### Adding New Features
1. Add new models to `models.py`
2. Create route handlers in `routes.py`
3. Register routes in `app.py`
4. Create templates in `templates/` directory

## Database Management

### Backup
To backup your data, simply copy the `smartmanagementhub.db` file.

### Reset Database
To reset the database, delete the `smartmanagementhub.db` file and restart the application.

### View Database
You can use tools like:
- **DB Browser for SQLite** (GUI tool)
- **SQLite command line**: `sqlite3 smartmanagementhub.db`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository. 