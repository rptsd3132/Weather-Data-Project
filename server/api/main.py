from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_connection

app = FastAPI(title="Weather API")

# Allow the React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """A simple welcome message to check the API is alive."""
    return {"message": "Weather API is running"}


@app.get("/cities")
def get_cities():
    """Return the list of distinct cities in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT city FROM weather ORDER BY city;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row["city"] for row in rows]


@app.get("/weather/{city}")
def get_latest_weather(city: str):
    """Return the most recent weather record for one city."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM weather WHERE city = %s ORDER BY recorded_at DESC LIMIT 1;",
        (city,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="City not found")
    return row


@app.get("/weather/{city}/history")
def get_weather_history(city: str):
    """Return all past weather records for one city (oldest first)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM weather WHERE city = %s ORDER BY recorded_at ASC;",
        (city,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows