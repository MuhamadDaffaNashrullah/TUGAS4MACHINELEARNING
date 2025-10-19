"""
Script untuk mengoptimasi model TensorFlow untuk deployment
Menjalankan script ini akan membuat model yang lebih kecil dan efisien
"""

import os
import tensorflow as tf
from tensorflow import keras
import h5py

def optimize_model():
    """Optimasi model untuk mengurangi ukuran file"""
    
    model_path = 'lstm_btc_daily_model.h5'
    optimized_path = 'lstm_btc_daily_model_optimized.h5'
    
    if not os.path.exists(model_path):
        print(f"❌ Model file {model_path} tidak ditemukan!")
        return
    
    try:
        # Load model asli
        print("📥 Loading model...")
        model = keras.models.load_model(model_path, compile=False)
        
        # Convert ke SavedModel format (lebih efisien)
        saved_model_path = 'model_saved_tf'
        print("💾 Converting to SavedModel format...")
        model.save(saved_model_path, save_format='tf')
        
        # Load kembali dan save dengan optimasi
        print("🔄 Re-loading and optimizing...")
        model_optimized = keras.models.load_model(saved_model_path, compile=False)
        
        # Save dengan kompresi
        model_optimized.save(optimized_path, save_format='h5')
        
        # Ukuran file comparison
        original_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        optimized_size = os.path.getsize(optimized_path) / (1024 * 1024)  # MB
        saved_model_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                              for dirpath, dirnames, filenames in os.walk(saved_model_path)
                              for filename in filenames) / (1024 * 1024)  # MB
        
        print(f"\n📊 Size comparison:")
        print(f"   Original H5: {original_size:.2f} MB")
        print(f"   Optimized H5: {optimized_size:.2f} MB")
        print(f"   SavedModel: {saved_model_size:.2f} MB")
        print(f"   Reduction: {((original_size - optimized_size) / original_size * 100):.1f}%")
        
        print(f"\n✅ Model optimization completed!")
        print(f"   Use '{optimized_path}' for deployment")
        
    except Exception as e:
        print(f"❌ Error optimizing model: {e}")

if __name__ == "__main__":
    optimize_model()
