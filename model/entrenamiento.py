from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


CATEGORICAS = ["pueblo", "temporada", "festivo", "clima", "movilidad"]
NUMERICAS = ["eventos", "mes", "turistas_historicos"]


def entrenar_modelo(data_path=None, model_path=None):
    base_dir = Path(__file__).resolve().parents[1]
    data_path = Path(data_path or base_dir / "data" / "turismo.csv")
    model_path = Path(model_path or base_dir / "model" / "modelo.pkl")

    datos = pd.read_csv(data_path)
    x = datos[CATEGORICAS + NUMERICAS]

    preprocesador = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
            ("num", "passthrough", NUMERICAS),
        ]
    )

    clasificador = Pipeline(
        steps=[
            ("preprocesador", preprocesador),
            ("modelo", RandomForestClassifier(n_estimators=120, random_state=42)),
        ]
    )
    regresor = Pipeline(
        steps=[
            ("preprocesador", preprocesador),
            ("modelo", RandomForestRegressor(n_estimators=120, random_state=42)),
        ]
    )

    clasificador.fit(x, datos["nivel_saturacion"])
    regresor.fit(x, datos["turistas_estimados"])

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"clasificador": clasificador, "regresor": regresor}, model_path)
    return model_path


if __name__ == "__main__":
    ruta = entrenar_modelo()
    print(f"Modelo guardado en {ruta}")
