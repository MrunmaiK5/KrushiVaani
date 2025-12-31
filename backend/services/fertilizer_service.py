import pandas as pd
import os

def recommend_fertilizer(input_data: dict) -> dict:
    """
    Hybrid Recommendation: Calculates nutrient gaps based on 
    crop-specific data from your CSV and suggests supplements.
    """
    try:
        # 1. Robust Absolute Path Resolution
        # Gets the absolute path to backend/services/
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        
        # Navigates up to KrushiVaani/ root and then into ml_models/fertilizer/
        data_path = os.path.abspath(os.path.join(
            BASE_DIR, "..", "..", "ml_models", "fertilizer", "fertilizer.csv"
        ))
        
        # Debug print to verify path resolution in terminal
        print(f"DEBUG: Attempting to load Fertilizer CSV from: {data_path}")
        
        if not os.path.exists(data_path):
            return {
                "status": "failed",
                "error": f"Fertilizer CSV not found at: {data_path}. Please verify folder structure."
            }
            
        df = pd.read_csv(data_path)

        # 2. Extract inputs with default values to prevent crashes
        current_n = float(input_data.get("N", 0))
        current_p = float(input_data.get("P", 0))
        current_k = float(input_data.get("K", 0))
        ph = float(input_data.get("ph", 7.0))
        crop_name = input_data.get("crop", "").lower()

        # 3. Find ideal NPK for this crop (Matches CSV 'Crop' column)
        crop_data = df[df['Crop'].str.lower() == crop_name]
        
        if crop_data.empty:
            # General defaults if crop is not found in CSV
            ideal_n, ideal_p, ideal_k, target_ph = 50, 50, 50, 6.5
        else:
            # Using column names exactly as they appear in your CSV: Crop, N, P, K, pH
            ideal_n = float(crop_data['N'].iloc[0])
            ideal_p = float(crop_data['P'].iloc[0])
            ideal_k = float(crop_data['K'].iloc[0])
            target_ph = float(crop_data['pH'].iloc[0])

        recommendations = []
        
        # 4. Nutrient Gap Analysis
        n_gap = ideal_n - current_n
        p_gap = ideal_p - current_p
        k_gap = ideal_k - current_k

        if n_gap > 10:
            recommendations.append(f"Nitrogen is low (Gap: {int(n_gap)}). Apply Urea.")
        if p_gap > 10:
            recommendations.append(f"Phosphorus is low (Gap: {int(p_gap)}). Apply DAP.")
        if k_gap > 10:
            recommendations.append(f"Potassium is low (Gap: {int(k_gap)}). Apply Muriate of Potash (MOP).")

        # 5. pH Check
        if ph < (target_ph - 0.5):
            recommendations.append(f"Soil is acidic (Target: {target_ph}). Apply Lime.")
        elif ph > (target_ph + 0.5):
            recommendations.append(f"Soil is alkaline (Target: {target_ph}). Apply Gypsum.")

        return {
            "crop": crop_name,
            "status": "success",
            "ideal_npk": {"N": ideal_n, "P": ideal_p, "K": ideal_k},
            "recommendations": recommendations if recommendations else ["Soil nutrients are optimal for this crop!"]
        }
    except Exception as e:
        return {"error": f"Internal Logic Error: {str(e)}", "status": "failed"}