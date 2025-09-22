import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os
import sys

# Add the parent directory to the system path to import from utils
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
sys.path.append(os.path.join(project_root, 'backend', 'utils'))

from preprocessing import prepare_image_data, save_class_mapping

# --- Configuration ---
# Define paths relative to the project root
TRAIN_DIR = os.path.join(project_root, 'ml_models', 'disease_detection', 'data', 'train')
TEST_DIR = os.path.join(project_root, 'ml_models', 'disease_detection', 'data', 'test')
MODEL_PATH = os.path.join(script_dir, 'disease_cnn.h5')
MAPPING_PATH = os.path.join(script_dir, 'data', 'class_mapping.json') 

# --- Data Preparation ---
# This re-uses your preprocessing script
train_generator, validation_generator, test_generator, class_names = prepare_image_data(TRAIN_DIR, TEST_DIR)

# Save the class mapping for later use
save_class_mapping(class_names, MAPPING_PATH)

# --- Model Architecture ---
# The CNN model based on your initial plan
model = Sequential([
    # Input layer with 128x128 images and 3 color channels
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5), # Regularization to prevent overfitting
    Dense(len(class_names), activation='softmax') # Output layer for multi-class classification
])

# --- Model Compilation ---
# Using the Adam optimizer and categorical cross-entropy loss for multi-class problems
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# --- Model Training ---
print("\nStarting model training...")
# Train the model using the data generators
history = model.fit(
    train_generator,
    epochs=10, # Number of times to iterate over the dataset
    validation_data=validation_generator
)

# --- Save the Trained Model ---
print("\nTraining complete. Saving model...")
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")