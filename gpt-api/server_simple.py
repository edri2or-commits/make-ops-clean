# GPT API v3 - Simple & Working
# Copy this content to server.py or run as separate server

from flask import Flask, request, jsonify
import subprocess
import os
import json
from datetime import datetime

app = Flask(__name__)

REPO_PATH = r"C:\Users\edri2\Work\AI-Projects\make-ops-clean"
SECRETS_FILE = os.path.join(REPO_PATH, "SECRETS", ".env.local")

def run_git(cmd):
    result = subprocess.run(cmd, shell=True, cwd=REPO_PATH, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

# Health
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "version": "3.0-simple"})

# Git
@app.route('/git/status', methods=['GET'])
def git_status():
    return jsonify(run_git("git status"))

@app.route('/git/commit', methods=['POST'])
def git_commit():
    msg = request.json.get('message', 'Auto commit')
    run_git("git add .")
    result = run_git(f'git commit -m "{msg}"')
    if result['returncode'] == 0:
        push = run_git("git push origin main")
        return jsonify({"commit": result, "push": push})
    return jsonify(result)

# Files
@app.route('/files/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    try:
        with open(os.path.join(REPO_PATH, path), 'r', encoding='utf-8') as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/write', methods=['POST'])
def write_file():
    data = request.json
    path = os.path.join(REPO_PATH, data['path'])
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data['content'])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Secrets
@app.route('/secrets/list', methods=['GET'])
def list_secrets():
    secrets = {}
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    secrets[k.strip()] = v.strip()[:8] + "***"
    return jsonify({"secrets": secrets})

@app.route('/secrets/set', methods=['POST'])
def set_secret():
    data = request.json
    os.makedirs(os.path.dirname(SECRETS_FILE), exist_ok=True)
    existing = {}
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    existing[k.strip()] = v.strip()
    existing[data['key']] = data['value']
    with open(SECRETS_FILE, 'w') as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")
    return jsonify({"success": True})

# Token Generation
@app.route('/tokens/generate', methods=['POST'])
def generate_token():
    import secrets
    import string
    data = request.json
    length = data.get('length', 64)
    prefix = data.get('prefix', '')
    
    chars = string.ascii_letters + string.digits
    token = prefix + ''.join(secrets.choice(chars) for _ in range(length))
    
    # Save it
    service = data.get('service', 'GENERATED_TOKEN')
    with open(SECRETS_FILE, 'a') as f:
        f.write(f"\n{service}={token}\n")
    
    return jsonify({
        "success": True,
        "service": service,
        "token": token,
        "length": len(token)
    })

if __name__ == '__main__':
    print("🚀 GPT API v3.0 - WORKING!")
    print(f"📁 Repo: {REPO_PATH}")
    print(f"🌐 http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
