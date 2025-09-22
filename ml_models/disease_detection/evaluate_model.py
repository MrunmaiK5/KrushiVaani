import tensorflow as tf
import os
import sys

# Add the parent directory to the system path to import from utils
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
sys.path.append(os.path.join(project_root, 'backend', 'utils'))

from preprocessing import prepare_image_data

# --- Configuration ---
# Define paths relative to the project root
TRAIN_DIR = os.path.join(project_root, 'ml_models', 'disease_detection', 'data', 'train')
TEST_DIR = os.path.join(project_root, 'ml_models', 'disease_detection', 'data', 'test')
MODEL_PATH = os.path.join(script_dir, 'disease_cnn.h5')

# --- Load the Trained Model ---
if not os.path.exists(MODEL_PATH):
    print(f"Error: Model not found at '{MODEL_PATH}'. Please train the model first.")
else:
    print("Loading the trained model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")

    # --- Data Preparation ---
    # Prepare the data, but we will only use the test_generator for evaluation
    train_generator, validation_generator, test_generator, class_names = prepare_image_data(TRAIN_DIR, TEST_DIR)

    # --- Model Evaluation ---
    print("\nEvaluating the model on the test data...")
    # The evaluate function returns the loss and the metrics you compiled the model with
    loss, accuracy = model.evaluate(test_generator, verbose=1)

    print("\n--- Model Performance ---")
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy:.4f}")