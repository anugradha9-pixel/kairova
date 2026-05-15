# API Reference — Kairova

## Base URL

```txt
http://127.0.0.1:8000
```

---

# Authentication APIs

---

## Signup

### Endpoint

```http
POST /auth/signup
```

### Request Body

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

### Success Response

```json
{
  "message": "User created successfully"
}
```

---

## Login

### Endpoint

```http
POST /auth/login
```

### Request Body

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

### Success Response

```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

### Authorization Header

```http
Authorization: Bearer your_access_token
```

---

## Refresh Token

### Endpoint

```http
POST /auth/refresh
```

### Request Body

```json
{
  "refresh_token": "jwt_refresh_token"
}
```

### Success Response

```json
{
  "access_token": "new_access_token"
}
```

---

# User APIs

---

## Get Current User

### Endpoint

```http
GET /me
```

### Headers

```http
Authorization: Bearer access_token
```

### Success Response

```json
{
  "id": "uuid",
  "email": "user@example.com"
}
```

---

## Protected Route

### Endpoint

```http
GET /protected
```

### Headers

```http
Authorization: Bearer access_token
```

### Success Response

```json
{
  "message": "Protected route accessed"
}
```

---

# Creator APIs

---

## Create Creator Analysis

### Endpoint

```http
POST /creator
```

### Headers

```http
Authorization: Bearer access_token
```

### Request Body

```json
{
  "platform": "instagram",
  "followers": 150000,
  "engagement_rate": 5.8
}
```

### Success Response

```json
{
  "estimated_price": 4200,
  "confidence_score": 88,
  "market_tier": "Premium",
  "reasoning": "This creator has strong engagement and audience quality."
}
```

---

## Get Creator Pricing

### Endpoint

```http
GET /creator/{creator_id}/pricing
```

### Example

```http
GET /creator/1/pricing
```

### Success Response

```json
{
  "creator_id": 1,
  "estimated_price": 4200,
  "confidence_score": 88,
  "market_tier": "Premium"
}
```

---

## Get All Creators

### Endpoint

```http
GET /creator/all
```

### Headers

```http
Authorization: Bearer access_token
```

### Success Response

```json
[
  {
    "id": 1,
    "platform": "instagram",
    "followers": 150000,
    "engagement_rate": 5.8,
    "estimated_price": 4200
  },
  {
    "id": 2,
    "platform": "youtube",
    "followers": 300000,
    "engagement_rate": 7.1,
    "estimated_price": 9800
  }
]
```

---

# Common Response Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# JWT Authentication Flow

```txt
User logs in
↓
Backend validates credentials
↓
Backend returns JWT tokens
↓
Frontend stores access token
↓
Frontend sends token in Authorization header
```

---

# Frontend Axios Configuration

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

# Example Frontend API Calls

---

## Login API Call

```javascript
const response = await API.post("/auth/login", {
  email,
  password,
});

localStorage.setItem(
  "access_token",
  response.data.access_token
);
```

---

## Creator Analysis API Call

```javascript
const response = await API.post("/creator", {
  platform: "instagram",
  followers: 150000,
  engagement_rate: 5.8,
});

console.log(response.data);
```

---

# Future Planned APIs

---

## Analytics APIs

```http
GET /analytics/revenue
GET /analytics/platforms
GET /analytics/trends
```

---

## Recommendation APIs

```http
POST /recommendations/brands
POST /recommendations/campaigns
```

---

## Forecasting APIs

```http
POST /forecast/pricing
POST /forecast/roi
```

---

# Environment Variables

---

## Backend

```env
DATABASE_URL=postgresql://postgres:password@localhost/kairova
SECRET_KEY=supersecretkey
ALGORITHM=HS256
```

---

## Frontend

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# Run Commands

---

## Backend

```bash
uvicorn backend.app:app --reload
```

---

## Frontend

```bash
npm run dev
```

---

# Current API Status

| Feature | Status |
|---|---|
| JWT Auth | Complete |
| Refresh Tokens | Complete |
| Protected Routes | Complete |
| Creator Pricing | Complete |
| Confidence Scoring | Complete |
| AI Reasoning | Complete |
| Dashboard Integration | In Progress |
| Analytics APIs | Planned |
| Recommendation Engine | Planned |