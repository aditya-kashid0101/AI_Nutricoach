
# NutriCoach — End-to-End Local MVP

NutriCoach is a full-stack adaptive nutrition application.

## Included now

- React + TypeScript + Vite + Tailwind frontend
- FastAPI backend
- PostgreSQL database through Docker
- JWT authentication
- User profile
- Deterministic BMR/TDEE/calorie/macro engine
- Food database seeded automatically
- Food intake logging
- AI Coach recommendation endpoint
- AI fallback when no provider key is configured
- Local development configuration
- Tests for the nutrition engine

## Run

### 1. Database

```bash
cd backend
docker compose up -d
```

### 2. Backend

Python 3.12 is recommended.

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally http://localhost:5173.

### 4. AI

The application works without an AI key using a safe fallback recommendation.

To enable generated AI recommendations, edit `backend/.env`:

```env
AI_API_KEY=your-provider-key
AI_MODEL=gpt-4o-mini
AI_BASE_URL=https://api.openai.com/v1
```

Then restart FastAPI.

## Flow

Register → Login → JWT → Profile → Nutrition targets → Food logging → AI Coach recommendation.

## Important

The deterministic nutrition engine is authoritative for calculations. The AI layer provides recommendations and explanations; it does not calculate or override the nutrition targets.

This is a local MVP foundation. Production deployment should add stronger secret management, database migrations, rate limiting, observability, refresh-token/session hardening, and comprehensive automated tests.
