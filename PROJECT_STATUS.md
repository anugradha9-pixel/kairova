# Kairova Project Context

## Stack
Frontend:
- React + Vite
- Axios
- React Router

Backend:
- FastAPI
- PostgreSQL
- JWT Authentication

## Current Working Features
- Login API works
- JWT token generation works
- Refresh token system works
- React login UI works
- Protected dashboard routing works
- Axios connected to backend
- CORS configured

## Backend Run Command
uvicorn backend.app:app --reload

## Frontend Run Command
npm run dev

## Frontend Port
http://localhost:5173

## Backend Port
http://127.0.0.1:8000

## Existing Routes
POST /auth/signup
POST /auth/login
POST /auth/refresh
POST /creator
GET /creator/{creator_id}/pricing
GET /me
GET /protected

## Current Frontend Structure
src/
- api/
- auth/
- components/
- pages/
- context/
- layouts/

## Current Goal
Build Creator Intelligence Dashboard:
- creator submission form
- pricing card
- confidence score
- AI reasoning panel

## Known Fixes Already Completed
- Fixed Axios import issues
- Fixed Vite App.jsx structure
- Fixed backend module imports
- Fixed CORS preflight issue
- Fixed JWT login flow