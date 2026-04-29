import os
import time
import psutil
import numpy as np
import tensorflow as tf
from pathlib import Path

# =================================================================
# BENCHMARK CONFIGURATION
# =================================================================

class Config:
    # BASE_DIR is backend/metric_evaluation
    # MODELS_DIR is backend/models
    BASE_DIR = Path(__file__).resolve().parent.parent
    MODELS_DIR = BASE_DIR / "models"
    
    # Paths relative to MODELS_DIR
    MODELS = {
        "Nail": "nail/Nail_epoch_24.keras",
        "Tongue": "tongue/Tongue_epoch_01.keras",
        "Skin": "skin/skin_disease_model_epoch_46.keras"
    }
    
    DEFAULT_IMG_SIZE = (224, 224)
    INFERENCE_ITERATIONS = 10

# =================================================================
# HELPERS
# =================================================================

def get_process_memory():
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def format_size(size_mb):
    return f"{size_mb:.2f} MB"

def format_time(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    return f"{seconds:.2f} s"

# =================================================================
# BENCHMARK CORE
# =================================================================

def benchmark_model(name, relative_path):
    model_path = Config.MODELS_DIR / relative_path
    
    if not model_path.exists():
        return {
            "name": name,
            "status": "[NOT FOUND]",
            "file_size": "N/A",
            "ram_delta": "N/A",
            "load_time": "N/A",
            "avg_latency": "N/A"
        }

    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    
    print(f"--> Loading {name} model ({format_size(file_size_mb)})...")
    
    # Baseline memory
    mem_before = get_process_memory()
    
    # Load Timing
    start_load = time.time()
    try:
        # Load model
        model = tf.keras.models.load_model(str(model_path))
        load_duration = time.time() - start_load
        
        # Memory after load
        mem_after = get_process_memory()
        ram_delta = mem_after - mem_before
        
        # Inference Timing
        print(f"    Running {Config.INFERENCE_ITERATIONS} inference iterations...")
        dummy_input = np.random.rand(1, *Config.DEFAULT_IMG_SIZE, 3).astype(np.float32)
        
        # Warm up
        model.predict(dummy_input, verbose=0)
        
        # Actual benchmark
        start_inf = time.time()
        for _ in range(Config.INFERENCE_ITERATIONS):
            model.predict(dummy_input, verbose=0)
        total_inf_time = time.time() - start_inf
        avg_latency = total_inf_time / Config.INFERENCE_ITERATIONS
        
        # Cleanup
        del model
        tf.keras.backend.clear_session()
        
        return {
            "name": name,
            "status": "[OK]",
            "file_size": format_size(file_size_mb),
            "ram_delta": format_size(ram_delta),
            "load_time": format_time(load_duration),
            "avg_latency": format_time(avg_latency)
        }
        
    except Exception as e:
        return {
            "name": name,
            "status": f"[ERROR]",
            "file_size": format_size(file_size_mb),
            "ram_delta": "N/A",
            "load_time": "N/A",
            "avg_latency": "N/A"
        }

def main():
    print("\n" + "="*80)
    print(f"{'MODEL PERFORMANCE BENCHMARK':^80}")
    print("="*80)
    print(f"Date: {time.ctime()}")
    print(f"TF Version: {tf.__version__}")
    print("="*80 + "\n")
    
    results = []
    for name, path in Config.MODELS.items():
        res = benchmark_model(name, path)
        results.append(res)
    
    # Final Table
    print("\n" + "="*95)
    print(f"{'Model':<12} | {'Status':<15} | {'Disk Size':<12} | {'RAM Usage':<12} | {'Load Time':<12} | {'Avg Latency':<12}")
    print("-" * 95)
    for r in results:
        print(f"{r['name']:<12} | {r['status']:<15} | {r['file_size']:<12} | {r['ram_delta']:<12} | {r['load_time']:<12} | {r['avg_latency']:<12}")
    print("="*95)
    print("* RAM Usage is the approximate delta in RSS after loading.")
    print("* Avg Latency is measured over 10 iterations after 1 warm-up run.\n")

if __name__ == "__main__":
    main()
