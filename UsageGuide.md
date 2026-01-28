# ChronoHunt Investment App - Usage Guide

This guide provides instructions on how to run the application and manually verify the implemented features (Phase 1-3).

## Prerequisites

- **Docker** and **Docker Compose** installed.
- **Node.js** (v18+) and **npm** installed.

## 1. Starting the Application

### Backend & Infrastructure
Start the backend, database (PostgreSQL), Redis, and Celery worker:

```bash
docker-compose up -d --build
```
- **Backend API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`

### Frontend
Start the Next.js development server:

```bash
cd frontend
npm install
npm run dev
```
- **Dashboard**: `http://localhost:3000`

---

## 2. Manual Verification Steps

### A. VIX Monitoring (Defense)
1.  Open the Dashboard (`http://localhost:3000`).
2.  Locate the **Defense** column.
3.  Observe the **VIX Status** card.
    -   It should display the current VIX price (fetched live from Yahoo Finance).
    -   **Status**: Normal (Green), Caution (Yellow), or Crisis (Red) based on the price.

### B. Portfolio Tracking (Defense)
1.  In the **Defense** column, look for the **Portfolio Holdings** table.
2.  Initially, it may be empty.
3.  **Verify API**:
    -   Go to `http://localhost:8000/docs`.
    -   Use `POST /api/v1/portfolio/holdings` to add a test holding (e.g., Symbol: "AAPL", Quantity: 10, Price: 150).
    -   Refresh the Dashboard. The holding should appear in the table.

### C. Alert System (Defense)
1.  In the **Defense** column, look for the **Alert Rules** section (AlertConfig component).
2.  This UI currently displays static/mock alerts for the MVP.
3.  **Verify Backend**:
    -   The Celery worker is running in the background.
    -   It periodically checks the VIX against thresholds.
    -   To see logs: `docker-compose logs -f celery_worker`.

### D. Momentum Scanner (Offense)
1.  Locate the **Offense** column on the Dashboard.
2.  Find the **Momentum Scanner** table.
3.  Click the **"Run Scan"** button.
    -   The app will fetch 1-year historical data for a default list of tech stocks (AAPL, MSFT, NVDA, etc.).
    -   It calculates **RSI (14)** and **Momentum (20d % Change)**.
    -   The table will populate with the results, sorted by highest momentum.
    -   *Note: This typically takes 2-5 seconds depending on your connection to Yahoo Finance.*

---

## 3. Running Automated Tests

To run the full backend test suite (VIX, Portfolio, Scanner, Alerts):

```bash
docker-compose exec backend python -m pytest
```

---

## Troubleshooting

- **Backend fails to start?** Check if ports 5432 (Postgres) or 6379 (Redis) are already in use.
- **Frontend build errors?** Ensure you are in the `frontend` directory and have run `npm install`.
- **"Not enough data" in Scanner?** Occasionally Yahoo Finance APIs rate limit or return empty data. Try again in a few seconds.
