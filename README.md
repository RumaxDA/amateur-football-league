# Amateur Football League (AFL) Management System

A comprehensive web application designed to manage amateur football leagues. This system provides a full suite of tools to track teams, players, tournaments, matches, and detailed in-game events (actions), offering a professional-level management experience for amateur sports.

## Tech Stack

The project uses a modern, fully-containerized architecture with REST API communication between the frontend and backend layers.

**Frontend:**

- Angular 18 (with Vite)
- Angular Material (UI Components)
- TypeScript

**Backend:**

- Python 3.11+
- FastAPI
- SQLAlchemy & Pydantic (Data Validation)
- Passlib & JWT (Authentication & Authorization)

**Infrastructure & Database:**

- PostgreSQL 17
- Docker & Docker Compose
- Nginx (SPA Routing)

## Database model

![baza](model.png)

## Core Features

- **Authentication & Authorization:** Secure registration and login system using JWT tokens. Role-based access for judges, team managers, and standard non-login users.
- **Tournaments Management:** Create and manage league seasons, track standings, and schedule fixtures.
- **Team & Player Profiles:** Full CRUD operations for teams and individual players.
- **Match Tracking:** Schedule matches, update scores, and assign them to specific tournaments.
- **Detailed Match Actions:** Record granular, real-time match events (goals, assists, yellow/red cards) to generate comprehensive player statistics.

## Getting Started

The easiest way to get the application running is via Docker.

### Prerequisites

- Docker Desktop or Docker Engine installed.
- Docker Compose installed.

### Installation & Running

**Step 1: Clone the repository**

```bash
git clone https://github.com/RumaxDA/amateur-football-league
cd amateur-football-league
```

**Step 2: Environment configuration**

```bash
cp .env.example .env
```

**Step 3: Build and start the containers**

```bash
docker compose up --build
```

### Access points

**Frontend:** http://localhost:4200
**Backend API Docs (Swagger UI):** http://localhost:8000/docs
**Database:** Accessible via port 5432 on your localhost.

### Project Structure

- **/front** - Contains the Angular frontend application.
- **/back** - Contains the FastAPI backend application and database models.
- **docker-compose.yml** - Orchestrates the database, backend, and frontend containers.
