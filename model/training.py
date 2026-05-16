from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL = ["town", "season", "holiday", "weather", "mobility"]
NUMERICAL = ["events", "month", "historical_tourists", "occupancy_pressure", "event_pressure"]
FEATURES = CATEGORICAL + NUMERICAL
LABELS = ["Low", "Medium", "High"]

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def normalize_tourism_data(data, require_targets=True):
    framed = data.copy()
    framed.columns = [column.strip() for column in framed.columns]

    if "occupancy" not in framed.columns and "hotel_occupancy" in framed.columns:
        framed["occupancy"] = framed["hotel_occupancy"]

    if "mobility" not in framed.columns:
        if "mobility_index" in framed.columns:
            mobility_index = pd.to_numeric(framed["mobility_index"], errors="coerce")
        elif "road_traffic" in framed.columns:
            mobility_index = pd.to_numeric(framed["road_traffic"], errors="coerce")
        else:
            mobility_index = pd.Series(50, index=framed.index)

        framed["mobility"] = pd.cut(
            mobility_index.fillna(mobility_index.median()).fillna(50),
            bins=[-1, 39, 69, 100],
            labels=["Low", "Medium", "High"],
        ).astype(str)

    if "month" in framed.columns:
        month_text = framed["month"].astype(str).str.strip().str.lower()
        framed["month"] = pd.to_numeric(framed["month"], errors="coerce").fillna(month_text.map(MONTHS))

    for column in ["events", "month", "historical_tourists", "estimated_tourists", "occupancy", "lat", "lon"]:
        if column in framed.columns:
            framed[column] = pd.to_numeric(framed[column], errors="coerce")

    required_columns = CATEGORICAL + ["events", "month", "historical_tourists", "occupancy"]
    if require_targets:
        required_columns += ["saturation_level", "estimated_tourists"]

    required = set(required_columns)
    missing = sorted(required.difference(framed.columns))
    if missing:
        raise ValueError(f"Tourism dataset is missing required columns: {', '.join(missing)}")

    # CORRECCIÓN DE SEGURIDAD: Limpieza estricta de filas vacías o nulas para Scikit-Learn
    framed = framed.dropna(subset=required_columns)
    if require_targets:
        framed = framed[framed["saturation_level"].isin(LABELS)]
        
    return framed


def engineer_features(data, require_targets=False):
    framed = normalize_tourism_data(data, require_targets=require_targets)
    framed["occupancy_pressure"] = framed["occupancy"] / 100
    framed["event_pressure"] = framed["events"] * framed["historical_tourists"] / 10000
    return framed


def _feature_names(preprocessor):
    cat_names = preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL)
    return list(cat_names) + NUMERICAL


def train_model(data_path=None, model_path=None):
    base_dir = Path(__file__).resolve().parents[1]
    data_path = Path(data_path or base_dir / "data" / "tourism.csv")
    model_path = Path(model_path or base_dir / "model" / "model.pkl")

    data = engineer_features(pd.read_csv(data_path), require_targets=True)
    
    # Control de contingencia en caso de que las muestras sean extremadamente bajas en producción
    if len(data) < 5:
        # Duplicamos sintéticamente el mini dataset de arranque para no romper las matrices de división
        data = pd.concat([data] * 5, ignore_index=True)

    X = data[FEATURES]
    y = data["saturation_level"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("num", "passthrough", NUMERICAL),
        ]
    )

    classifier = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=260, max_depth=9, random_state=42)),
        ]
    )

    regressor = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(n_estimators=220, max_depth=9, random_state=42)),
        ]
    )

    # CORRECCIÓN CONTROL SAMPLES: Estratificación segura inteligente
    min_class_count = y.value_counts().min()
    stratify = y if min_class_count >= 2 and len(y.unique()) > 1 else None
    test_size = 0.28 if len(data) > 10 else 0.1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=stratify
    )

    classifier.fit(X_train, y_train)
    regressor.fit(X_train, data.loc[X_train.index, "estimated_tourists"])

    y_pred = classifier.predict(X_test)
    report = classification_report(y_test, y_pred, labels=LABELS, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_test, y_pred, labels=LABELS)

    fitted_preprocessor = classifier.named_steps["preprocessor"]
    importances = classifier.named_steps["model"].feature_importances_
    feature_importance = sorted(
        [
            {"feature": feature, "importance": round(float(score), 4)}
            for feature, score in zip(_feature_names(fitted_preprocessor), importances)
        ],
        key=lambda item: item["importance"],
        reverse=True,
    )[:10]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 3),
        "precision": round(float(report["weighted avg"]["precision"]), 3),
        "recall": round(float(report["weighted avg"]["recall"]), 3),
        "f1": round(float(report["weighted avg"]["f1-score"]), 3),
        "confusion_matrix": matrix.tolist(),
        "labels": LABELS,
        "feature_importance": feature_importance,
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "classifier": classifier,
            "regressor": regressor,
            "metrics": metrics,
            "features": FEATURES,
        },
        model_path,
    )

    return model_path


if __name__ == "__main__":
    saved_path = train_model()
    print(f"Model saved at: {saved_path}")
