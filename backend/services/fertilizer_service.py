fertilizer_dict = {
    "rice": ["Urea", "DAP"], "maize": ["Urea", "MOP"], "wheat": ["Urea", "DAP", "Potash"],
    "cotton": ["Urea", "Potash"], "sugarcane": ["NPK 20:10:10", "Urea"],
    "ground nuts": ["Urea", "Compost"], # Add more as needed
}

def recommend_fertilizer(input_data: dict) -> dict:
    """Rule-based fertilizer recommendation."""
    N = float(input_data["N"])
    P = float(input_data["P"])
    K = float(input_data["K"])
    ph = float(input_data["ph"])
    crop = input_data.get("crop", "").lower() # Uses the 'crop' key now, not 'Crop'

    fertilizers = fertilizer_dict.get(crop, ["General Purpose NPK", "Compost"])

    notes = []
    if N < 50: notes.append("Nitrogen (N) is low. Consider Urea.")
    if P < 40: notes.append("Phosphorus (P) is low. Consider DAP.")
    if K < 40: notes.append("Potassium (K) is low. Consider MOP (Potash).")
    if ph < 5.5: notes.append("Soil is acidic. Consider applying lime.")
    if ph > 7.5: notes.append("Soil is alkaline. Consider applying gypsum.")

    return {"recommended_fertilizers": fertilizers, "notes": notes}