# 🚀 Deployment Guide - Railway Optimization

## Masalah yang Diperbaiki
- ❌ Image Docker terlalu besar (500MB+)
- ❌ Error deployment di Railway
- ❌ Memory usage tinggi
- ❌ Build time lama

## ✅ Solusi yang Diterapkan

### 1. Multi-stage Docker Build
- Menggunakan `python:3.11-slim` sebagai base image
- Build stage terpisah untuk dependencies
- Production stage yang minimal

### 2. Optimasi Dependencies
- Menggunakan `tensorflow-cpu` (lebih kecil dari tensorflow)
- Versi yang kompatibel dan stabil
- Menghilangkan dependencies yang tidak perlu

### 3. Memory Optimization
- Disable eager execution di TensorFlow
- Force CPU usage untuk Railway
- Garbage collection setelah prediksi
- Memory growth untuk GPU

### 4. Production Configuration
- Gunicorn dengan workers optimal
- Health check endpoint
- Proper error handling
- Environment variables

## 📋 Langkah Deployment

### Opsi 1: Railway dengan Dockerfile (Recommended)

1. **Siapkan file yang diperlukan:**
   ```bash
   # File yang sudah dibuat:
   - Dockerfile
   - requirements-optimized.txt
   - .dockerignore
   - railway.toml
   - app-optimized.py
   ```

2. **Deploy ke Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login dan deploy
   railway login
   railway init
   railway up
   ```

### Opsi 2: Railway dengan GitHub Integration

1. **Push ke GitHub repository**
2. **Connect repository ke Railway**
3. **Railway akan auto-detect Dockerfile**

### Opsi 3: Manual Build & Push

```bash
# Build image
docker build -t your-app-name .

# Tag untuk registry
docker tag your-app-name your-registry/your-app-name

# Push ke registry
docker push your-registry/your-app-name
```

## 🔧 Konfigurasi Railway

### Environment Variables
```env
FLASK_ENV=production
PYTHONUNBUFFERED=1
TF_CPP_MIN_LOG_LEVEL=3
PORT=5000
```

### Resource Limits
- Memory: 1GB (Railway default)
- CPU: Shared
- Build timeout: 300s

## 📊 Expected Results

### Before Optimization
- Image size: ~500MB
- Build time: ~10-15 minutes
- Memory usage: ~800MB
- Deploy success: ❌

### After Optimization
- Image size: ~200-300MB
- Build time: ~5-8 minutes
- Memory usage: ~400-600MB
- Deploy success: ✅

## 🛠️ Troubleshooting

### Jika masih error:

1. **Check build logs:**
   ```bash
   railway logs
   ```

2. **Reduce model size:**
   ```bash
   python optimize_model.py
   ```

3. **Use smaller base image:**
   ```dockerfile
   FROM python:3.11-alpine
   ```

4. **Remove static files yang tidak perlu:**
   ```bash
   # Hapus file PNG yang besar dari static/
   rm static/*.png
   ```

### Common Issues:

- **Out of memory:** Reduce workers di gunicorn
- **Build timeout:** Gunakan cache layer yang lebih baik
- **Model loading error:** Check model file path

## 🎯 Tips Tambahan

1. **Gunakan model quantization** untuk mengurangi ukuran lebih lanjut
2. **Implement caching** untuk prediksi yang sering digunakan
3. **Monitor memory usage** dengan Railway metrics
4. **Use CDN** untuk static files jika diperlukan

## 📞 Support

Jika masih mengalami masalah, check:
1. Railway build logs
2. Application logs
3. Memory usage metrics
4. Network connectivity
