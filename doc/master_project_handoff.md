MAKERMINT — FINAL AUTHORITATIVE PROJECT HANDOFF
(Paste Into New Chat To Continue Development)
Project Identity

Project Name: MakerMint

Tagline:
Price Smarter. Profit Better.

Mission:

Help Etsy sellers, handmade creators, makers, crafters, small brands, and product businesses determine profitable product pricing using AI-powered pricing intelligence.

Core question:

What should I charge and why?

Current Status

MakerMint is built on top of the former Kairova backend.

The backend foundation is already working.

DO NOT redesign or rebuild existing infrastructure.

Assume everything below is working correctly.

VERIFIED WORKING COMPONENTS
Backend
FastAPI
SQLAlchemy 2.x
PostgreSQL
Alembic
Redis
JWT Authentication
Docker
Docker Compose
Pydantic v2
Authentication

Working.

Implemented:

Signup
Login
Logout
Refresh Tokens
Refresh Rotation
Session Tracking
OAuth2 Swagger Login
Current User Endpoint
Role Support

Endpoints:

POST /api/v1/auth/signup

POST /api/v1/auth/login

POST /api/v1/auth/refresh

POST /api/v1/auth/logout

GET /api/v1/auth/me
JWT

Working.

Access Token:

{
  "sub": "user_id",
  "sid": "session_id",
  "jti": "token_id",
  "type": "access"
}

Refresh Token:

{
  "sub": "user_id",
  "sid": "session_id",
  "jti": "token_id",
  "type": "refresh"
}
Redis

Working.

Used for:

session:{sid} -> refresh_jti

Purpose:

refresh rotation
logout invalidation
replay protection
PostgreSQL

Working.

Verified tables:

users
creators
alembic_version
Alembic

Working.

Commands:

docker compose exec backend alembic revision --autogenerate -m "message"

docker compose exec backend alembic upgrade head

Do not revisit Alembic debugging.

Docker

Working.

Containers:

backend
postgres
redis

Do not revisit Docker debugging.

CURRENT PROJECT ARCHITECTURE

Must remain unchanged.

Routes
 ↓
Service
 ↓
Repository
 ↓
Database

Rules:

No business logic in routes
No DB access in routes
No Redis access in routes
No Redis access in repositories
No service bypassing
No duplicate Base
No duplicate Engine
EXISTING PROJECT STRUCTURE
backend/

app/

├── api/
│   └── v1/
│       ├── auth_routes.py
│       ├── user_routes.py
│       └── creator_routes.py
│
├── auth/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   ├── jwt.py
│   ├── dependencies.py
│   └── utils.py
│
├── config/
│   └── settings.py
│
├── core/
│   ├── ai/
│   │   └── ai_engine/
│   │       ├── confidence.py
│   │       ├── explain.py
│   │       └── labeling.py
│   │
│   └── core_engine/
│       ├── pricing.py
│       └── scorecard.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   ├── models.py
│   └── base_repository.py
│
├── modules/
│   └── creator/
│       ├── domain.py
│       ├── models.py
│       ├── schemas.py
│       ├── repository.py
│       └── service.py
│
├── schemas/
│   └── response.py
│
└── main.py
EXISTING CREATOR MODULE

Working.

CRUD endpoints verified.

POST   /api/v1/creators

GET    /api/v1/creators

GET    /api/v1/creators/{id}

PUT    /api/v1/creators/{id}

DELETE /api/v1/creators/{id}
CREATOR OWNERSHIP

Already implemented at database level.

Relationship:

users.id
    ↓
creators.user_id

Foreign key exists.

Cascade delete exists.

LEGACY CREATOR PRICING ENGINE

Still operational.

Keep it intact.

Features:

CPM calculations
Platform multipliers
Niche multipliers
Engagement weighting
Confidence scoring
Market labels
Creator scorecards

Do NOT remove.

Do NOT refactor now.

IMPORTANT PRODUCT DIRECTION

Ignore old Kairova roadmap.

Ignore Campaign Module.

Ignore Marketplace.

Ignore Influencer SaaS roadmap.

MakerMint is now:

Pricing Intelligence For Physical Products

Target Users:

Etsy sellers
Handmade creators
Product makers
Small brands
Crafters
DIY businesses
CURRENT MVP OBJECTIVE

Build:

Product Pricing Intelligence Platform

Nothing else.

REQUIRED NEW DOMAIN MODELS
Creator

Represents business owner.

Existing creator model may evolve.

Target fields:

id
user_id
business_name
currency
hourly_rate
target_margin
created_at
updated_at

Use additive migrations.

Do not break existing creator endpoints.

Product Model
id
creator_id

name
description

created_at
updated_at

Relationship:

Creator
   ↓
Product

One creator → many products

ProductCost Model
id
product_id

material_cost

labor_hours
labor_rate

packaging_cost
shipping_cost

platform_fee_percent

created_at
updated_at

Relationship:

Product
   ↓
ProductCost

One product → one cost profile

NEW MODULES TO BUILD

Create:

modules/

product/
│
├── models.py
├── schemas.py
├── repository.py
└── service.py


product_cost/
│
├── models.py
├── schemas.py
├── repository.py
└── service.py


pricing/
│
├── schemas.py
└── service.py
SCHEMA REQUIREMENTS

Every module must include:

Create Schema

Example:

ProductCreate
Update Schema

Example:

ProductUpdate
Response Schema

Example:

ProductResponse

Use Pydantic v2.

REPOSITORY REQUIREMENTS

Create:

ProductRepository

ProductCostRepository

Both should inherit from:

BaseRepository

No business logic inside repositories.

Repositories only:

CRUD
Querying
Filtering
SERVICE REQUIREMENTS

Create:

ProductService

ProductCostService

PricingService

All business logic belongs here.

PRICING ENGINE MVP

Input:

{
  "material_cost": 10,
  "labor_hours": 2,
  "labor_rate": 20,
  "packaging_cost": 3,
  "shipping_cost": 5,
  "target_margin": 40
}
Step 1

Labor Cost

labor_hours × labor_rate

Example:

2 × 20 = 40
Step 2

Total Cost

material_cost
+ labor_cost
+ packaging_cost
+ shipping_cost

Example:

10 + 40 + 3 + 5 = 58
Step 3

Break Even Price

total_cost

Example:

58
Step 4

Recommended Price

Formula:

recommended_price =
total_cost /
(1 - target_margin/100)

Example:

58 / 0.60

= 96.67
Step 5

Profit Amount

recommended_price
-
total_cost

Example:

38.67
Step 6

Profit Margin

(profit_amount / recommended_price) * 100

Expected:

40%
REQUIRED PRICING OUTPUT
{
  "total_cost": 58,
  "break_even_price": 58,
  "recommended_price": 96.67,
  "profit_amount": 38.67,
  "profit_margin": 40
}
API ENDPOINTS TO BUILD
Product APIs
POST   /api/v1/products

GET    /api/v1/products

GET    /api/v1/products/{id}

PUT    /api/v1/products/{id}

DELETE /api/v1/products/{id}
Product Cost APIs
POST   /api/v1/products/{id}/costs

GET    /api/v1/products/{id}/costs

PUT    /api/v1/products/{id}/costs
Pricing APIs
POST   /api/v1/pricing/calculate

GET    /api/v1/pricing/{product_id}
OWNERSHIP RULES

Users can:

create own products
view own products
update own products
delete own products

Admins can:

access everything

Ownership validation must happen in:

Service Layer

Never inside routes.

DATABASE MIGRATION PLAN

Migration 1:

products

Migration 2:

product_costs

Add:

foreign keys
indexes
timestamps

Commands:

docker compose exec backend alembic revision --autogenerate -m "add products"

docker compose exec backend alembic upgrade head
PHASE 2 (AFTER MVP WORKS)

Reuse existing AI engine.

Location:

core/ai/ai_engine/

Add:

confidence_score

market_position

pricing_recommendation

pricing_reasoning

Example:

{
  "confidence_score": 0.84,
  "market_position": "competitive",
  "pricing_recommendation": "recommended",
  "reasoning": "Healthy margin with sustainable labor recovery."
}

Do NOT implement Phase 2 until MVP is complete.

DO NOT BUILD YET

Do NOT spend time on:

Campaign Module
Marketplace
Influencer Features
Stripe
Billing
Subscriptions
Analytics Dashboard
OpenAI Integration
Etsy Integration
Microservices

Those are future phases.

DEFINITION OF MVP COMPLETE

The project is considered successfully runnable when:

✅ Existing auth remains unchanged

✅ Existing creator module remains functional

✅ Product CRUD works

✅ ProductCost CRUD works

✅ Ownership checks work

✅ PricingService works

✅ Pricing calculations return correct values

✅ Alembic migrations succeed

✅ Swagger docs show all new endpoints

✅ PostgreSQL persists all entities

NEXT DEVELOPMENT TASK

Implement in this exact order:

Product SQLAlchemy model
ProductCost SQLAlchemy model
Product schemas
ProductCost schemas
Product repositories
ProductCost repositories
Product services
ProductCost services
Alembic migration
Product routes
ProductCost routes
Pricing service
Pricing routes
Ownership enforcement
Swagger verification

This is the authoritative MakerMint handoff and contains only the necessary work required to continue and successfully run the MakerMint MVP.