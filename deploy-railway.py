"""
Script untuk deploy ke Railway dengan opsi yang berbeda
"""

import os
import shutil

def show_deployment_options():
    print("🚀 PILIHAN DEPLOYMENT RAILWAY")
    print("=" * 50)
    
    print("\n📋 OPSI DEPLOYMENT:")
    
    print("\n1️⃣ FIXED TENSORFLOW (Recommended)")
    print("   Files:")
    print("   - requirements-railway.txt (TensorFlow 2.12.0)")
    print("   - app-optimized.py")
    print("   - Dockerfile.railway")
    print("   - railway-fixed.toml")
    print("   Ukuran: ~300MB")
    print("   Status: ✅ Dependencies fixed")
    
    print("\n2️⃣ MINIMAL NO-TF (Fallback)")
    print("   Files:")
    print("   - requirements-minimal.txt (tanpa TensorFlow)")
    print("   - app-no-tf.py")
    print("   - Dockerfile.minimal")
    print("   Ukuran: ~50MB")
    print("   Status: ⚠️ Prediksi sederhana")
    
    print("\n3️⃣ ORIGINAL FIXED")
    print("   Files:")
    print("   - requirements.txt (updated)")
    print("   - app.py (original)")
    print("   - Procfile")
    print("   Ukuran: ~250MB")
    print("   Status: ✅ Tanpa Docker")

def prepare_deployment(option):
    if option == "1":
        print("\n🔧 Mempersiapkan FIXED TENSORFLOW deployment...")
        
        # Copy files untuk deployment
        shutil.copy("requirements-railway.txt", "requirements.txt")
        shutil.copy("app-optimized.py", "app.py")
        shutil.copy("Dockerfile.railway", "Dockerfile")
        shutil.copy("railway-fixed.toml", "railway.toml")
        
        print("✅ Files siap untuk deployment!")
        print("\n📦 Command deployment:")
        print("   railway up")
        
    elif option == "2":
        print("\n🔧 Mempersiapkan MINIMAL NO-TF deployment...")
        
        # Copy files untuk deployment
        shutil.copy("requirements-minimal.txt", "requirements.txt")
        shutil.copy("app-no-tf.py", "app.py")
        shutil.copy("Dockerfile.minimal", "Dockerfile")
        
        print("✅ Files siap untuk deployment!")
        print("\n📦 Command deployment:")
        print("   railway up")
        
    elif option == "3":
        print("\n🔧 Mempersiapkan ORIGINAL FIXED deployment...")
        
        # requirements.txt sudah diupdate sebelumnya
        print("✅ Files siap untuk deployment!")
        print("\n📦 Command deployment:")
        print("   railway up")
        
    else:
        print("❌ Opsi tidak valid!")

if __name__ == "__main__":
    show_deployment_options()
    
    print("\n🎯 REKOMENDASI:")
    print("   1. Coba FIXED TENSORFLOW dulu (opsi 1)")
    print("   2. Jika masih error, gunakan MINIMAL NO-TF (opsi 2)")
    print("   3. Atau gunakan ORIGINAL FIXED (opsi 3)")
    
    choice = input("\nPilih opsi deployment (1/2/3): ").strip()
    
    if choice in ["1", "2", "3"]:
        prepare_deployment(choice)
    else:
        print("❌ Pilihan tidak valid!")
