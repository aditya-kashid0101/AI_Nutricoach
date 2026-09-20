# NutriCoach architecture

React/Vite frontend communicates with FastAPI through Axios.

FastAPI is responsible for:
- authentication and authorization
- persistence
- deterministic nutrition calculations
- food logging
- orchestration of AI recommendations

PostgreSQL stores users, profiles, foods, food intake, and recommendation history.

The nutrition engine is deterministic. The AI layer receives calculated targets and logged intake as context and generates a recommendation. When an AI key is absent or the provider is unavailable, a deterministic fallback response keeps the application usable.

Current request flow:

React → FastAPI → PostgreSQL
              ↓
       Nutrition Engine
              ↓
          AI Coach
