import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { getCities, getWeather, getHistory } from "./api";
import "./App.css";

function App() {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState(null);
  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load the list of cities once when the app starts
  useEffect(() => {
    getCities().then((data) => {
      setCities(data);
      if (data.length > 0) setSelectedCity(data[0]);
    });
  }, []);

  // Load weather + history whenever the selected city changes
// Load weather + history when city changes, and auto-refresh every 60 seconds
  useEffect(() => {
    if (!selectedCity) return;

    // A reusable function to fetch the data
    const fetchData = (showLoading) => {
      if (showLoading) setLoading(true);
      Promise.all([getWeather(selectedCity), getHistory(selectedCity)])
        .then(([w, h]) => {
          setWeather(w);
          setHistory(
            h.map((row) => ({
              time: new Date(row.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              temperature: row.temperature,
              humidity: row.humidity,
            }))
          );
        })
        .finally(() => setLoading(false));
    };

    // Fetch immediately when city changes (show loading spinner)
    fetchData(true);

    // Then auto-refresh every 60 seconds (silently, no spinner)
    const interval = setInterval(() => fetchData(false), 60000);

    // Clean up the timer when city changes or component unmounts
    return () => clearInterval(interval);
  }, [selectedCity]);

  return (
    <div className="app">
      <div className="header">
        <h1>🌤️ Weather Dashboard</h1>
        <p>Live weather data </p>
      </div>

      {/* City selector buttons */}
      <div className="city-buttons">
        {cities.map((city) => (
          <button
            key={city}
            className={`city-btn ${city === selectedCity ? "active" : ""}`}
            onClick={() => setSelectedCity(city)}
          >
            {city}
          </button>
        ))}
      </div>

      {loading && <div className="loading">Loading {selectedCity}...</div>}

      {/* Weather cards */}
      {weather && !loading && (
        <>
          <div className="cards">
            <div className="card">
              <div className="label">Temperature</div>
              <div className="value">{weather.temperature}°C</div>
            </div>
            <div className="card">
              <div className="label">Feels Like</div>
              <div className="value">{weather.feels_like}°C</div>
            </div>
            <div className="card">
              <div className="label">Humidity</div>
              <div className="value">{weather.humidity}%</div>
            </div>
            <div className="card">
              <div className="label">Wind Speed</div>
              <div className="value">{weather.wind_speed}</div>
            </div>
          </div>

          {/* Temperature history chart */}
          <div className="chart-box">
            <h2>Temperature History — {selectedCity}</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.2)" />
                <XAxis dataKey="time" stroke="#fff" />
                <YAxis stroke="#fff" />
                <Tooltip contentStyle={{ background: "#764ba2", border: "none", borderRadius: "10px", color: "#fff" }} />
                <Line type="monotone" dataKey="temperature" stroke="#ffd700" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  );
}

export default App;

