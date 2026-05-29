from extract import extract_weather
from transform import transform_weather
from load import load_weather

# The cities we want to track
CITIES = ["London", "Tokyo", "New York", "Colombo", "Paris"]


def run_pipeline():
    """Run Extract -> Transform -> Load for every city."""
    for city in CITIES:
        try:
            raw = extract_weather(city)
            clean_df = transform_weather(raw)
            load_weather(clean_df)
            print(f"✓ Done: {city}")
        except Exception as e:
            print(f"✗ Failed: {city} — {e}")


if __name__ == "__main__":
    run_pipeline()