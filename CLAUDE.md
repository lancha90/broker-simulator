# IBKR Broker Simulator - Claude Code Context

## Project Overview

This is a Python-based broker simulation application built for testing autonomous trading bots. The application simulates stock and cryptocurrency trading with a complete backend API.

## Architecture

The project follows **Hexagonal Architecture** (Ports and Adapters) pattern:

```
src/
├── application/          # Business logic layer
│   ├── services/        # Application services
│   └── ports/           # Interfaces for external dependencies
├── domain/              # Core business domain
│   ├── entities/        # Domain models
│   └── repositories/    # Repository interfaces
└── infrastructure/      # External concerns
    ├── adapters/        # Implementations of ports
    ├── config/          # Configuration
    └── middleware/      # Cross-cutting concerns
```

## Technology Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Cache**: In-memory (with interface for future Redis integration)
- **Price Data**: Yahoo Finance API (primary), AlphaVantage (fallback)
- **Authentication**: API Key-based

## Key Components

### Domain Entities
- `User`: User management with API key authentication
- `Balance`: Cash balance tracking
- `StockBalance`: Stock holdings per user
- `Trade`: Trading history
- `StockPrice`: Price data with caching

### Services
- `PriceService`: Price fetching with 3-minute cache
- `BalanceService`: Cash balance management
- `TradeService`: Buy/sell execution with validation
- `PortfolioService`: Portfolio viewing

### External Adapters
- `CompositePriceProvider`: Fallback chain for price data
- `MemoryCache`: Local caching with TTL support
- `SupabaseRepositories`: Database persistence

## API Endpoints

All endpoints require `Authorization: Bearer <api_key>` header except health check.

- `GET /health` - Health check with server info
- `GET /api/v1/balance` - Get user cash balance
- `GET /api/v1/price/{ticker}` - Get current stock price
- `GET /api/v1/portfolio` - Get user stock holdings
- `POST /api/v1/trade` - Execute buy/sell orders

## Database Schema

Tables: `ibkr_users`, `ibkr_balances`, `ibkr_stock_balances`, `ibkr_trades`
- All tables use UUID primary keys
- Foreign key relationships to ibkr_users table
- Automatic timestamp management

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Server runs on http://localhost:8000
# API docs available at /docs
```

## Environment Variables

Required:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key

Optional:
- `ALPHAVANTAGE_API_KEY`: For price data fallback
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Testing

Use the sample user created in database setup:
- Email: `test@example.com`
- API Key: `test-api-key-123`

## Price Data Sources

1. **Yahoo Finance** (Primary): `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}`
2. **AlphaVantage** (Fallback): Requires API key

Price validation for trades:
- Buy orders: price >= market price
- Sell orders: price <= market price

## Cache Implementation

- Memory-based with 3-minute TTL for price data
- Designed for easy Redis migration
- Automatic cleanup of expired entries

## Error Handling

- Comprehensive validation for all trade operations
- Proper HTTP status codes
- Detailed error messages for API consumers

## Security

- API key authentication for all protected endpoints
- Input validation and sanitization
- No sensitive data in logs or responses