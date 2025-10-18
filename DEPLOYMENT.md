# Deployment Guide

## Common Issues and Solutions

### 1. "No builders available in region" Error
This usually happens on Railway when the platform can't find a suitable builder. Solutions:

**Option A: Use Dockerfile (Recommended)**
- The `railway.json` is configured to use Dockerfile
- Make sure your Dockerfile is in the root directory
- Ensure all required files are present

**Option B: Use Nixpacks (Alternative)**
- Delete `railway.json` to let Railway auto-detect
- Railway will use Nixpacks builder instead

### 2. Build Failures
Common causes and fixes:

**Memory Issues:**
- Add `--memory=4g` to Docker build if building locally
- Railway should handle this automatically

**Missing Dependencies:**
- Check that all files are in the repository
- Ensure `lstm_btc_daily_model.h5` and `scaler_minmax.joblib` are committed

**Python Version Issues:**
- The Dockerfile uses Python 3.11
- Make sure your local Python version matches

### 3. Runtime Errors
**Model Loading Issues:**
- Check that model files are in the correct location
- Verify file permissions
- Check the logs for specific error messages

## Deployment Steps

### For Railway:
1. Push code to GitHub
2. Connect repository to Railway
3. Railway will auto-detect the configuration
4. Monitor the build logs for any errors

### For Heroku:
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`

### For Docker (Local Testing):
```bash
# Build the image
docker build -t btc-predictor .

# Run the container
docker run -p 5000:5000 btc-predictor
```

## Troubleshooting Commands

```bash
# Check if all files are present
ls -la

# Test the app locally
python app.py

# Check requirements
pip install -r requirements.txt
```

## File Structure Required:
```
├── app.py
├── requirements.txt
├── Dockerfile
├── railway.json
├── Procfile
├── lstm_btc_daily_model.h5
├── scaler_minmax.joblib
├── templates/
│   └── index.html
└── static/
    └── (your image files)
```
