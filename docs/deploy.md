# IBKR Broker Simulator - Deployment Guide

This document provides instructions for deploying the IBKR Broker Simulator application.

## Prerequisites

- Python 3.8+
- Supabase account
- AlphaVantage API key (optional, for stock price fallback)

## Database Setup

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Note your project URL and API key

### 2. Set up Database Schema

1. In your Supabase dashboard, go to the SQL Editor
2. Run the SQL script from `database_setup.sql`

## Environment Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env .env
```

2. Fill in your environment variables:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key  # Optional
PORT=8000
HOST=0.0.0.0
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Deployment Options

### Option 1: Railway (Free Tier Available)

Railway offers a free tier perfect for testing and small applications.

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Add environment variables:
```bash
railway variables set SUPABASE_URL=your_supabase_project_url
railway variables set SUPABASE_KEY=your_supabase_anon_key
railway variables set ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
railway variables set PORT=8000
railway variables set HOST=0.0.0.0
```

5. Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python main.py"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

6. Deploy:
```bash
railway up
```

### Option 2: Render (Free Tier Available)

Render provides free hosting for web services.

1. Fork/push your code to GitHub
2. Go to [Render](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. Add environment variables in the Render dashboard
7. Deploy

### Option 3: Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: python main.py
```

3. Create `runtime.txt`:
```
python-3.11.0
```

4. Deploy:
```bash
heroku create your-app-name
heroku config:set SUPABASE_URL=your_supabase_project_url
heroku config:set SUPABASE_KEY=your_supabase_anon_key
heroku config:set ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
git push heroku main
```

## API Documentation

Once deployed, visit `https://your-domain/docs` to access the interactive API documentation powered by FastAPI's automatic OpenAPI generation.

## Testing the Deployment

1. Health check:
```bash
curl https://your-domain/health
```

2. Get balance (requires authentication):
```bash
curl -H "Authorization: Bearer test-api-key-123" https://your-domain/api/v1/balance
```

## Security Considerations

- Use strong API keys in production
- Enable CORS only for trusted domains
- Consider rate limiting for production deployments
- Use environment variables for all sensitive configuration

## Monitoring

The application includes basic health checks and server information endpoints. For production deployments, consider adding:

- Application performance monitoring (APM)
- Log aggregation
- Uptime monitoring
- Error tracking

## Scaling Considerations

For high-traffic deployments:

- Replace memory cache with Redis
- Use connection pooling for database
- Implement rate limiting
- Add load balancing
- Consider microservices architecture