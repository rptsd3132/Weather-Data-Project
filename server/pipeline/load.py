import os
import psycopg2
from dotenv import load_dotenv

# Load database settings from .env
load_dotenv()


def get_connection():
    """Open a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def load_weather(df):
    """Save each row of the clean DataFrame into the weather table."""
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO weather
                (city, temperature, feels_like, humidity, description, wind_speed, recorded_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["city"],
                row["temperature"],
                row["feels_like"],
                row["humidity"],
                row["description"],
                row["wind_speed"],
                row["recorded_at"]
            )
        )

    conn.commit()   # save the changes permanently
    cursor.close()
    conn.close()
    print(f"Saved {len(df)} row(s) into the database.")


# Test block
if __name__ == "__main__":
    from extract import extract_weather
    from transform import transform_weather

    raw = extract_weather("London")
    clean_df = transform_weather(raw)
    load_weather(clean_df)