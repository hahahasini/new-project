import os
import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path
import time

# =================================================================
# ACCURACY EVALUATION CONFIGURATION
# =================================================================

class Config:
    # BASE_DIR is backend/metric_evaluation
    BASE_DIR = Path(__file__).resolve().parent.parent
    MODELS_DIR = BASE_DIR / "models"
    
    # Dataset is in the project root under 'final dataset/Test'
    DATASET_DIR = BASE_DIR.parent / "final dataset" / "Test"
    
    # Paths relative to MODELS_DIR
    MODELS = {
        "Nail": "nail/Nail_epoch_24.keras",
        "Tongue": "tongue/Tongue_epoch_01.keras",
        "Skin": "skin/skin_disease_model_epoch_46.keras"
    }
    
    # This order MUST match the classes the models were trained with
    # Based on app/config.py mappings
    DISEASE_MAPPING = {
        "Nail": ["No Disease", "Bluish nail", "aloperia areata"], 
        "Tongue": ["Diabetes", "Pale Tongue"],
        "Skin": ["Acne", "Carcinoma"]
    }
    
    IMG_SIZE = (224, 224)

# =================================================================
# HELPERS
# =================================================================

def load_and_preprocess_image(path):
    """Load image from disk and resize/normalize for model."""
    try:
        # Use cv2 to read as it handles various formats well
        img = cv2.imread(str(path))
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, Config.IMG_SIZE)
        img = img.astype(np.float32) / 255.0
        return np.expand_dims(img, axis=0)
    except Exception:
        return None

# =================================================================
# EVALUATION CORE
# =================================================================

def evaluate_model(name, relative_path):
    model_path = Config.MODELS_DIR / relative_path
    test_dir = Config.DATASET_DIR / name
    
    if not model_path.exists():
        print(f"\n[!] Model {name} not found at {model_path}")
        return None
    
    if not test_dir.exists():
        print(f"\n[!] Test directory {name} not found at {test_dir}")
        return None

    print(f"\n--> Starting Evaluation for {name} Model...")
    print(f"    Path: {relative_path}")
    
    try:
        model = tf.keras.models.load_model(str(model_path))
    except Exception as e:
        print(f"    [ERROR] Failed to load model: {e}")
        return None
    
    expected_classes = Config.DISEASE_MAPPING[name]
    results = {
        "total_correct": 0,
        "total_images": 0,
        "class_performance": {}
    }

    for class_idx, class_name in enumerate(expected_classes):
        # Flexible folder matching (case-insensitive)
        actual_folder = None
        for folder in test_dir.iterdir():
            if folder.is_dir() and folder.name.lower().replace(" ", "") == class_name.lower().replace(" ", ""):
                actual_folder = folder
                break
        
        if not actual_folder:
            print(f"    [WARNING] Folder for '{class_name}' not found. Skipping.")
            continue

        # Get all images in the folder
        image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
        image_paths = []
        for ext in image_extensions:
            image_paths.extend(list(actual_folder.glob(ext)))
            image_paths.extend(list(actual_folder.glob(ext.upper())))
        
        if not image_paths:
            continue

        print(f"    Processing class '{class_name}': {len(image_paths)} images found.")
        
        class_correct = 0
        class_total = 0
        
        for i, img_path in enumerate(image_paths):
            img_array = load_and_preprocess_image(img_path)
            if img_array is None:
                continue
            
            prediction = model.predict(img_array, verbose=0)
            pred_idx = np.argmax(prediction[0])
            
            class_total += 1
            if pred_idx == class_idx:
                class_correct += 1
            
            # Simple progress log every 10 images
            if (i + 1) % 10 == 0:
                print(f"      Progress: {i+1}/{len(image_paths)}...", end="\r")
        
        print(f"      Done. Accuracy for '{class_name}': {(class_correct/class_total*100):.2f}%")
        
        results["class_performance"][class_name] = {
            "correct": class_correct,
            "total": class_total,
            "acc": (class_correct/class_total*100)
        }
        results["total_correct"] += class_correct
        results["total_images"] += class_total

    # Cleanup memory
    del model
    tf.keras.backend.clear_session()
    
    if results["total_images"] > 0:
        results["overall_acc"] = (results["total_correct"] / results["total_images"]) * 100
    else:
        results["overall_acc"] = 0
        
    return results

def main():
    print("\n" + "="*70)
    print(f"{'VITAMIN DETECTION MODEL ACCURACY EVALUATOR':^70}")
    print("="*70)
    print(f"Date: {time.ctime()}")
    print(f"Test Dataset: {Config.DATASET_DIR}")
    print("="*70 + "\n")
    
    final_stats = {}
    for name, path in Config.MODELS.items():
        stats = evaluate_model(name, path)
        if stats:
            final_stats[name] = stats
    
    # Final Summary Table
    print("\n\n" + "="*70)
    print(f"{'FINAL ACCURACY SUMMARY':^70}")
    print("="*70)
    print(f"{'Model Name':<15} | {'Images':<10} | {'Correct':<10} | {'Accuracy':<15}")
    print("-" * 70)
    
    for name, stats in final_stats.items():
        print(f"{name:<15} | {stats['total_images']:<10} | {stats['total_correct']:<10} | {stats['overall_acc']:>8.2f}%")
    
    print("="*70)
    print("\nDetailed breakdown per class:\n")
    for name, stats in final_stats.items():
        print(f"[{name} Model]")
        for cls_name, cls_stats in stats["class_performance"].items():
            print(f"  - {cls_name:<15}: {cls_stats['acc']:>6.2f}% ({cls_stats['correct']}/{cls_stats['total']})")
        print("-" * 40)

if __name__ == "__main__":
    main()
