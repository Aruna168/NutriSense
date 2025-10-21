from datetime import datetime
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(50), nullable=False)
    allergies = db.Column(db.String(255), default="")
    goal = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=False)
    carbs_g = db.Column(db.Float, nullable=False)
    fat_g = db.Column(db.Float, nullable=False)
    fiber_g = db.Column(db.Float, default=0)
    sodium_mg = db.Column(db.Float, default=0)
    cluster_label = db.Column(db.Integer, index=True)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_item.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


