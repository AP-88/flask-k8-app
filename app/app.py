import os
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# configured via ConfigMap or send the default 
DATA_FILE_PATH = os.getenv('FILE_PATH', '/storage/data.txt')

# shared log file on pv
LOG_FILE_PATH = "/storage/access_log.txt"

@app.before_request
def log_access():
    if request.path == '/health':
        return
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{now}] User IP: {request.remote_addr} -> {request.path}\n"
        with open(LOG_FILE_PATH, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")

@app.route('/')
def home():
    title = os.getenv('TITLE', 'Flask k8 App')
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        data = ["The data file is not available."]
    return render_template('index.html', title=title, data=data)

@app.route('/log')
def show_logs():
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            log_data = f.readlines()[-30:] # Display the last 30 lines
    except FileNotFoundError:
        log_data = ["No logs recorded."]
    return render_template('log.html', log_data=log_data)

@app.route('/health')
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
