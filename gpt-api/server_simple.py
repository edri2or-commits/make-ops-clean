# GPT_CONTROL_API_V1
# Official API endpoint for GPT control over make-ops-clean repository
# Port: 5001

from flask import Flask, request, jsonify
import subprocess
import os
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

REPO_PATH = r"C:\Users\edri2\Work\AI-Projects\make-ops-clean"
SECRETS_FILE = os.path.join(REPO_PATH, "SECRETS", ".env.local")

# Load API key from environment or secrets file
API_KEY = None
SECRETS_ENV_FILE = os.path.join(REPO_PATH, "gpt-api", "secrets", "secrets.env")

def load_api_key():
    """Load GPT_CONTROL_API_KEY from environment or secrets file"""
    global API_KEY
    
    # Try environment variable first
    API_KEY = os.getenv('GPT_CONTROL_API_KEY')
    
    # If not in env, try secrets file
    if not API_KEY and os.path.exists(SECRETS_ENV_FILE):
        with open(SECRETS_ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith('GPT_CONTROL_API_KEY='):
                    API_KEY = line.split('=', 1)[1].strip()
                    break
    
    if not API_KEY:
        print("⚠️  WARNING: No GPT_CONTROL_API_KEY found. API is unprotected!")
        print("   Set GPT_CONTROL_API_KEY in environment or gpt-api/secrets/secrets.env")

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not API_KEY:
            # If no API key configured, allow access (for initial setup)
            return f(*args, **kwargs)
        
        # Check for API key in header
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key or provided_key != API_KEY:
            return jsonify({"error": "unauthorized"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def run_git(cmd):
    result = subprocess.run(cmd, shell=True, cwd=REPO_PATH, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

# Health check (no auth required)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "version": "GPT_CONTROL_API_V1",
        "api": "GPT_CONTROL_API_V1",
        "auth_enabled": bool(API_KEY)
    })

# Git operations
@app.route('/git/status', methods=['GET'])
@require_api_key
def git_status():
    return jsonify(run_git("git status"))

@app.route('/git/commit', methods=['POST'])
@require_api_key
def git_commit():
    msg = request.json.get('message', 'Auto commit')
    run_git("git add .")
    result = run_git(f'git commit -m "{msg}"')
    if result['returncode'] == 0:
        push = run_git("git push origin main")
        return jsonify({"commit": result, "push": push})
    return jsonify(result)

# File operations
@app.route('/files/read', methods=['GET'])
@require_api_key
def read_file():
    path = request.args.get('path')
    try:
        with open(os.path.join(REPO_PATH, path), 'r', encoding='utf-8') as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/write', methods=['POST'])
@require_api_key
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

# Secrets management
@app.route('/secrets/list', methods=['GET'])
@require_api_key
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
@require_api_key
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

# Token generation
@app.route('/tokens/generate', methods=['POST'])
@require_api_key
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
    load_api_key()
    print("=" * 60)
    print("🚀 GPT_CONTROL_API_V1")
    print("=" * 60)
    print(f"📁 Repository: {REPO_PATH}")
    print(f"🌐 Endpoint: http://localhost:5001")
    print(f"🔐 Auth: {'ENABLED' if API_KEY else 'DISABLED (WARNING!)'}")
    print("")
    print("✅ Capabilities:")
    print("   - Git operations (status, commit+push)")
    print("   - File operations (read, write)")
    print("   - Secrets management (list, set)")
    print("   - Token generation (basic)")
    print("")
    if not API_KEY:
        print("⚠️  To enable authentication:")
        print("   Add GPT_CONTROL_API_KEY to gpt-api/secrets/secrets.env")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5001, debug=True)
