from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

from model.training import FEATURES, engineer_features, train_model

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "tourism.csv"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

app = Flask(__name__)

TOWN_CONTENT = {
    "Villa de Leyva": {
        "department": "Boyaca",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Plaza_Mayor_-_Villa_de_Leyva%2C_Boyac%C3%A1%2C_Colombia.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Plaza_Mayor_-_Villa_de_Leyva%2C_Boyac%C3%A1%2C_Colombia.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Villa_de_Leyva_Boyaca_Colombia.jpg?width=900",
        ],
        "description": "A preserved colonial town known for one of the largest main squares in South America, pale stone architecture, fossils, and desert landscapes.",
        "history": "Founded in 1572, Villa de Leyva became a religious, agricultural, and political center during the colonial period.",
        "attractions": ["Main Square", "Paleontological Museum", "Pozos Azules", "Santo Ecce Homo Convent"],
        "season": "March to May and September to November",
    },
    "Salento": {
        "department": "Quindio",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Valle_de_Cocora_Salento.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Valle_de_Cocora_Salento.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Salento_Quindio_Colombia.jpg?width=900",
        ],
        "description": "A coffee region icon connected to Cocora Valley, wax palms, artisan streets, and mountain viewpoints.",
        "history": "Salento is among the oldest settlements in Quindio and grew around mule routes and coffee culture.",
        "attractions": ["Cocora Valley", "Calle Real", "Coffee farms", "Alto de la Cruz"],
        "season": "February to May and September",
    },
    "Barichara": {
        "department": "Santander",
        "image": "/static/img/towns/barichara-1.jpg",
        "gallery": [
            "/static/img/towns/barichara-1.jpg",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Barichara_Santander_Colombia.jpg?width=900",
        ],
        "description": "A stone-built heritage town recognized for traditional architecture, quiet viewpoints, and craft culture.",
        "history": "Declared a national monument in 1978, Barichara preserves a strong colonial urban layout and artisanal identity.",
        "attractions": ["Camino Real to Guane", "Cathedral", "Viewpoints", "Paper workshops"],
        "season": "January to March and August to November",
    },
    "Guatapé": {
        "department": "Antioquia",
        "image": "/static/img/towns/guatape-1.jpg",
        "gallery": [
            "/static/img/towns/guatape-1.jpg",
            "/static/img/towns/guatape-2.jpg",
        ],
        "description": "A colorful lakeside destination famous for painted zocalos, boat routes, and El Penol Rock.",
        "history": "The modern tourism economy expanded after the hydroelectric reservoir reshaped the landscape in the twentieth century.",
        "attractions": ["El Penol Rock", "Reservoir", "Zocalo streets", "Boat tours"],
        "season": "Weekdays throughout the year",
    },
    "Jardín": {
        "department": "Antioquia",
        "image": "/static/img/towns/jardin-1.jpg",
        "gallery": [
            "/static/img/towns/jardin-1.jpg",
            "/static/img/towns/jardin-2.jpg",
        ],
        "description": "A coffee mountain town with colorful balconies, nature trails, birdwatching, and a lively central square.",
        "history": "Jardin developed as an agricultural and coffee municipality and is recognized for its conserved architecture.",
        "attractions": ["Minor Basilica", "La Garrucha", "Coffee farms", "Waterfall routes"],
        "season": "February to April and September",
    },
    "Filandia": {
        "department": "Quindio",
        "image": "/static/img/towns/filandia-1.jpg",
        "gallery": [
            "/static/img/towns/filandia-1.jpg",
            "/static/img/towns/filandia-2.jpg",
        ],
        "description": "A quieter coffee cultural landscape destination with viewpoints, basketry, and traditional streets.",
        "history": "Filandia formed part of the Antioquian colonization route and preserves coffee region urban traditions.",
        "attractions": ["Illuminated Hill viewpoint", "Basketry workshops", "Main square", "Coffee routes"],
        "season": "May to June and September to November",
    },
    "Mompox": {
        "department": "Bolivar",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Mompox_Colombia.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Mompox_Colombia.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Santa_Cruz_de_Mompox_Colombia.jpg?width=900",
        ],
        "description": "A UNESCO-listed river town with churches, filigree jewelry, inland Caribbean history, and preserved colonial streets.",
        "history": "Mompox was a strategic port on the Magdalena River and played a major role in commerce and independence history.",
        "attractions": ["Santa Barbara Church", "Magdalena River", "Filigree workshops", "Historic center"],
        "season": "January to March and September",
    },
    "Jericó": {
        "department": "Antioquia",
        "image": "/static/img/towns/jerico-1.jpg",
        "gallery": [
            "/static/img/towns/jerico-1.jpg",
            "/static/img/towns/jerico-2.jpg",
        ],
        "description": "A mountain heritage town associated with religious tourism, leather crafts, viewpoints, and coffee landscapes.",
        "history": "Jerico is linked to Antioquian colonization, religious heritage, and the life of Saint Laura Montoya.",
        "attractions": ["Morro El Salvador", "Religious museums", "Leather workshops", "Main square"],
        "season": "March to June and September",
    },
    "Monguí": {
        "department": "Boyaca",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Mongu%C3%AD_Boyac%C3%A1_Colombia.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Mongu%C3%AD_Boyac%C3%A1_Colombia.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Paramo_de_Oceta.jpg?width=900",
        ],
        "description": "A highland town known for colonial bridges, football manufacturing, and access to Oceta paramo.",
        "history": "Mongui preserves religious architecture and artisan traditions from the colonial and republican periods.",
        "attractions": ["Basilica", "Calicanto Bridge", "Oceta paramo", "Football workshops"],
        "season": "Dry weeks between December and March",
    },
    "Salamina": {
        "department": "Caldas",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Salamina_Caldas_Colombia.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Salamina_Caldas_Colombia.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Salamina_Caldas.jpg?width=900",
        ],
        "description": "A coffee cultural landscape town with carved wooden balconies, viewpoints, and traditional houses.",
        "history": "Salamina is a national heritage town and one of the architectural references of the coffee region.",
        "attractions": ["Historic center", "La Pila", "Coffee landscapes", "Wooden balcony routes"],
        "season": "March to May and September to November",
    },
    "Honda": {
        "department": "Tolima",
        "image": "/static/img/towns/honda-1.jpg",
        "gallery": [
            "/static/img/towns/honda-1.jpg",
            "/static/img/towns/honda-2.jpg",
        ],
        "description": "A warm Magdalena River heritage town with bridges, historic streets, fishing culture, and colonial trade memory.",
        "history": "Honda was one of the most important river ports for commerce between the Caribbean and central Colombia.",
        "attractions": ["Navarro Bridge", "Magdalena River Museum", "Calle de las Trampas", "Market district"],
        "season": "June to September for lower rain probability",
    },
    "Santa Fe de Antioquia": {
        "department": "Antioquia",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Santa_Fe_de_Antioquia_Colombia.jpg?width=1100",
        "gallery": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Santa_Fe_de_Antioquia_Colombia.jpg?width=900",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Puente_de_Occidente_Santa_Fe_de_Antioquia.jpg?width=900",
        ],
        "description": "A hot-climate colonial town with churches, museums, cobbled streets, and the iconic Puente de Occidente.",
        "history": "It was the first capital of Antioquia and remains a key reference for regional colonial history.",
        "attractions": ["Puente de Occidente", "Metropolitan Cathedral", "Juan del Corral Museum", "Historic streets"],
        "season": "Weekdays outside school vacations",
    },
}


def load_data():
    return pd.read_csv(DATA_PATH)


def load_model():
    if not MODEL_PATH.exists() or MODEL_PATH.stat().st_mtime < DATA_PATH.stat().st_mtime:
        train_model(DATA_PATH, MODEL_PATH)
    return joblib.load(MODEL_PATH)


def latest_town_records():
    data = load_data()
    latest = data.sort_values(["town", "month"]).groupby("town", as_index=False).tail(1)
    return latest.sort_values("town")


def enriched_towns():
    rows = []
    for record in latest_town_records().to_dict(orient="records"):
        content = TOWN_CONTENT.get(record["town"], {})
        rows.append({**record, **content})
    return rows


@app.route("/")
def index():
    data = load_data()
    model = load_model()
    summary = {
        "towns": int(data["town"].nunique()),
        "tourists": int(data["historical_tourists"].sum()),
        "occupancy": round(data["occupancy"].mean(), 1),
        "accuracy": int(model["metrics"]["accuracy"] * 100),
    }
    return render_template("index.html", summary=summary, towns=enriched_towns()[:3])


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/map")
def map_view():
    return render_template("map.html")


@app.route("/prediction")
def prediction():
    towns = sorted(load_data()["town"].unique())
    return render_template("prediction.html", towns=towns)


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/crisp-ml")
def crisp_ml():
    return render_template("crisp_ml.html")


@app.route("/towns")
def towns():
    return render_template("towns.html", towns=enriched_towns())


@app.route("/api/dashboard")
def api_dashboard():
    data = load_data()
    by_town = data.groupby("town", as_index=False).agg(
        tourists=("historical_tourists", "mean"),
        occupancy=("occupancy", "mean"),
        estimated=("estimated_tourists", "mean"),
    ).sort_values("tourists", ascending=False)
    by_month = data.groupby("month", as_index=False).agg(tourists=("historical_tourists", "sum")).sort_values("month")
    levels = data["saturation_level"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0)
    return jsonify(
        {
            "towns": by_town["town"].tolist(),
            "tourists": by_town["tourists"].round(0).astype(int).tolist(),
            "occupancy": by_town["occupancy"].round(1).tolist(),
            "estimated": by_town["estimated"].round(0).astype(int).tolist(),
            "months": by_month["month"].tolist(),
            "monthly": by_month["tourists"].astype(int).tolist(),
            "levels": levels.tolist(),
        }
    )


@app.route("/api/map")
def api_map():
    return jsonify(enriched_towns())


@app.route("/api/analytics")
def api_analytics():
    model = load_model()
    metrics = model["metrics"]
    return jsonify(metrics)


@app.route("/api/monitoring")
def api_monitoring():
    return jsonify(
        {
            "drift": [0.04, 0.05, 0.08, 0.12, 0.14, 0.18, 0.21],
            "confidence": [0.91, 0.9, 0.88, 0.86, 0.84, 0.82, 0.8],
            "labels": ["W1", "W2", "W3", "W4", "W5", "W6", "W7"],
            "retraining": "Recommended if drift exceeds 0.25",
        }
    )


@app.route("/api/prediction", methods=["POST"])
def api_prediction():
    payload = request.get_json(force=True)
    data = pd.DataFrame([payload])
    data["occupancy"] = min(99, max(18, (data.loc[0, "historical_tourists"] / 125) + data.loc[0, "events"] * 6))
    features = engineer_features(data)[FEATURES]

    model = load_model()
    classifier = model["classifier"]
    regressor = model["regressor"]
    level = classifier.predict(features)[0]
    probabilities = classifier.predict_proba(features)[0]
    confidence = round(float(max(probabilities)) * 100, 1)
    estimated = int(regressor.predict(features)[0])

    recommendation = {
        "Low": "Demand is favorable. Recommend heritage walks, museums, and flexible booking.",
        "Medium": "Demand is rising. Recommend early arrivals, pre-booked activities, and weekday mobility.",
        "High": "High saturation expected. Recommend booking accommodation, transport, and attractions in advance.",
    }[level]

    return jsonify(
        {
            "level": level,
            "confidence": confidence,
            "tourists": estimated,
            "recommendation": recommendation,
            "explanation": "Random Forest evaluated season, holidays, weather, mobility, events, month, historical flow, and engineered pressure indicators.",
            "probabilities": {
                label: round(float(prob) * 100, 1)
                for label, prob in zip(classifier.classes_, probabilities)
            },
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
