-- Create users table
CREATE TABLE IF NOT EXISTS ibkr_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create balances table
CREATE TABLE IF NOT EXISTS ibkr_balances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES ibkr_users(id) ON DELETE CASCADE,
    cash_balance DECIMAL(15,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Create stock_balances table
CREATE TABLE IF NOT EXISTS ibkr_stock_balances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES ibkr_users(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    quantity DECIMAL(15,8) NOT NULL DEFAULT 0,
    average_price DECIMAL(15,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, ticker)
);

-- Create trades table
CREATE TABLE IF NOT EXISTS ibkr_trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES ibkr_users(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    trade_type VARCHAR(4) NOT NULL CHECK (trade_type IN ('buy', 'sell')),
    quantity DECIMAL(15,8) NOT NULL,
    price DECIMAL(15,2) NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_ibkr_users_api_key ON ibkr_users(api_key);
CREATE INDEX IF NOT EXISTS idx_ibkr_balances_user_id ON ibkr_balances(user_id);
CREATE INDEX IF NOT EXISTS idx_ibkr_stock_balances_user_id ON ibkr_stock_balances(user_id);
CREATE INDEX IF NOT EXISTS idx_ibkr_stock_balances_user_ticker ON ibkr_stock_balances(user_id, ticker);
CREATE INDEX IF NOT EXISTS idx_ibkr_trades_user_id ON ibkr_trades(user_id);
CREATE INDEX IF NOT EXISTS idx_ibkr_trades_created_at ON ibkr_trades(created_at);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at column
CREATE TRIGGER update_ibkr_users_updated_at BEFORE UPDATE ON ibkr_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ibkr_balances_updated_at BEFORE UPDATE ON ibkr_balances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ibkr_stock_balances_updated_at BEFORE UPDATE ON ibkr_stock_balances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample user for testing (optional)
INSERT INTO ibkr_users (email, api_key) VALUES 
('test@example.com', 'test-api-key-123')
ON CONFLICT (email) DO NOTHING;