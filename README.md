# 🌤️ Weather Data Pipeline & Dashboard

A full-stack data engineering project that collects real-time weather data, cleans and stores it, serves it through an API, and displays it on a live, auto-refreshing dashboard. The pipeline is automated with Apache Airflow.

## Overview

This project demonstrates a complete ETL (Extract, Transform, Load) data pipeline combined with a full-stack web application. Weather data is fetched from an external API, processed, stored in a PostgreSQL database, exposed via a FastAPI backend, and visualized in a React dashboard that updates in real time.

```
Weather API  ->  Python Pipeline (ETL)  ->  PostgreSQL
                                               |
                                          FastAPI (REST API)
                                               |
                                          React (Dashboard)
                                               |
                                             User
```

The pipeline runs automatically every 5 minutes via Apache Airflow, and the dashboard re-fetches data every 60 seconds, giving a true real-time experience.

## Features

- Automated ETL pipeline that extracts live weather data for multiple cities
- Data cleaning and transformation with pandas
- Persistent storage in PostgreSQL
- REST API built with FastAPI, serving cities, current weather, and historical data
- Colorful, responsive React dashboard with a glassmorphism design
- Live temperature history charts using Recharts
- Frontend auto-refresh every 60 seconds
- Scheduled pipeline runs every 5 minutes using Apache Airflow
- Fully containerized database and Airflow setup with Docker

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Source | OpenWeatherMap API |
| Pipeline (ETL) | Python, requests, pandas |
| Database | PostgreSQL (Docker) |
| Backend API | FastAPI, uvicorn, psycopg2 |
| Frontend | React (Vite), axios, Recharts |
| Orchestration | Apache Airflow (Docker Compose) |
| Containerization | Docker, Docker Compose |

## Project Structure

```
weather/
├── server/                  # Backend (Python)
│   ├── pipeline/            # ETL pipeline
│   │   ├── extract.py       # Fetch raw data from the weather API
│   │   ├── transform.py     # Clean and reshape the data
│   │   ├── load.py          # Save data into PostgreSQL
│   │   └── run_pipeline.py  # Run the full pipeline for all cities
│   ├── api/                 # FastAPI backend
│   │   ├── main.py          # API endpoints
│   │   └── database.py      # Database connection helper
│   ├── .env                 # Secrets (API key, DB credentials) - not committed
│   └── requirements.txt     # Python dependencies
│
├── client/                  # Web frontend (React)
│   └── src/
│       ├── App.jsx          # Main dashboard component
│       ├── App.css          # Styles
│       └── api.js           # API call helpers
│
├── airflow/                 # Workflow orchestration
│   ├── dags/                # Airflow DAGs (scheduled workflows)
│   ├── docker-compose.yaml  # Airflow container setup
│   └── ...
│
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- A free OpenWeatherMap API key (https://openweathermap.org/api)

## Setup & Installation

### 1. Database (PostgreSQL via Docker)

Start a PostgreSQL container:

```bash
docker run --name weather-db \
  -e POSTGRES_USER=weather_user \
  -e POSTGRES_PASSWORD=weather_pass \
  -e POSTGRES_DB=weather_db \
  -p 5433:5432 \
  -d postgres:16
```

Create the `weather` table:

```sql
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature REAL,
    feels_like REAL,
    humidity INTEGER,
    description VARCHAR(255),
    wind_speed REAL,
    recorded_at TIMESTAMP NOT NULL
);
```

### 2. Backend (FastAPI + Pipeline)

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `server` folder:

```
WEATHER_API_KEY=your_api_key_here
DB_HOST=localhost
DB_PORT=5433
DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=weather_pass
```

Run the pipeline once to populate data:

```bash
python pipeline/run_pipeline.py
```

Start the API:

```bash
uvicorn api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### 3. Frontend (React)

```bash
cd client
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### 4. Airflow (Automated Scheduling)

```bash
cd airflow
docker compose up airflow-init
docker compose up -d
```

Open the Airflow dashboard at `http://localhost:8080` (default login: `airflow` / `airflow`). Enable the weather pipeline DAG to run automatically every 5 minutes.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/cities` | List all tracked cities |
| GET | `/weather/{city}` | Latest weather for a city |
| GET | `/weather/{city}/history` | Historical weather records for a city |

## How It Works

1. **Extract** — The pipeline calls the OpenWeatherMap API for each tracked city and receives raw JSON data.
2. **Transform** — pandas cleans the data, keeping only the needed fields, converting units, and adding a timestamp.
3. **Load** — The clean data is inserted as new rows into PostgreSQL.
4. **Serve** — FastAPI reads from the database and returns clean JSON through its endpoints.
5. **Visualize** — The React dashboard calls the API, displays current conditions as cards, and renders a temperature history chart.
6. **Automate** — Apache Airflow triggers the pipeline every 5 minutes, continuously building up weather history.

## Running the Full Project

You will need these running together:

1. PostgreSQL container — `docker start weather-db`
2. FastAPI backend — `uvicorn api.main:app --reload --port 8000` (from `server`)
3. React frontend — `npm run dev` (from `client`)
4. Airflow — `docker compose up -d` (from `airflow`)

## Notes

- The `.env` files containing secrets are excluded from version control via `.gitignore`.
- PostgreSQL runs on port `5433` to avoid conflicts with a locally installed PostgreSQL on `5432`.
- The dashboard's temperature chart fills with more variation as the pipeline collects data over time.

## License

This project is for educational purposes.

## 👨‍💻 Author

R. P. T. Sandeepa Dilhara (computer engineer and IT undergraduate student )