from typing import Dict, Tuple, Optional


def validate_user_payload(payload: Dict) -> Tuple[bool, Optional[str]]:
    required_fields = [
        "name",
        "age",
        "gender",
        "height_cm",
        "weight_kg",
        "activity_level",
        "goal",
    ]
    for field in required_fields:
        if field not in payload:
            return False, f"Missing field: {field}"

    try:
        age = int(payload["age"])
        height = float(payload["height_cm"])
        weight = float(payload["weight_kg"])
    except (ValueError, TypeError):
        return False, "age, height_cm, weight_kg must be numeric"

    if not (0 < age < 120):
        return False, "age must be between 1 and 119"
    if not (50 < height < 250):
        return False, "height_cm must be between 50 and 250"
    if not (10 < weight < 400):
        return False, "weight_kg must be between 10 and 400"

    if payload.get("gender") not in {"male", "female", "other"}:
        return False, "gender must be one of: male, female, other"

    if payload.get("activity_level") not in {"sedentary", "light", "moderate", "active", "very_active"}:
        return False, "invalid activity_level"

    if payload.get("goal") not in {"weight_loss", "maintenance", "muscle_gain"}:
        return False, "invalid goal"

    return True, None


