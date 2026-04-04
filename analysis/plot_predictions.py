import requests
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# FETCH DATA FROM API
# ---------------------------
url = "http://127.0.0.1:8000/history?limit=200"

response = requests.get(url)
data = response.json()

if "data" not in data:
    print("Error:", data)
    exit()

df = pd.DataFrame(data["data"])

# ---------------------------
# CLEAN DATA
# ---------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# ---------------------------
# PLOT
# ---------------------------
plt.figure()

# Price (low so far)
plt.plot(df["timestamp"], df["low_so_far"], label="Low So Far")

# Probability (scaled for visibility)
plt.plot(df["timestamp"], df["probability"] * df["low_so_far"].max(), label="Probability (scaled)")

plt.legend()
plt.xlabel("Time")
plt.ylabel("Value")

plt.title("Model Behavior Over Time")

plt.show()