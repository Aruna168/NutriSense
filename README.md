# Clean push (create fresh repo without history)

If GitHub rejected your push due to large files in history (for example a committed virtualenv or compiled binaries like xgboost.dll), you can create a fresh repository snapshot without history and push it.

1. Create a new empty repository on GitHub (do not initialize with README/license).
2. From this repo root, run the helper script and provide the new remote URL when prompted:

```powershell
.\clean_push.ps1
# then paste the new repo URL when asked
```

This will create an orphan branch `clean-main`, commit the current working tree (respecting `.gitignore`), set the given remote as `origin`, rename branch to `main`, and push.

Note: This does NOT delete the old remote's history. If you want to rewrite existing remote history instead, see the "history cleanup" instructions in the previous project notes.

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


