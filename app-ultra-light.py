from flask import Flask, render_template, request
import os
import joblib
import numpy as np
import h5py
import json
import gc

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
        # Import TensorFlow dengan optimasi ekstra
        import tensorflow as tf
        
        # Disable logging untuk mengurangi overhead
        tf.get_logger().setLevel('ERROR')
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        
        # Optimasi TensorFlow untuk production
        tf.config.threading.set_inter_op_parallelism_threads(1)
        tf.config.threading.set_intra_op_parallelism_threads(1)
        tf.config.run_functions_eagerly(False)
        
        from tensorflow import keras
        
        # Load model dengan optimasi
        if os.path.exists(MODEL_PATH):
            try:
                # Coba load dengan cara yang paling efisien
                model = keras.models.load_model(MODEL_PATH, compile=False)
            except Exception as e1:
                try:
                    # Fallback method
                    from tensorflow.python.keras.saving import hdf5_format
                    with h5py.File(MODEL_PATH, mode='r') as f:
                        model = hdf5_format.load_model_from_hdf5(f)
                except Exception as e2:
                    model_error = f'Model load failed: {str(e2)}'
        else:
            model_error = 'Model file not found'
            
        # Clear cache setelah loading
        tf.keras.backend.clear_session()
        gc.collect()
        
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
        return render_template('index.html', 
                             charts=charts, 
                             model_loaded=model is not None, 
                             scaler_loaded=scaler is not None, 
                             model_error=model_error, 
                             scaler_error=scaler_error, 
                             predict_error='Model atau scaler belum siap.', 
                             predict_value=None)
    
    text = request.form.get('values', '')
    series = _parse_series(text)
    if len(series) < 60:
        return render_template('index.html', 
                             charts=charts, 
                             model_loaded=True, 
                             scaler_loaded=True, 
                             model_error=model_error, 
                             scaler_error=scaler_error, 
                             predict_error='Minimal 60 nilai penutupan diperlukan.', 
                             predict_value=None)
    
    window = np.array(series[-60:], dtype=np.float32).reshape(-1, 1)
    try:
        scaled = scaler.transform(window)
        x = scaled.reshape(1, 60, 1)
        
        # Prediksi dengan optimasi memory
        import tensorflow as tf
        with tf.device('/CPU:0'):
            y_scaled = model.predict(x, verbose=0, batch_size=1)
        
        y = scaler.inverse_transform(y_scaled.reshape(-1, 1)).ravel()[0]
        
        # Clear memory immediately
        del scaled, x, y_scaled, window
        tf.keras.backend.clear_session()
        gc.collect()
        
        return render_template('index.html', 
                             charts=charts, 
                             model_loaded=True, 
                             scaler_loaded=True, 
                             model_error=model_error, 
                             scaler_error=scaler_error, 
                             predict_error=None, 
                             predict_value=float(y))
    except Exception as e:
        return render_template('index.html', 
                             charts=charts, 
                             model_loaded=True, 
                             scaler_loaded=True, 
                             model_error=model_error, 
                             scaler_error=scaler_error, 
                             predict_error=str(e), 
                             predict_value=None)

@app.route('/health')
def health():
    return {'status': 'Deteksi Masalah Deployment', 'model_loaded': model is not None, 'scaler_loaded': scaler is not None}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
