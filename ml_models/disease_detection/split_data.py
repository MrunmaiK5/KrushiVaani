import os
import shutil
from sklearn.model_selection import train_test_split

# --- Configuration ---
# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct path to the directory containing the actual disease classes
RAW_DATA_PATH = os.path.join(script_dir, 'data', 'raw', 'dd_dataset', 'PlantVillage')

# Paths for the new organized train, validate, and test folders
TRAIN_PATH = os.path.join(script_dir, 'data', 'train')
VALIDATE_PATH = os.path.join(script_dir, 'data', 'validate')
TEST_PATH = os.path.join(script_dir, 'data', 'test')

# Define the split ratios (e.g., 70% train, 15% validation, 15% test)
TRAIN_RATIO = 0.70
VALIDATE_RATIO = 0.15
# The remaining 15% will be for the test set

def organize_dataset():
    """
    Splits the raw dataset into training, validation, and testing directories.
    """
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: The expected raw data folder not found at '{RAW_DATA_PATH}'")
        return

    # Create the directories, removing old ones first
    for path in [TRAIN_PATH, VALIDATE_PATH, TEST_PATH]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    disease_classes = [d for d in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, d))]
    
    if not disease_classes:
        print(f"Error: No class folders found in '{RAW_DATA_PATH}'.")
        return

    print("Processing disease classes...")
    for cls in disease_classes:
        # Create class subdirectories in all sets
        os.makedirs(os.path.join(TRAIN_PATH, cls), exist_ok=True)
        os.makedirs(os.path.join(VALIDATE_PATH, cls), exist_ok=True)
        os.makedirs(os.path.join(TEST_PATH, cls), exist_ok=True)
        
        # Get all images for the current class
        all_images = [f for f in os.listdir(os.path.join(RAW_DATA_PATH, cls)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Check if the list of images is empty before splitting
        if not all_images:
            print(f"  - WARNING: No images found for class '{cls}'. Skipping.")
            continue # Move to the next class
            
        # 1. First split: Separate the training set from the rest
        train_images, remaining_images = train_test_split(
            all_images,
            train_size=TRAIN_RATIO,
            random_state=42
        )
        
        # 2. Second split: Split the remainder into validation and testing sets
        relative_test_size = 0.5 # 50% of the remaining 30% gives 15% for test
        
        validate_images, test_images = train_test_split(
            remaining_images,
            test_size=relative_test_size,
            random_state=42
        )

        # Function to copy files to a destination folder
        def copy_files(file_list, dest_folder):
            for img_name in file_list:
                source_path = os.path.join(RAW_DATA_PATH, cls, img_name)
                dest_path = os.path.join(dest_folder, cls, img_name)
                shutil.copy(source_path, dest_path)

        # Copy files to their respective directories
        copy_files(train_images, TRAIN_PATH)
        copy_files(validate_images, VALIDATE_PATH)
        copy_files(test_images, TEST_PATH)

        print(f"- Class '{cls}': {len(train_images)} train, {len(validate_images)} validate, {len(test_images)} test")

    print("\nDataset organization complete!")

if __name__ == '__main__':
    organize_dataset()