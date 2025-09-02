def recommend_fertilizer(data: dict):
    n = data.get("n", 0)
    p = data.get("p", 0)
    k = data.get("k", 0)

    if n < 50:
        return "Add Nitrogen fertilizer"
    elif p < 30:
        return "Add Phosphorus fertilizer"
    elif k < 20:
        return "Add Potassium fertilizer"
    else:
        return "Soil is balanced"
