# Deployment Guide

## Deploy to Render (Recommended)

### Step 1: Prepare Your Code
1. Make sure all files are committed to your GitHub repository
2. Ensure you have these files in your root directory:
   - `app.py`
   - `models.py`
   - `routes.py`
   - `requirements.txt`
   - `Procfile`
   - `init_db.py`

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `smartmanagementhub` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid if needed)

### Step 3: Environment Variables (Optional)
Add these environment variables in Render dashboard:
- `SECRET_KEY`: Your secret key for Flask sessions

### Step 4: Deploy
Click "Create Web Service" and wait for deployment to complete.

## Deploy to Railway

### Step 1: Prepare Your Code
Same as Render preparation.

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect it's a Python app and deploy

## Deploy to Heroku

### Step 1: Install Heroku CLI
```bash
# Download and install from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add PostgreSQL addon (recommended for production)
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Run database migrations
heroku run python init_db.py
```

## Troubleshooting

### Database Issues
If you see "no such table" errors:
1. Check that `init_db.py` is running during deployment
2. Verify the database file is being created
3. Check Render/Heroku logs for errors

### Common Issues

#### 1. Import Errors
- Make sure all required packages are in `requirements.txt`
- Check that file names match exactly

#### 2. Database Connection Issues
- For SQLite: Ensure the app has write permissions
- For PostgreSQL: Check connection strings

#### 3. Static Files Not Loading
- Make sure templates are in the correct directory
- Check file paths in your code

### Logs and Debugging
- **Render**: Check the "Logs" tab in your service dashboard
- **Railway**: Check the "Deployments" tab
- **Heroku**: Use `heroku logs --tail`

## Environment-Specific Notes

### Render
- Free tier has limitations on request timeouts
- Database file persists between deployments
- Auto-deploys on git push

### Railway
- Similar to Render
- Good for development and small projects
- Easy GitHub integration

### Heroku
- More robust for production
- Better for larger applications
- Requires credit card for some features

## Production Considerations

### Security
1. Change the default `SECRET_KEY`
2. Use environment variables for sensitive data
3. Enable HTTPS (automatic on most platforms)

### Database
- Consider using PostgreSQL for production
- Set up regular backups
- Monitor database size and performance

### Performance
- Enable caching where appropriate
- Monitor response times
- Consider using a CDN for static assets

## Support
If you encounter issues:
1. Check the platform's documentation
2. Review the logs for error messages
3. Ensure all dependencies are properly installed
4. Verify database initialization is working 