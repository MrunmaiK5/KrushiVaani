import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import json

def prepare_image_data(train_dir, test_dir, img_size=(128, 128), batch_size=32):
    """
    Prepares and preprocesses image data for the CNN model.
    Returns data generators and class name mapping.
    """
    print("Starting image preprocessing...")
    
    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        directory=train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        directory=train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    test_generator = test_datagen.flow_from_directory(
        directory=test_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    class_indices = train_generator.class_indices
    class_names = {v: k for k, v in class_indices.items()}
    
    print("Preprocessing complete.")
    return train_generator, validation_generator, test_generator, class_names

def save_class_mapping(class_mapping, filepath):
    """Saves the class mapping dictionary to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(class_mapping, f, indent=4)
    print(f"Class mapping saved to {filepath}")

if __name__ == '__main__':
    # This block is for testing the script independently
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    TRAIN_DIR = os.path.join(project_root, 'ml_models/disease_detection/data/train')
    TEST_DIR = os.path.join(project_root, 'ml_models/disease_detection/data/test')
    MAPPING_PATH = os.path.join(project_root, 'ml_models/disease_detection/data/class_mapping.json')

    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training directory not found at {TRAIN_DIR}")
    elif not os.path.exists(TEST_DIR):
        print(f"Error: Testing directory not found at {TEST_DIR}")
    else:
        train_gen, val_gen, test_gen, labels = prepare_image_data(TRAIN_DIR, TEST_DIR)
        save_class_mapping(labels, MAPPING_PATH)
        print("Class labels mapping:", labels)