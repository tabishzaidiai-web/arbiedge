# ArbiEdge

**AI-Powered Deal Validator for Amazon Online Arbitrage**

ArbiEdge scans Amazon Best Seller lists, cross-references prices across Walmart, Target, and other retailers, calculates real-time profit margins and ROI, and delivers AI-scored deal recommendations.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14 (App Router), React 18, Tailwind CSS, TypeScript |
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2 |
| Database | PostgreSQL 16 |
| Caching | Redis 7 |
| Auth | Clerk (OAuth + JWT) |
| Payments | Stripe |
| Deployment | Vercel (frontend) + Docker (backend) |

## Project Structure

```
arbiedge/
├── frontend/                 # Next.js 14 frontend
│   ├── src/app/
│   │   ├── page.tsx          # Landing page with pricing
│   │   ├── layout.tsx        # Root layout
│   │   ├── globals.css       # Tailwind styles
│   │   ├── dashboard/        # Dashboard with KPIs
│   │   ├── deals/            # Deal feed with filtering
│   │   ├── calculator/       # ROI/profit calculator
│   │   ├── sign-in/          # Authentication
│   │   └── sign-up/          # Registration
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── package.json
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── core/             # Config, database, redis, security
│   │   ├── api/              # Route handlers
│   │   │   ├── auth.py       # Registration, login, JWT
│   │   │   ├── deals.py      # Deal CRUD, filtering, scoring
│   │   │   ├── products.py   # Product catalog, search
│   │   │   ├── prices.py     # Cross-reference pricing
│   │   │   ├── profit.py     # FBA fee calculator
│   │   │   ├── dashboard.py  # KPI endpoints
│   │   │   ├── reports.py    # Daily digest reports
│   │   │   ├── user_settings.py  # Preferences
│   │   │   └── scan.py       # Scan job management
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic (deal scorer)
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── package.json              # Root workspace scripts
```

## Quick Start (Local Development)

### Prerequisites
- Node.js 20+
- Python 3.12+
- Docker & Docker Compose

### 1. Clone and configure
```bash
git clone https://github.com/tabishzaidiai-web/arbiedge.git
cd arbiedge
cp .env.example .env
# Edit .env with your API keys (Clerk, Stripe, Amazon)
```

### 2. Start with Docker (recommended)
```bash
docker compose up -d
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### 3. Or start manually

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## One-Click Vercel Deployment

### Frontend (Vercel)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the `arbiedge` repository
3. Set **Root Directory** to `frontend`
4. Set **Framework Preset** to `Next.js`
5. Add environment variables:
   - `NEXT_PUBLIC_API_URL` = your backend URL
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` = your Clerk key
   - `NEXT_PUBLIC_CLERK_SIGN_IN_URL` = `/sign-in`
   - `NEXT_PUBLIC_CLERK_SIGN_UP_URL` = `/sign-up`
6. Click **Deploy**

### Backend (Railway / Render / AWS)

The backend can be deployed to any Docker-compatible platform:

**Railway:**
```bash
# Install Railway CLI
railway login
railway init
railway up --service backend
```

**Render:**
1. Create a new Web Service
2. Connect your GitHub repo
3. Set Root Directory to `backend`
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, get JWT |
| GET | `/api/v1/auth/me` | Current user profile |
| GET | `/api/v1/deals` | List deals (filtered, paginated) |
| GET | `/api/v1/deals/{id}` | Get deal details |
| POST | `/api/v1/deals/{id}/save` | Save a deal |
| POST | `/api/v1/deals/{id}/purchase` | Mark as purchased |
| POST | `/api/v1/deals/batch-score` | Score multiple ASINs |
| GET | `/api/v1/products` | List products |
| GET | `/api/v1/products/search` | Search products |
| GET | `/api/v1/prices/cross-reference/{asin}` | Cross-platform prices |
| GET | `/api/v1/prices/snapshot/{asin}` | Price history |
| POST | `/api/v1/profit/calculate` | Calculate ROI & fees |
| GET | `/api/v1/dashboard/kpis` | Dashboard metrics |
| GET | `/api/v1/reports/daily` | Daily deal report |
| GET/POST | `/api/v1/user/preferences` | User preferences |
| POST | `/api/v1/scan/trigger` | Trigger deal scan |

## Pricing Tiers

- **Starter** ($49/mo) - 50 deals/day, basic scoring, email digest
- **Pro** ($99/mo) - Unlimited deals, advanced AI, real-time feed, API access
- **Enterprise** ($249/mo) - Multi-user, white-label, custom integrations

## License

Proprietary. All rights reserved.
