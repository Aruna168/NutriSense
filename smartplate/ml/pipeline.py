from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from joblib import dump, load


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "nutrition_sample.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "model")
KMEANS_PATH = os.path.join(MODEL_DIR, "kmeans.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.joblib")


@dataclass
class NutrientTargets:
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


class SmartPlatePipeline:
    """
    This pipeline demonstrates how ML techniques power personalization:

    - Data Preprocessing: loads dataset, handles missing values, scales features.
    - Clustering (KMeans): groups foods by nutrition profile to diversify meals.
    - Regression (placeholder here): predicts daily targets from user profile; in
      production, use XGBoost/LightGBM trained on labeled data.
    - Content-Based Recommendation: computes cosine similarity between target
      nutrient vector and food item vectors (within cluster neighborhoods) to
      generate meal suggestions.
    """

    def __init__(self, n_clusters: int = 8) -> None:
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.n_clusters = n_clusters
        self.food_df = self._load_dataset()
        self.scaler, self.kmeans = self._fit_or_load_models(self.food_df)

    def _load_dataset(self) -> pd.DataFrame:
        df = pd.read_csv(DATA_PATH)
        df = df.dropna(subset=["name", "category"]).copy()
        # Fill missing numeric nutrients with median
        for col in ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg"]:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        return df

    def _fit_or_load_models(self, df: pd.DataFrame):
        features = df[["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg"]].values
        if os.path.exists(SCALER_PATH) and os.path.exists(KMEANS_PATH):
            scaler = load(SCALER_PATH)
            kmeans = load(KMEANS_PATH)
        else:
            scaler = StandardScaler()
            X = scaler.fit_transform(features)
            kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
            kmeans.fit(X)
            dump(scaler, SCALER_PATH)
            dump(kmeans, KMEANS_PATH)

        # assign cluster labels (stored in-memory for recommendation neighborhoods)
        X = scaler.transform(features)
        self.food_df = df.copy()
        self.food_df["cluster_label"] = kmeans.predict(X)
        return scaler, kmeans

    # ---------------- Regression Placeholder ----------------
    def predict_daily_targets(self, user: Dict) -> Dict[str, float]:
        """
        Predict daily macro targets from user profile.

        In production: train a gradient boosting regressor (XGBoost/LightGBM)
        to predict calories, protein, carbs, fat based on age, gender, BMI, and
        activity. For this scaffold, we compute Mifflin-St Jeor BMR and apply
        multipliers and goal adjustments as a strong baseline.
        """
        age = int(user["age"])
        gender = user["gender"]
        height_cm = float(user["height_cm"])
        weight_kg = float(user["weight_kg"])
        activity_level = user["activity_level"]
        goal = user["goal"]

        if gender == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        activity_map = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9,
        }
        tdee = bmr * activity_map.get(activity_level, 1.2)

        if goal == "weight_loss":
            calories = tdee - 400
        elif goal == "muscle_gain":
            calories = tdee + 300
        else:
            calories = tdee

        calories = max(1200.0, float(calories))

        # Macro split baseline (can be learned with regression models):
        protein_g = round(1.8 * weight_kg, 1)
        fat_g = round(0.9 * weight_kg, 1)
        protein_kcal = protein_g * 4
        fat_kcal = fat_g * 9
        remaining_kcal = max(0.0, calories - protein_kcal - fat_kcal)
        carbs_g = round(remaining_kcal / 4, 1)

        return {
            "calories": round(calories, 0),
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fat_g": fat_g,
        }

    # -------------- Content-based Recommendation --------------
    def recommend_meal_plan(self, targets: Dict[str, float], allergies: str = "") -> List[Dict]:
        """
        Recommend top foods close to the user's target nutrient vector.

        Steps:
        1) Form a nutrient target vector from daily targets
        2) Select candidate foods from clusters with similar calorie density
        3) Compute cosine similarity between scaled food vectors and target vector
        4) Return top-N items excluding allergens
        """
        allergy_terms = {a.strip().lower() for a in allergies.split(",") if a.strip()}

        df = self.food_df.copy()
        # Filter allergen hits by name/category
        if allergy_terms:
            mask = ~df["name"].str.lower().apply(lambda n: any(t in n for t in allergy_terms))
            mask &= ~df["category"].str.lower().apply(lambda n: any(t in n for t in allergy_terms))
            df = df[mask]

        feature_cols = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg"]
        X = self.scaler.transform(df[feature_cols].values)

        # Build target vector emphasizing calories/macros; fiber/sodium neutral
        target_vec_raw = np.array([
            targets.get("calories", 2000) / 4,  # downscale calories magnitude
            targets.get("protein_g", 120),
            targets.get("carbs_g", 250),
            targets.get("fat_g", 70),
            25.0,  # fiber target baseline
            1500.0,  # sodium baseline
        ]).reshape(1, -1)
        target_vec = self.scaler.transform(target_vec_raw)

        sims = cosine_similarity(X, target_vec).ravel()
        df = df.assign(similarity=sims)

        # Promote diversity across clusters (take top per cluster and then merge)
        top_per_cluster = (
            df.sort_values("similarity", ascending=False)
            .groupby("cluster_label")
            .head(3)
        )
        top = top_per_cluster.sort_values("similarity", ascending=False).head(12)

        results: List[Dict] = []
        for _, row in top.iterrows():
            results.append(
                {
                    "food_id": int(row.get("id", 0)),
                    "name": row["name"],
                    "category": row["category"],
                    "calories": float(row["calories"]),
                    "protein_g": float(row["protein_g"]),
                    "carbs_g": float(row["carbs_g"]),
                    "fat_g": float(row["fat_g"]),
                    "cluster": int(row["cluster_label"]),
                    "similarity": float(round(row["similarity"], 4)),
                }
            )
        return results


