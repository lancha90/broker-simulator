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
- **Database**: PostgreSQL (asyncpg) / Supabase (legacy support)
- **Migrations**: Alembic
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
- `PostgresRepositories`: Direct PostgreSQL persistence (asyncpg) - **Recommended**
  - `PostgresBalanceRepository`
  - `PostgresUserRepository`
  - `PostgresStockBalanceRepository`
  - `PostgresTradeRepository`
- `SupabaseRepositories`: Database persistence via Supabase client - **Legacy**
  - `SupabaseBalanceRepository`
  - `SupabaseUserRepository`
  - `SupabaseStockBalanceRepository`
  - `SupabaseTradeRepository`

## API Endpoints

All endpoints require `Authorization: Bearer <api_key>` header except health check.

- `GET /health` - Health check with server info
- `GET /api/v1/balance` - Get user cash balance
- `GET /api/v1/price/{ticker}` - Get current stock price
- `GET /api/v1/portfolio` - Get user stock holdings
- `POST /api/v1/trade` - Execute buy/sell orders

## Database Schema

### Tables

**ibkr_users**
- `id` (String, PK): UUID primary key
- `email` (String, Unique): User email address
- `api_key` (String, Unique): API authentication key
- `created_at` (Timestamp): Creation timestamp
- `updated_at` (Timestamp): Last update timestamp
- **Indexes**: Unique on `api_key`, Unique on `email`

**ibkr_balances**
- `id` (String, PK): UUID primary key
- `user_id` (String): Foreign key to ibkr_users
- `cash_balance` (Numeric 15,2): Cash balance amount
- `created_at` (Timestamp): Creation timestamp
- `updated_at` (Timestamp): Last update timestamp
- **Indexes**: Index on `user_id`

**ibkr_stock_balances**
- `id` (String, PK): UUID primary key
- `user_id` (String, FK): Foreign key to ibkr_users (CASCADE DELETE)
- `ticker` (String): Stock ticker symbol
- `quantity` (Numeric 15,4): Number of shares
- `average_price` (Numeric 15,2): Average purchase price
- `current_price` (Numeric 15,2): Current market price
- `created_at` (Timestamp): Creation timestamp
- `updated_at` (Timestamp): Last update timestamp
- **Indexes**: Index on `user_id`, Unique on `(user_id, ticker)`

**ibkr_trades**
- `id` (String, PK): UUID primary key
- `user_id` (String, FK): Foreign key to ibkr_users (CASCADE DELETE)
- `ticker` (String): Stock ticker symbol
- `trade_type` (String): "buy" or "sell"
- `quantity` (Numeric 15,4): Number of shares traded
- `price` (Numeric 15,2): Trade execution price
- `total_amount` (Numeric 15,2): Total transaction amount
- `created_at` (Timestamp): Trade timestamp
- **Indexes**: Index on `user_id`, Index on `created_at`

### Database Migrations (Alembic)

The project uses Alembic for schema versioning and migrations.

**Configuration:**
- `alembic.ini`: Alembic configuration file
- `alembic/env.py`: Environment configuration (reads `DATABASE_URL` from settings)
- `alembic/versions/`: Migration files

**Migration Files:**
1. `55c37baaa218_create_ibkr_balances_table.py` - Creates ibkr_balances table
2. `33a24868dd4a_create_ibkr_users_table.py` - Creates ibkr_users table with unique constraints
3. `f6c063e31254_create_ibkr_stock_balances_table.py` - Creates ibkr_stock_balances with FK to users
4. `fe94ecebcec0_create_ibkr_trades_table.py` - Creates ibkr_trades with FK to users

**Migration Order:**
balances → users → stock_balances → trades

### Database Connection

**PostgreSQL (Recommended):**
- Connection pool using `asyncpg`
- Pool configuration: min_size=2, max_size=10, timeout=60s
- Connection string: `postgresql://user:password@host:port/database`
- Configuration: `src/infrastructure/config/postgres_database.py`

**Supabase (Legacy):**
- Supabase Python client
- Configuration: `src/infrastructure/config/database.py`

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Database migrations
alembic upgrade head              # Apply all pending migrations
alembic downgrade -1              # Rollback one migration
alembic history                   # View migration history
alembic revision -m "description" # Create new migration
alembic current                   # Show current migration version

# Run development server
python main.py

# Server runs on http://localhost:8000
# API docs available at /docs
```

## Environment Variables

**Database Configuration (choose one):**
- `DATABASE_URL`: PostgreSQL connection string (Recommended)
  - Format: `postgresql://user:password@host:port/database`
  - Example: `postgresql://postgres:mypass@localhost:5432/ibkr_simulator`
- `SUPABASE_URL` + `SUPABASE_KEY`: Supabase project credentials (Legacy)

**Optional:**
- `ALPHAVANTAGE_API_KEY`: For price data fallback
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `ENVIRONMENT`: Environment name (default: development)

## Testing

**Creating Test Users:**

If using **Supabase**, use the sample user from `database_setup.sql`:
- Email: `test@example.com`
- API Key: `test-api-key-123`

If using **PostgreSQL with Alembic**, create a test user manually:
```sql
INSERT INTO ibkr_users (id, email, api_key, created_at, updated_at)
VALUES (
    gen_random_uuid()::text,
    'test@example.com',
    'test-api-key-123',
    now(),
    now()
);

INSERT INTO ibkr_balances (id, user_id, cash_balance, created_at, updated_at)
VALUES (
    gen_random_uuid()::text,
    (SELECT id FROM ibkr_users WHERE email = 'test@example.com'),
    10000.00,
    now(),
    now()
);
```

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