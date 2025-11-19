# GPT_CONTROL_API_V1 - Cloud Run Production Version
# Official API endpoint for GPT control over make-ops-clean repository

from flask import Flask, request, jsonify
import subprocess
import os
import json
import logging
from datetime import datetime
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment
PORT = int(os.getenv('PORT', '8080'))  # Cloud Run uses PORT env
REPO_PATH = os.getenv('REPO_PATH', '/workspace')
SECRETS_FILE = os.path.join(REPO_PATH, "SECRETS", ".env.local")
API_KEY = os.getenv('GPT_CONTROL_API_KEY')

if not API_KEY:
    logger.critical("⚠️  CRITICAL: GPT_CONTROL_API_KEY not set! API will be unprotected!")
else:
    logger.info("✅ API Key authentication enabled")

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not API_KEY:
            logger.warning("API called without authentication (no key configured)")
            return jsonify({"error": "Server misconfigured - no API key"}), 500
        
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key:
            logger.warning(f"Unauthorized attempt - no API key provided from {request.remote_addr}")
            return jsonify({"error": "unauthorized - missing X-API-Key header"}), 401
        
        if provided_key != API_KEY:
            logger.warning(f"Unauthorized attempt - invalid API key from {request.remote_addr}")
            return jsonify({"error": "unauthorized - invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def run_git(cmd):
    """Execute git command safely"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=REPO_PATH, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        return {
            "stdout": result.stdout, 
            "stderr": result.stderr, 
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        logger.error(f"Git command timed out: {cmd}")
        return {"error": "Command timed out", "returncode": -1}
    except Exception as e:
        logger.error(f"Git command failed: {cmd} - {str(e)}")
        return {"error": str(e), "returncode": -1}

# Health check (no auth required)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "version": "GPT_CONTROL_API_V1",
        "api": "GPT_CONTROL_API_V1",
        "environment": "cloud_run",
        "auth_enabled": bool(API_KEY)
    })

# Git operations
@app.route('/git/status', methods=['GET'])
@require_api_key
def git_status():
    logger.info("Git status requested")
    return jsonify(run_git("git status"))

@app.route('/git/commit', methods=['POST'])
@require_api_key
def git_commit():
    data = request.json or {}
    msg = data.get('message', 'GPT automated commit')
    push = data.get('push', True)
    
    logger.info(f"Git commit requested: {msg[:50]}...")
    
    # Add all changes
    run_git("git add .")
    
    # Commit
    result = run_git(f'git commit -m "{msg}"')
    
    if result['returncode'] == 0 and push:
        push_result = run_git("git push origin main")
        logger.info("Git commit and push completed")
        return jsonify({"commit": result, "push": push_result})
    
    logger.info("Git commit completed (no push)")
    return jsonify(result)

# File operations
@app.route('/files/read', methods=['GET'])
@require_api_key
def read_file():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Missing 'path' parameter"}), 400
    
    logger.info(f"File read requested: {path}")
    
    try:
        full_path = os.path.join(REPO_PATH, path)
        
        # Security: prevent path traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(REPO_PATH)):
            logger.warning(f"Path traversal attempt: {path}")
            return jsonify({"error": "Invalid path"}), 403
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({"path": path, "content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"File read error: {path} - {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/files/write', methods=['POST'])
@require_api_key
def write_file():
    data = request.json
    if not data or 'path' not in data or 'content' not in data:
        return jsonify({"error": "Missing 'path' or 'content'"}), 400
    
    path = data['path']
    content = data['content']
    
    logger.info(f"File write requested: {path}")
    
    try:
        full_path = os.path.join(REPO_PATH, path)
        
        # Security: prevent path traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(REPO_PATH)):
            logger.warning(f"Path traversal attempt: {path}")
            return jsonify({"error": "Invalid path"}), 403
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"File written successfully: {path}")
        return jsonify({"success": True, "path": path})
    except Exception as e:
        logger.error(f"File write error: {path} - {str(e)}")
        return jsonify({"error": str(e)}), 500

# Secrets management
@app.route('/secrets/list', methods=['GET'])
@require_api_key
def list_secrets():
    logger.info("Secrets list requested")
    secrets = {}
    
    try:
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip()
                        # Mask the value (show first 8 chars)
                        if len(v) > 8:
                            secrets[k] = v[:8] + "***"
                        else:
                            secrets[k] = "***"
        
        # Never log actual secret values
        logger.info(f"Secrets list returned: {len(secrets)} keys")
        return jsonify({"secrets": secrets})
    except Exception as e:
        logger.error(f"Secrets list error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/secrets/set', methods=['POST'])
@require_api_key
def set_secret():
    data = request.json
    if not data or 'key' not in data or 'value' not in data:
        return jsonify({"error": "Missing 'key' or 'value'"}), 400
    
    key = data['key']
    value = data['value']
    
    # Never log the actual secret value
    logger.info(f"Secret set requested: {key}")
    
    try:
        os.makedirs(os.path.dirname(SECRETS_FILE), exist_ok=True)
        
        # Read existing secrets
        existing = {}
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        existing[k.strip()] = v.strip()
        
        # Update or add new secret
        existing[key] = value
        
        # Write back
        with open(SECRETS_FILE, 'w') as f:
            f.write(f"# Updated: {datetime.now().isoformat()}\n")
            for k, v in existing.items():
                f.write(f"{k}={v}\n")
        
        logger.info(f"Secret set successfully: {key}")
        return jsonify({"success": True, "key": key})
    except Exception as e:
        logger.error(f"Secret set error: {key} - {str(e)}")
        return jsonify({"error": str(e)}), 500

# Token generation
@app.route('/tokens/generate', methods=['POST'])
@require_api_key
def generate_token():
    import secrets
    import string
    
    data = request.json or {}
    service = data.get('service', 'GENERATED_TOKEN')
    prefix = data.get('prefix', '')
    length = data.get('length', 64)
    
    logger.info(f"Token generation requested: {service}")
    
    try:
        # Generate cryptographically secure token
        chars = string.ascii_letters + string.digits
        token = prefix + ''.join(secrets.choice(chars) for _ in range(length))
        
        # Save to secrets file
        os.makedirs(os.path.dirname(SECRETS_FILE), exist_ok=True)
        with open(SECRETS_FILE, 'a') as f:
            f.write(f"\n{service}={token}\n")
        
        logger.info(f"Token generated and saved: {service}")
        
        return jsonify({
            "success": True,
            "service": service,
            "token": token,
            "length": len(token)
        })
    except Exception as e:
        logger.error(f"Token generation error: {service} - {str(e)}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 GPT_CONTROL_API_V1 - Cloud Run")
    logger.info("=" * 60)
    logger.info(f"📁 Repository: {REPO_PATH}")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🔐 Auth: {'ENABLED' if API_KEY else 'DISABLED (CRITICAL!)'}")
    logger.info("")
    logger.info("✅ Capabilities:")
    logger.info("   - Git operations (status, commit+push)")
    logger.info("   - File operations (read, write)")
    logger.info("   - Secrets management (list, set)")
    logger.info("   - Token generation (basic)")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=PORT)
