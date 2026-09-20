import pytest

from app.services.nutrition import calculate_nutrition


def test_nutrition_is_deterministic():
    result = calculate_nutrition(21, "male", 183, 75, "moderate", "muscle_gain")

    assert result["bmr"] > 0
    assert result["tdee"] > result["bmr"]
    assert result["calorie_target"] > result["tdee"]
    assert result["protein_g"] > 0
    assert result["carbs_g"] >= 0
    assert result["fat_g"] > 0


def test_invalid_activity_is_rejected():
    with pytest.raises(ValueError):
        calculate_nutrition(21, "male", 183, 75, "unknown", "maintenance")


def test_invalid_gender_is_rejected():
    with pytest.raises(ValueError):
        calculate_nutrition(21, "unknown", 183, 75, "moderate", "maintenance")


def test_weight_loss_adjustment():
    maintenance = calculate_nutrition(
        21, "male", 183, 75, "moderate", "maintenance"
    )
    weight_loss = calculate_nutrition(
        21, "male", 183, 75, "moderate", "weight_loss"
    )

    assert weight_loss["calorie_target"] == maintenance["calorie_target"] - 400
