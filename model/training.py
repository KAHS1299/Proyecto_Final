from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Updated categories to match English headers
CATEGORICAL = ["town", "season", "holiday", "weather", "mobility"]
NUMERICAL = ["events", "month", "historical_tourists"]

def train_model(data_path=None, model_path=None):
    base_dir = Path(__file__).resolve().parents[1]
    
    # Updated default file names to English
    data_path = Path(data_path or base_dir / "data" / "tourism.csv")
    model_path = Path(model_path or base_dir / "model" / "model.pkl")

    data = pd.read_csv(data_path)
    X = data[CATEGORICAL + NUMERICAL]

    # Preprocessor configuration
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("num", "passthrough", NUMERICAL),
        ]
    )

    # Classifier Pipeline (formerly sorter)
    classifier = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=120, random_state=42)),
        ]
    )
    
    # Regressor Pipeline
    regressor = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(n_estimators=120, random_state=42)),
        ]
    )

    # Training using English column names
    classifier.fit(X, data["saturation_level"])
    regressor.fit(X, data["estimated_tourists"])

    # Saving the model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"classifier": classifier, "regressor": regressor}, model_path)
    
    return model_path

if __name__ == "__main__":
    saved_path = train_model()
    print(f"Model saved in: {saved_path}")
