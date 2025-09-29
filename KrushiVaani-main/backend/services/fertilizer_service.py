# backend/services/fertilizer_service.py

# Dictionary mapping crop -> fertilizer recommendations
fertilizer_dict = {
    "rice": ["Urea", "DAP"], "maize": ["Urea", "MOP"], "wheat": ["Urea", "DAP", "Potash"],
    "cotton": ["Urea", "Potash"], "sugarcane": ["NPK 20:10:10", "Urea"], "banana": ["Urea", "Compost"],
    "mango": ["Compost", "Potash"], "pomegranate": ["Potash", "Compost"],
}


def recommend_fertilizer(input_data: dict):
    """Rule-based fertilizer recommendation"""
    required_fields = ["N", "P", "K", "ph", "soil_moisture", "Crop"]
    for f in required_fields:
        if f not in input_data or input_data[f] is None:
            raise ValueError(f"Missing required field: {f}")

    N, P, K, ph, moisture = float(input_data["N"]), float(input_data["P"]), float(input_data["K"]), float(
        input_data["ph"]), float(input_data["soil_moisture"])
    crop = input_data.get("Crop")

    fertilizers = fertilizer_dict.get(str(crop).lower(), ["General Compost"])

    notes = []
    if N < 50: notes.append("Nitrogen low → consider Urea or organic N sources.")
    if P < 40: notes.append("Phosphorus low → consider DAP or bone meal.")
    if K < 40: notes.append("Potassium low → consider MOP (potash).")
    if ph < 5.5: notes.append("Soil acidic → apply lime (after soil test).")
    if ph > 7.5: notes.append("Soil alkaline → consider gypsum.")
    if moisture < 30: notes.append("Soil moisture low → irrigate before applying certain fertilizers.")

    return {"recommended_fertilizers": fertilizers, "notes": notes}