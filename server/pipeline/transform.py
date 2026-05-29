import pandas as pd
from datetime import datetime


def transform_weather(raw_data):
    """Take raw API data and return one clean row as a DataFrame."""

    # Pick out only the fields we want from the messy dictionary
    clean = {
        "city": raw_data["name"],
        "temperature": raw_data["main"]["temp"],
        "feels_like": raw_data["main"]["feels_like"],
        "humidity": raw_data["main"]["humidity"],
        "description": raw_data["weather"][0]["description"],
        "wind_speed": raw_data["wind"]["speed"],
        "recorded_at": datetime.now()
    }

    # Put the clean data into a pandas DataFrame (a table with one row)
    df = pd.DataFrame([clean])
    return df


# Test block — runs only when this file is run directly
if __name__ == "__main__":
    from extract import extract_weather

    raw = extract_weather("London")
    clean_df = transform_weather(raw)
    print(clean_df)