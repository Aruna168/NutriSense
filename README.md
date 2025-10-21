# 🧠 NutriSense – AI-Powered Personalized Diet Planner  

> **Smart. Adaptive. Sensor-Free Nutrition.**

---

## 🌍 Overview  

**NutriSense** is an innovative AI-based nutrition planning system that delivers **personalized diet recommendations** based on user health parameters such as age, gender, BMI, and activity level.  

Unlike traditional fitness or diet apps that rely on external wearables or static data, NutriSense uses a **sensor-free personalization approach** powered by **machine learning** to dynamically adjust nutrition goals and meal plans in real time.  

The system also includes a **responsive web dashboard** that enables users to visualize nutrition data, track meal habits, and receive adaptive recommendations powered by feedback learning.  

---

## 💡 Innovation Highlights  

| Innovation Area | Description |
|------------------|-------------|
| **AI-Driven Nutrition Prediction** | Predicts optimal macronutrient ratios using ML models. |
| **Sensor-Free Personalization** | Eliminates the need for costly hardware devices. |
| **Dynamic Meal Recommendations** | Suggests daily meals tailored to health metrics, preferences, and region. |
| **User Feedback Adaptation** | Learns from user ratings and adjusts future predictions. |
| **Real-Time Web Dashboard** | Tracks calorie intake and recommendation analytics visually. |
| **Lightweight & Scalable Solution** | Built with modular Python backend and simple web frontend for easy scaling. |

---

## 🧩 Architecture Overview  

```plaintext
User Input → Preprocessing → ML Models (XGBoost, LightGBM) → Nutrition Prediction
     ↓
   Feedback Loop ← User Ratings & Behavior
     ↓
   Dynamic Meal Recommendations + Web Dashboard Visualization
```

---

If you'd like any small edits (add contributors, license, badges, screenshots, or a short usage section), tell me what to include and I'll add it.

SmartPlate – AI-Driven Personalized Nutrition System

Overview

SmartPlate is a web-based system that analyzes user details (age, gender, height, weight, activity level, allergies, and health goals) to generate personalized diet recommendations using machine learning and nutrition datasets.

Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap, Chart.js
- Backend: Python (Flask), SQLite (SQLAlchemy)
- Machine Learning: scikit-learn, XGBoost, LightGBM, pandas, NumPy

Key Features

- User registration and profile storage
- ML pipeline: preprocessing, clustering (KMeans), regression (XGBoost/LightGBM), and content-based recommendation via cosine similarity
- Meal plan generation and visualization of nutrient targets vs intake
- Feedback storage for iterative improvement

Quick Start

1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py`
4. Open http://127.0.0.1:5000 in your browser

Project Structure

```
app.py
smartplate/
  __init__.py
  config.py
  extensions.py
  models.py
  utils/
    validation.py
  blueprints/
    api/
      __init__.py
      routes.py
    web/
      __init__.py
      routes.py
  ml/
    pipeline.py
templates/
  layout.html
  index.html
  form.html
  results.html
  feedback.html
static/
  css/styles.css
  js/main.js
  js/charts.js
data/
  nutrition_sample.csv
model/
  train.ipynb
requirements.txt
README.md
```

Notes

- The `ml/pipeline.py` file contains commented explanations of how clustering, regression, and content-based filtering are used.
- The dataset in `data/nutrition_sample.csv` is a minimal sample; replace with a comprehensive dataset (e.g., USDA) for better results.


