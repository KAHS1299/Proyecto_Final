from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request
from model.training import train_model

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "tourism.csv"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

app = Flask(__name__)

def load_data():
    return pd.read_csv(DATA_PATH)

def load_model():
    if not MODEL_PATH.exists():
        train_model(DATA_PATH, MODEL_PATH)
    return joblib.load(MODEL_PATH)

# --- ROUTES ---

@app.route("/")
def index():
    data = load_data()
    summary = {
        "tourists": int(data["historical_tourists"].sum()),
        "occupancy": round(data["occupancy"].mean(), 1),
        "risk": int((data["saturation_level"] == "High").mean() * 100),
    }
    return render_template("index.html", summary=summary)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/map")
def map_view():
    return render_template("map.html")

@app.route("/prediction")
def prediction():
    data = load_data()
    towns = sorted(data["town"].unique())
    return render_template("prediction.html", towns=towns)

# --- API ENDPOINTS (Ensuring English Keys) ---

@app.route("/api/dashboard")
def api_dashboard():
    data = load_data()
    by_town = data.groupby("town", as_index=False).agg(
        tourists=("historical_tourists", "mean"), 
        occupancy=("occupancy", "mean")
    ).sort_values("tourists", ascending=False)
    
    by_month = data.groupby("month", as_index=False).agg(
        tourists=("historical_tourists", "sum")
    ).sort_values("month")
    
    levels = data["saturation_level"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0)
    
    return jsonify({
        "towns": by_town["town"].tolist(),
        "tourists": by_town["tourists"].round(0).astype(int).tolist(),
        "occupancy": by_town["occupancy"].round(1).tolist(),
        "months": by_month["month"].tolist(),
        "monthly": by_month["tourists"].astype(int).tolist(),
        "levels": levels.tolist()
    })

@app.route("/api/map")
def api_map():
    data = load_data()
    # Get the latest data point for each town
    latest = data.sort_values("month").groupby("town", as_index=False).tail(1)
    return jsonify(latest.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
