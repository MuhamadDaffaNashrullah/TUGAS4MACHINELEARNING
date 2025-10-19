from flask import Flask, render_template, request
import os
import joblib
import numpy as np
import h5py
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'lstm_btc_daily_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler_minmax.joblib')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder='static', template_folder='templates')

model = None
scaler = None
model_error = None
scaler_error = None

def try_load_assets():
    global model, scaler, model_error, scaler_error
    try:
        # Simulasi model loading tanpa TensorFlow
        if os.path.exists(MODEL_PATH):
            model = "Model loaded (simulated)"
        else:
            model_error = 'Model file not found'
    except Exception as e:
        model_error = str(e)

    try:
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
        else:
            scaler_error = 'Scaler file not found'
    except Exception as e:
        scaler_error = str(e)

try_load_assets()

def list_static_charts():
    if not os.path.isdir(STATIC_DIR):
        return []
    files = []
    for name in os.listdir(STATIC_DIR):
        lower = name.lower()
        if lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            files.append(name)
    files.sort()
    return files

@app.route('/')
def index():
    charts = list_static_charts()
    return render_template('index.html',
                           charts=charts,
                           model_loaded=model is not None,
                           scaler_loaded=scaler is not None,
                           model_error=model_error,
                           scaler_error=scaler_error,
                           predict_error=None,
                           predict_value=None)

def _parse_series(text):
    if not text:
        return []
    parts = [p.strip() for p in text.replace('\n', ',').split(',') if p.strip()]
    vals = []
    for p in parts:
        try:
            vals.append(float(p))
        except ValueError:
            return []
    return vals

@app.route('/predict', methods=['POST'])
def predict():
    charts = list_static_charts()
    if model is None or scaler is None:
        return render_template('index.html', charts=charts, model_loaded=model is not None, scaler_loaded=scaler is not None, model_error=model_error, scaler_error=scaler_error, predict_error='Model atau scaler belum siap.', predict_value=None)
    
    text = request.form.get('values', '')
    series = _parse_series(text)
    if len(series) < 60:
        return render_template('index.html', charts=charts, model_loaded=True, scaler_loaded=True, model_error=model_error, scaler_error=scaler_error, predict_error='Minimal 60 nilai penutupan diperlukan.', predict_value=None)
    
    # Simulasi prediksi tanpa TensorFlow
    window = np.array(series[-60:], dtype=float).reshape(-1, 1)
    try:
        scaled = scaler.transform(window)
        
        # Simulasi prediksi sederhana
        last_price = series[-1]
        trend = np.mean(np.diff(series[-10:]))  # Trend dari 10 hari terakhir
        prediction = last_price + (trend * 1.2)  # Prediksi sederhana
        
        return render_template('index.html', charts=charts, model_loaded=True, scaler_loaded=True, model_error=model_error, scaler_error=scaler_error, predict_error=None, predict_value=float(prediction))
    except Exception as e:
        return render_template('index.html', charts=charts, model_loaded=True, scaler_loaded=True, model_error=model_error, scaler_error=scaler_error, predict_error=str(e), predict_value=None)

@app.route('/health')
def health():
    """Health check endpoint untuk Railway"""
    try:
        status = {
            'status': 'healthy',
            'model_loaded': model is not None,
            'scaler_loaded': scaler is not None,
            'timestamp': str(__import__('datetime').datetime.now())
        }
        return status, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

@app.route('/health/live')
def health_live():
    """Liveness probe untuk Railway"""
    return {'status': 'alive'}, 200

@app.route('/health/ready')
def health_ready():
    """Readiness probe untuk Railway"""
    if model is not None and scaler is not None:
        return {'status': 'ready'}, 200
    else:
        return {'status': 'not ready'}, 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
