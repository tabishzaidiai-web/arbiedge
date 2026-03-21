"""ArbiEdge FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import auth, deals, products, prices, profit, dashboard, reports, user_settings, scan

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting {settings.APP_NAME} API server...")
    yield
    # Shutdown
    print(f"Shutting down {settings.APP_NAME} API server...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Deal Validator for Amazon Online Arbitrage",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(deals.router, prefix=f"{settings.API_V1_PREFIX}/deals", tags=["Deals"])
app.include_router(products.router, prefix=f"{settings.API_V1_PREFIX}/products", tags=["Products"])
app.include_router(prices.router, prefix=f"{settings.API_V1_PREFIX}/prices", tags=["Prices"])
app.include_router(profit.router, prefix=f"{settings.API_V1_PREFIX}/profit", tags=["Profit Calculator"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(reports.router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["Reports"])
app.include_router(user_settings.router, prefix=f"{settings.API_V1_PREFIX}/user", tags=["User Settings"])
app.include_router(scan.router, prefix=f"{settings.API_V1_PREFIX}/scan", tags=["Scanner"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME, "version": "1.0.0"}
