from flask import request, jsonify
from . import api_bp
from ...extensions import db
from ...models import User, FoodItem, Feedback
from ...utils.validation import validate_user_payload
from ...ml.pipeline import SmartPlatePipeline


pipeline = SmartPlatePipeline()


@api_bp.route("/register_user", methods=["POST"])
def register_user():
    payload = request.get_json(force=True, silent=True) or {}
    ok, err = validate_user_payload(payload)
    if not ok:
        return jsonify({"error": err}), 400

    user = User(
        name=payload["name"],
        age=int(payload["age"]),
        gender=payload["gender"],
        height_cm=float(payload["height_cm"]),
        weight_kg=float(payload["weight_kg"]),
        activity_level=payload["activity_level"],
        allergies=payload.get("allergies", ""),
        goal=payload["goal"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user_registered", "user_id": user.id}), 201


@api_bp.route("/predict", methods=["POST"])
def predict_targets():
    payload = request.get_json(force=True, silent=True) or {}
    ok, err = validate_user_payload(payload)
    if not ok:
        return jsonify({"error": err}), 400

    prediction = pipeline.predict_daily_targets(payload)
    return jsonify({"targets": prediction}), 200


@api_bp.route("/recommend", methods=["POST"])
def recommend_meals():
    payload = request.get_json(force=True, silent=True) or {}
    ok, err = validate_user_payload(payload)
    if not ok:
        return jsonify({"error": err}), 400

    targets = pipeline.predict_daily_targets(payload)
    recs = pipeline.recommend_meal_plan(targets, allergies=payload.get("allergies", ""))
    return jsonify({"targets": targets, "recommendations": recs}), 200


@api_bp.route("/get_recommendations", methods=["GET"])
def get_recommendations():
    # Simple GET wrapper using query params for demo
    args = request.args.to_dict()
    ok, err = validate_user_payload(args)
    if not ok:
        return jsonify({"error": err}), 400

    targets = pipeline.predict_daily_targets(args)
    recs = pipeline.recommend_meal_plan(targets, allergies=args.get("allergies", ""))
    return jsonify({"targets": targets, "recommendations": recs}), 200


@api_bp.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    payload = request.get_json(force=True, silent=True) or {}
    try:
        user_id = int(payload.get("user_id"))
        food_id = int(payload.get("food_id"))
        rating = int(payload.get("rating"))
    except (TypeError, ValueError):
        return jsonify({"error": "user_id, food_id, rating are required integers"}), 400

    comment = payload.get("comment", "")
    fb = Feedback(user_id=user_id, food_id=food_id, rating=rating, comment=comment)
    db.session.add(fb)
    db.session.commit()

    # Optional: in a background job, we could retrain/fine-tune using feedback
    return jsonify({"message": "feedback_recorded"}), 201


