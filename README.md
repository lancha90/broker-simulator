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
- PostgreSQL database (Supabase or local PostgreSQL)
- AlphaVantage API key (optional)

### 2. Database Setup

#### Option A: Using Supabase (Recommended for quick start)

1. Create a Supabase project
2. Run the SQL script from `database_setup.sql` in your Supabase SQL editor

#### Option B: Using PostgreSQL with Alembic Migrations

1. Install PostgreSQL locally or use a cloud provider
2. Create a new database
3. Configure `DATABASE_URL` in `.env` (see step 3)
4. Run migrations:
```bash
alembic upgrade head
```

### 3. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# For Supabase (Legacy support)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# For direct PostgreSQL connection (Recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/database_name

# Optional configurations
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
PORT=8000
HOST=0.0.0.0
```

### 4. Installation & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations (if using PostgreSQL)
alembic upgrade head

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

### Tables

- **ibkr_users**: User accounts with API keys (unique constraints on email and api_key)
- **ibkr_balances**: Cash balances per user
- **ibkr_stock_balances**: Stock holdings per user/ticker (unique constraint on user_id + ticker)
- **ibkr_trades**: Complete trading history with audit trail

### Migrations

The project uses **Alembic** for database migrations. All migrations are located in `alembic/versions/`.

**Available migrations:**
1. `create_ibkr_balances_table` - Cash balance tracking
2. `create_ibkr_users_table` - User accounts and authentication
3. `create_ibkr_stock_balances_table` - Stock holdings with foreign key to users
4. `create_ibkr_trades_table` - Trade history with foreign key to users

**Migration commands:**
```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Create a new migration
alembic revision -m "description"
```

## Deployment

See [deploy.md](docs/deploy.md) for detailed deployment instructions including:
- Railway (Free tier)
- Render (Free tier)  
- Heroku

## Development

### Project Structure
```
src/
├── application/           # Business logic
│   ├── services/         # Application services
│   └── ports/           # Port interfaces
├── domain/               # Core entities
│   ├── entities/        # Domain models
│   └── repositories/    # Repository interfaces
└── infrastructure/       # External adapters
    ├── adapters/
    │   ├── persistence/
    │   │   ├── postgres/    # PostgreSQL repositories (asyncpg)
    │   │   └── supabase/    # Supabase repositories (legacy)
    │   ├── pricing/         # Price data providers
    │   └── web/             # HTTP controllers
    ├── config/              # Configuration
    └── middleware/          # Cross-cutting concerns

alembic/
├── versions/            # Database migrations
└── env.py              # Alembic configuration
```

### Database Repository Implementations

The project supports two database adapters:

1. **PostgreSQL (Recommended)** - Direct connection using `asyncpg`
   - `PostgresBalanceRepository`
   - `PostgresUserRepository`
   - `PostgresStockBalanceRepository`
   - `PostgresTradeRepository`

2. **Supabase (Legacy)** - Using Supabase client
   - `SupabaseBalanceRepository`
   - `SupabaseUserRepository`
   - `SupabaseStockBalanceRepository`
   - `SupabaseTradeRepository`

### Adding New Features
1. Define domain entities in `src/domain/entities/`
2. Create repository interfaces in `src/domain/repositories/`
3. Implement repository adapters in `src/infrastructure/adapters/persistence/postgres/`
4. Create Alembic migration: `alembic revision -m "description"`
5. Implement services in `src/application/services/`
6. Create web controllers in `src/infrastructure/adapters/web/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the hexagonal architecture patterns
4. Ensure all trades maintain data consistency
5. Submit a pull request

## License

MIT License - see LICENSE file for details.