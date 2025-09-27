# ml_models/personalization/personalization_logic.py

def get_personalized_tip(query_history):
    """
    Analyzes a user's query history and returns a personalized tip.
    
    Args:
        query_history (list): A list of dictionaries, where each dictionary
                              is a past query from the user.
                              
    Returns:
        str: A personalized tip or a default message.
    """
    
    # --- Rule 1: Check for recurring low nitrogen ---
    # Find all queries where the user's Nitrogen input was low (e.g., < 40)
    low_nitrogen_queries = [
        query for query in query_history 
        if 'input_data' in query and query['input_data'].get('N', 100) < 40
    ]
    
    if len(low_nitrogen_queries) >= 2:
        return ("🌱 Tip: We've noticed your soil often seems low in Nitrogen. "
                "Consider regular use of compost or Urea to improve soil health.")

    # --- Rule 2: Check for recurring crop recommendations ---
    # Find how many times 'rice' has been recommended
    rice_recommendations = [
        query for query in query_history
        if 'result_data' in query and query['result_data'].get('predicted_crop') == 'rice'
    ]
    
    if len(rice_recommendations) >= 2:
        return ("🌱 Tip: Growing rice repeatedly can deplete specific nutrients. "
                "Ensure you are using a balanced fertilizer for each season.")
                
    # --- Add more rules here in the future ---
    
    # --- Default Message ---
    # If no other rules match, return a general tip
    return "🌱 Tip: Remember to rotate your crops each season to maintain healthy soil and prevent diseases."


# --- This is your test area ---
if __name__ == "__main__":
    
    # Create your own "dummy" history data for testing
    # This is a fake history for a user who often has low Nitrogen
    dummy_history_for_testing = [
        {
            "query_type": "hybrid", 
            "input_data": {"N": 30, "P": 50, "K": 50, "temperature": 25},
            "result_data": {"predicted_crop": "lentil"}
        },
        {
            "query_type": "fertilizer", 
            "input_data": {"N": 25, "P": 60, "K": 45, "Crop": "lentil"},
            "result_data": {"recommended_fertilizers": ["Urea", "DAP"]}
        },
        {
            "query_type": "hybrid", 
            "input_data": {"N": 35, "P": 55, "K": 50, "temperature": 26},
            "result_data": {"predicted_crop": "maize"}
        }
    ]
    
    # Call your function with the dummy data
    tip = get_personalized_tip(dummy_history_for_testing)
    
    # Print the result to see if your logic works
    print(f"Generated Tip: {tip}")