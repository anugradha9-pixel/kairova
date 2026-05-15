# Kairova Production Architecture Blueprint

## Overview

Kairova is a full-stack AI-powered creator pricing intelligence platform.

Core capabilities:

* JWT Authentication
* Creator Pricing Engine
* Confidence Scoring
* AI Reasoning Engine
* Dashboard Analytics
* Structured API Responses

---

# Backend Architecture (FastAPI)

## Recommended Structure

```txt
backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── cors.py
│   │   └── dependencies.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── creator.py
│   │   └── pricing.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── creator.py
│   │   └── pricing.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── creator.py
│   │       ├── dashboard.py
│   │       └── me.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── pricing_engine.py
│   │   ├── confidence_engine.py
│   │   ├── ai_reasoning_service.py
│   │   └── creator_service.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   └── helpers.py
│   │
│   └── middleware/
│       └── auth_middleware.py
│
├── requirements.txt
├── .env
└── run.py
```

---

# Backend Core Files

## app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

app = FastAPI(title="Kairova API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def home():
    return {"message": "Kairova API Running"}
```

---

## app/api/router.py

```python
from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.creator import router as creator_router
from app.api.routes.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(creator_router, prefix="/creator", tags=["Creator"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
```

---

## app/core/config.py

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
```

---

## app/core/security.py

```python
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)



def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)



def create_access_token(data: dict, expires_minutes: int = 30):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
```

---

## app/services/pricing_engine.py

```python
class PricingEngine:
    def calculate_price(
        self,
        followers,
        engagement_rate,
        platform,
    ):
        base_price = followers * 0.02

        engagement_bonus = engagement_rate * 100

        platform_multiplier = {
            "instagram": 1.0,
            "youtube": 1.4,
            "tiktok": 1.2,
        }

        multiplier = platform_multiplier.get(platform.lower(), 1)

        estimated_price = (
            base_price + engagement_bonus
        ) * multiplier

        return round(estimated_price, 2)
```

---

## app/services/confidence_engine.py

```python
class ConfidenceEngine:
    def calculate_confidence(
        self,
        engagement_rate,
        followers,
    ):
        score = 50

        if engagement_rate > 5:
            score += 25

        if followers > 100000:
            score += 15

        return min(score, 100)
```

---

## app/services/ai_reasoning_service.py

```python
class AIReasoningService:
    def generate_reasoning(
        self,
        followers,
        engagement_rate,
        platform,
    ):
        return (
            f"This creator has {followers} followers on {platform} "
            f"with an engagement rate of {engagement_rate}%. "
            f"The estimated pricing reflects strong audience value."
        )
```

---

## app/api/routes/creator.py

```python
from fastapi import APIRouter

from app.schemas.creator import CreatorRequest
from app.services.pricing_engine import PricingEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.ai_reasoning_service import AIReasoningService

router = APIRouter()

pricing_engine = PricingEngine()
confidence_engine = ConfidenceEngine()
reasoning_service = AIReasoningService()


@router.post("")
def create_creator(data: CreatorRequest):
    estimated_price = pricing_engine.calculate_price(
        data.followers,
        data.engagement_rate,
        data.platform,
    )

    confidence_score = confidence_engine.calculate_confidence(
        data.engagement_rate,
        data.followers,
    )

    reasoning = reasoning_service.generate_reasoning(
        data.followers,
        data.engagement_rate,
        data.platform,
    )

    return {
        "estimated_price": estimated_price,
        "confidence_score": confidence_score,
        "market_tier": "Premium",
        "reasoning": reasoning,
    }
```

---

# Frontend Architecture (React + Vite)

## Recommended Structure

```txt
frontend/
├── src/
│   ├── api/
│   │   ├── axios.js
│   │   ├── auth.api.js
│   │   └── creator.api.js
│   │
│   ├── auth/
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   └── authService.js
│   │
│   ├── components/
│   │   ├── cards/
│   │   │   ├── PricingCard.jsx
│   │   │   ├── ConfidenceCard.jsx
│   │   │   └── ReasoningPanel.jsx
│   │   │
│   │   ├── forms/
│   │   │   └── CreatorForm.jsx
│   │   │
│   │   └── shared/
│   │       ├── Button.jsx
│   │       └── Input.jsx
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── hooks/
│   │   └── useAuth.js
│   │
│   ├── layouts/
│   │   └── DashboardLayout.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── CreatorPage.jsx
│   │   └── LoginPage.jsx
│   │
│   ├── routes/
│   │   └── ProtectedRoute.jsx
│   │
│   ├── styles/
│   │   └── global.css
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── .env
```

---

# Frontend Core Files

## src/api/axios.js

```javascript
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default API;
```

---

## src/routes/ProtectedRoute.jsx

```javascript
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access_token");

  return token ? children : <Navigate to="/" />;
}
```

---

## src/pages/Dashboard.jsx

```javascript
import CreatorForm from "../components/forms/CreatorForm";

export default function Dashboard() {
  return (
    <div>
      <h1>Kairova Dashboard</h1>

      <CreatorForm />
    </div>
  );
}
```

---

## src/components/forms/CreatorForm.jsx

```javascript
import { useState } from "react";

import API from "../../api/axios";

export default function CreatorForm() {
  const [formData, setFormData] = useState({
    platform: "",
    followers: "",
    engagement_rate: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await API.post(
        "/creator",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="platform"
          placeholder="Platform"
          onChange={handleChange}
        />

        <input
          type="number"
          name="followers"
          placeholder="Followers"
          onChange={handleChange}
        />

        <input
          type="number"
          name="engagement_rate"
          placeholder="Engagement Rate"
          onChange={handleChange}
        />

        <button type="submit">
          Analyze Creator
        </button>
      </form>

      {result && (
        <div>
          <h3>Estimated Price</h3>
          <p>${result.estimated_price}</p>

          <h3>Confidence</h3>
          <p>{result.confidence_score}%</p>

          <h3>Market Tier</h3>
          <p>{result.market_tier}</p>

          <h3>Reasoning</h3>
          <p>{result.reasoning}</p>
        </div>
      )}
    </div>
  );
}
```

---

# Environment Variables

## backend/.env

```env
DATABASE_URL=postgresql://postgres:password@localhost/kairova
SECRET_KEY=supersecretkey
ALGORITHM=HS256
```

---

## frontend/.env

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# Run Commands

## Backend

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
npm run dev
```

---

# Current Production Readiness Checklist

## Authentication

* [x] JWT login
* [x] Refresh token system
* [x] Protected routes
* [x] Axios auth interceptor

## Backend

* [x] FastAPI structure
* [x] Service layer
* [x] Structured routing
* [x] Pricing engine
* [x] Confidence engine

## Frontend

* [x] Vite React setup
* [x] Protected dashboard
* [x] API layer
* [x] Creator form foundation

## Next Recommended Features

* [ ] Dashboard analytics charts
* [ ] Creator history table
* [ ] AI recommendation engine
* [ ] Revenue forecasting
* [ ] Stripe payments
* [ ] Docker deployment
* [ ] CI/CD pipeline
* [ ] Role-based access
* [ ] Admin dashboard
