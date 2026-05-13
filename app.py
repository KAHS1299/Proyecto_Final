from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

from model.entrenamiento import entrenar_modelo


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "turismo.csv"
MODEL_PATH = BASE_DIR / "model" / "modelo.pkl"

app = Flask(__name__)


def cargar_datos():
    return pd.read_csv(DATA_PATH)


def cargar_modelo():
    if not MODEL_PATH.exists():
        entrenar_modelo(DATA_PATH, MODEL_PATH)
    return joblib.load(MODEL_PATH)


def construir_features(payload):
    return pd.DataFrame(
        [
            {
                "pueblo": payload.get("pueblo", "Villa de Leyva"),
                "temporada": payload.get("temporada", "Alta"),
                "festivo": payload.get("festivo", "Si"),
                "clima": payload.get("clima", "Templado"),
                "movilidad": payload.get("movilidad", "Alta"),
                "eventos": int(payload.get("eventos", 2)),
                "mes": int(payload.get("mes", 7)),
                "turistas_historicos": int(payload.get("turistas_historicos", 4200)),
            }
        ]
    )


def explicar_prediccion(features, nivel, turistas):
    fila = features.iloc[0]
    motivos = []
    if fila["temporada"] == "Alta":
        motivos.append("temporada alta")
    if fila["festivo"] == "Si":
        motivos.append("presencia de festivos")
    if fila["movilidad"] == "Alta":
        motivos.append("alta movilidad")
    if fila["eventos"] >= 2:
        motivos.append("eventos culturales activos")

    if not motivos:
        motivos.append("condiciones moderadas de viaje")

    return (
        f"La IA predice saturacion {nivel.lower()} para {fila['pueblo']} "
        f"por {', '.join(motivos)}. Estimacion: {turistas:,} turistas."
    )


@app.route("/")
def index():
    datos = cargar_datos()
    resumen = {
        "turistas": int(datos["turistas_historicos"].sum()),
        "ocupacion": round(datos["ocupacion"].mean(), 1),
        "riesgo": int((datos["nivel_saturacion"] == "Alta").mean() * 100),
    }
    return render_template("index.html", resumen=resumen)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


@app.route("/prediccion")
def prediccion():
    datos = cargar_datos()
    pueblos = sorted(datos["pueblo"].unique())
    return render_template("prediccion.html", pueblos=pueblos)


@app.route("/api/dashboard")
def api_dashboard():
    datos = cargar_datos()
    por_pueblo = (
        datos.groupby("pueblo", as_index=False)
        .agg(turistas=("turistas_historicos", "mean"), ocupacion=("ocupacion", "mean"))
        .sort_values("turistas", ascending=False)
    )
    por_mes = (
        datos.groupby("mes", as_index=False)
        .agg(turistas=("turistas_historicos", "sum"), ocupacion=("ocupacion", "mean"))
        .sort_values("mes")
    )
    niveles = datos["nivel_saturacion"].value_counts().reindex(["Baja", "Media", "Alta"], fill_value=0)
    return jsonify(
        {
            "pueblos": por_pueblo["pueblo"].tolist(),
            "turistas": por_pueblo["turistas"].round(0).astype(int).tolist(),
            "ocupacion": por_pueblo["ocupacion"].round(1).tolist(),
            "meses": por_mes["mes"].tolist(),
            "mensual": por_mes["turistas"].astype(int).tolist(),
            "niveles": niveles.tolist(),
        }
    )


@app.route("/api/mapa")
def api_mapa():
    datos = cargar_datos()
    ultimo = datos.sort_values("mes").groupby("pueblo", as_index=False).tail(1)
    return jsonify(ultimo.to_dict(orient="records"))


@app.route("/api/prediccion", methods=["POST"])
def api_prediccion():
    payload = request.get_json() or {}
    modelo = cargar_modelo()
    features = construir_features(payload)
    nivel = modelo["clasificador"].predict(features)[0]
    turistas = int(modelo["regresor"].predict(features)[0])
    turistas = max(turistas, 250)
    explicacion = explicar_prediccion(features, nivel, turistas)
    recomendacion = (
        "Viaja en temporada baja o entre semana para reducir congestiones."
        if nivel == "Alta"
        else "Es una ventana favorable para visitar con menor saturacion."
    )
    return jsonify(
        {
            "nivel": nivel,
            "turistas": turistas,
            "explicacion": explicacion,
            "recomendacion": recomendacion,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
