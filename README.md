# IBKR Broker Simulator

A Python-based broker simulation application designed for testing autonomous trading bots. This application provides a complete REST API for simulating stock and cryptocurrency trading operations.

## Features

- ✅ **User Management**: API key-based authentication
- ✅ **Balance Tracking**: Cash balance management with automatic updates
- ✅ **Stock Portfolio**: Track holdings per stock with average price calculation
- ✅ **Trading Engine**: Buy/sell operations with market price validation
- ✅ **Price Data**: Real-time stock prices with caching (Yahoo Finance + AlphaVantage fallback)
- ✅ **Trade History**: Complete audit trail of all trades
- ✅ **Health Monitoring**: Server health and performance metrics

## Architecture

Built using **Hexagonal Architecture** for clean separation of concerns:
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: External integrations (database, APIs, web)

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Supabase account
- AlphaVantage API key (optional)

### 2. Database Setup

1. Create a Supabase project
2. Run the SQL script from `database_setup.sql` in your Supabase SQL editor

### 3. Environment Configuration

```bash
cp .env .env
```

Edit `.env` with your configuration:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key  # Optional
PORT=8000
HOST=0.0.0.0
```

### 4. Installation & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

## API Usage

All endpoints (except health check) require authentication via `Authorization` header:

```bash
Authorization: Bearer your-api-key
```

### Test with Sample User

Use the pre-created test user:
- **API Key**: `test-api-key-123`

### Example Requests

**Get Balance:**
```bash
curl -H "Authorization: Bearer test-api-key-123" \
     http://localhost:8000/api/v1/balance
```

**Get Stock Price:**
```bash
curl -H "Authorization: Bearer test-api-key-123" \
     http://localhost:8000/api/v1/price/AAPL
```

**Execute Trade:**
```bash
curl -X POST \
     -H "Authorization: Bearer test-api-key-123" \
     -H "Content-Type: application/json" \
     -d '{"ticker": "AAPL", "action": "buy", "quantity": 10, "price": 150.00}' \
     http://localhost:8000/api/v1/trade
```

**View Portfolio:**
```bash
curl -H "Authorization: Bearer test-api-key-123" \
     http://localhost:8000/api/v1/portfolio
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Server health check | No |
| GET | `/api/v1/balance` | Get user cash balance | Yes |
| GET | `/api/v1/price/{ticker}` | Get current stock price | Yes |
| GET | `/api/v1/portfolio` | Get user stock holdings | Yes |
| POST | `/api/v1/trade` | Execute buy/sell order | Yes |

## Trading Rules

### Buy Orders
- Price must be **≥** current market price
- Sufficient cash balance required
- Updates cash balance and stock holdings

### Sell Orders  
- Price must be **≤** current market price
- Sufficient stock quantity required
- Updates cash balance and stock holdings

### Price Validation
Prices are fetched from:
1. **Yahoo Finance** (primary)
2. **AlphaVantage** (fallback)

Prices are cached for 3 minutes to improve performance.

## Database Schema

- **users**: User accounts with API keys
- **balances**: Cash balances per user
- **stock_balances**: Stock holdings per user/ticker
- **trades**: Complete trading history

## Deployment

See [deploy.md](docs/deploy.md) for detailed deployment instructions including:
- Railway (Free tier)
- Render (Free tier)  
- Heroku

## Development

### Project Structure
```
src/
├── application/     # Business logic
├── domain/         # Core entities
└── infrastructure/ # External adapters
```

### Adding New Features
1. Define domain entities in `src/domain/entities/`
2. Create repository interfaces in `src/domain/repositories/`
3. Implement services in `src/application/services/`
4. Add infrastructure adapters as needed
5. Create web controllers in `src/infrastructure/adapters/web/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the hexagonal architecture patterns
4. Ensure all trades maintain data consistency
5. Submit a pull request

## License

MIT License - see LICENSE file for details.