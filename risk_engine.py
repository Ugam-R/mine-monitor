import math


def calculate_risk(data):
    """
    Prototype risk engine.

    IMPORTANT:
    This is a rule-based prototype, not a validated
    mine-safety prediction model.
    """

    score = 0

    # -------------------------
    # FSR / Load indicator
    # -------------------------
    force = data["force_raw"]

    if force > 800:
        score += 30
    elif force > 500:
        score += 20
    elif force > 250:
        score += 10

    # -------------------------
    # Flex / deformation
    # -------------------------
    flex = data["flex_raw"]

    # Current prototype baseline is around ~675.
    # Large deviation from baseline is treated as deformation.
    flex_deviation = abs(flex - 675)

    if flex_deviation > 200:
        score += 25
    elif flex_deviation > 100:
        score += 15
    elif flex_deviation > 50:
        score += 5

    # -------------------------
    # Moisture / seepage proxy
    # -------------------------
    moisture = data["moisture_raw"]

    if moisture < 700:
        score += 20
    elif moisture < 850:
        score += 10

    # -------------------------
    # Accelerometer movement
    # -------------------------
    x = data["accel_x"]
    y = data["accel_y"]
    z = data["accel_z"]

    magnitude = math.sqrt(x*x + y*y + z*z)

    # Prototype baseline is approximately 620.
    acceleration_change = abs(magnitude - 620)

    if acceleration_change > 80:
        score += 20
    elif acceleration_change > 40:
        score += 10

    # -------------------------
    # Roof convergence proxy
    # -------------------------
    distance = data["roof_distance_cm"]

    if distance >= 0:
        if distance < 50:
            score += 25
        elif distance < 100:
            score += 10

    # -------------------------
    # Limit score
    # -------------------------
    score = min(score, 100)

    # -------------------------
    # Risk level
    # -------------------------
    if score >= 75:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level
