"""
Script untuk membandingkan ukuran package yang berbeda
"""

import subprocess
import sys

def check_package_size(package_name):
    """Check ukuran package dengan pip show"""
    try:
        result = subprocess.run(['pip', 'show', package_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('Location:'):
                    location = line.split(':', 1)[1].strip()
                    # Coba hitung ukuran (aproximasi)
                    return f"Package found at: {location}"
        return "Package not found"
    except:
        return "Error checking package"

def compare_requirements():
    """Bandingkan ukuran requirements yang berbeda"""
    
    print("🔍 Analisis Ukuran Package untuk Deployment")
    print("=" * 50)
    
    # Versi original (berat)
    print("\n📦 VERSI ORIGINAL (Berat):")
    original_packages = [
        "tensorflow==2.16.1",
        "numpy>=1.23.0",
        "scikit-learn>=1.3.0"
    ]
    
    for package in original_packages:
        print(f"  {package}")
    
    print("\n📦 VERSI OPTIMIZED (Ringan):")
    optimized_packages = [
        "tensorflow-cpu==2.10.1",
        "numpy==1.21.6", 
        "scikit-learn==1.1.3"
    ]
    
    for package in optimized_packages:
        print(f"  {package}")
    
    print("\n📦 VERSI ULTRA-LIGHT (Paling Ringan):")
    ultra_light_packages = [
        "tensorflow-cpu==2.9.3",
        "numpy==1.21.6",
        "scikit-learn==1.1.3"
    ]
    
    for package in ultra_light_packages:
        print(f"  {package}")
    
    print("\n💡 REKOMENDASI:")
    print("  1. Gunakan requirements-ultra-light.txt untuk deployment Railway")
    print("  2. Gunakan Dockerfile.ultra-light untuk build yang paling kecil")
    print("  3. Gunakan app-ultra-light.py untuk aplikasi yang dioptimasi")
    
    print("\n📊 ESTIMASI UKURAN:")
    print("  Original:     ~500MB")
    print("  Optimized:    ~300MB") 
    print("  Ultra-light:  ~200MB")

if __name__ == "__main__":
    compare_requirements()
