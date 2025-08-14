import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.infrastructure.adapters.web import (
    health_controller,
    balance_controller,
    price_controller,
    portfolio_controller,
    trade_controller
)
from src.infrastructure.config.settings import settings

load_dotenv()

app = FastAPI(
    title="IBKR Broker Simulator",
    description="A simulated broker for stocks and crypto trading",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_controller.router, tags=["Health"])
app.include_router(balance_controller.router, prefix="/api", tags=["Balance"])
app.include_router(price_controller.router, prefix="/api", tags=["Price"])
app.include_router(portfolio_controller.router, prefix="/api", tags=["Portfolio"])
app.include_router(trade_controller.router, prefix="/api", tags=["Trade"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )