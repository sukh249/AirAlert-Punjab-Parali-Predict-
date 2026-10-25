import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

print("🔄 Generating environmental dataset for Punjab region...")

# 1. Create synthetic historical data based on weather & satellite dynamics
np.random.seed(42)
num_samples = 2000

fire_count_24h = np.random.randint(0, 150, num_samples)  # Active fire count
wind_speed = np.random.uniform(2.0, 25.0, num_samples)  # Wind speed in km/h
wind_direction_deg = np.random.uniform(0, 360, num_samples)  # Direction in degrees
temperature = np.random.uniform(15.0, 38.0, num_samples)  # Temp in °C
humidity = np.random.uniform(30.0, 90.0, num_samples)  # Humidity %
current_pm25 = np.random.uniform(20.0, 300.0, num_samples)  # Current sensor PM2.5

# Relationship rule: High fires + low wind + high humidity = severe smoke buildup 24h later
predicted_pm25_24h = (
    (current_pm25 * 0.6)
    + (fire_count_24h * 1.8)
    - (wind_speed * 2.5)
    + (humidity * 0.4)
    + np.random.normal(0, 10, num_samples)
)
predicted_pm25_24h = np.clip(predicted_pm25_24h, 10, 500)

# Organize data into a structured Table (DataFrame)
df = pd.DataFrame({
    "fire_count_24h": fire_count_24h,
    "wind_speed": wind_speed,
    "wind_direction_deg": wind_direction_deg,
    "temperature": temperature,
    "humidity": humidity,
    "current_pm25": current_pm25,
    "target_pm25_24h": predicted_pm25_24h,
})

# 2. Separate Inputs (X) from the Answer/Target (y)
X = df[[
    "fire_count_24h",
    "wind_speed",
    "wind_direction_deg",
    "temperature",
    "humidity",
    "current_pm25",
]]
y = df["target_pm25_24h"]

# Split into 80% Training Data and 20% Test Data to evaluate accuracy
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🧠 Training Random Forest Machine Learning Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Test accuracy on unseen test data
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n--- MODEL TRAINING RESULTS ---")
print(f"✅ R² Score (Accuracy): {score * 100:.2f}%")
print(f"📉 Prediction Error (RMSE): ±{rmse:.2f} µg/m³")

# 4. Save model to disk
joblib.dump(model, "air_quality_model.pkl")
print("💾 Saved intelligence model as 'air_quality_model.pkl'!\n")