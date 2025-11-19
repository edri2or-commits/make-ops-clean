# GPT_CONTROL_API_V1 - Cloud Run Production (GitHub API Based)
# No local repo - all operations via GitHub API

from flask import Flask, request, jsonify
import requests
import os
import json
import logging
import base64
from datetime import datetime
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment
PORT = int(os.getenv('PORT', '8080'))
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'edri2or-commits')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'make-ops-clean')
API_KEY = os.getenv('GPT_CONTROL_API_KEY')

# GitHub API base
GITHUB_API = 'https://api.github.com'

if not API_KEY:
    logger.critical("⚠️ CRITICAL: GPT_CONTROL_API_KEY not set!")
else:
    logger.info("✅ API Key authentication enabled")

if not GITHUB_TOKEN:
    logger.critical("⚠️ CRITICAL: GITHUB_TOKEN not set!")
else:
    logger.info("✅ GitHub token configured")

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not API_KEY:
            return jsonify({"error": "Server misconfigured"}), 500
        
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key or provided_key != API_KEY:
            logger.warning(f"Unauthorized from {request.remote_addr}")
            return jsonify({"error": "unauthorized"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def github_request(method, endpoint, data=None):
    """Make authenticated GitHub API request"""
    url = f"{GITHUB_API}{endpoint}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, timeout=30)
        else:
            return {"error": f"Unsupported method: {method}"}, 400
        
        if response.status_code >= 400:
            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            return {"error": response.json().get('message', 'GitHub API error')}, response.status_code
        
        return response.json(), response.status_code
    except requests.Timeout:
        logger.error("GitHub API timeout")
        return {"error": "Request timeout"}, 504
    except Exception as e:
        logger.error(f"GitHub request failed: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "version": "GPT_CONTROL_API_V1",
        "mode": "github_api",
        "auth_enabled": bool(API_KEY),
        "github_configured": bool(GITHUB_TOKEN)
    })

@app.route('/git/status', methods=['GET'])
@require_api_key
def git_status():
    """Get repository status via GitHub API"""
    logger.info("Git status requested")
    
    # Get latest commit
    endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits/main"
    result, status = github_request('GET', endpoint)
    
    if status != 200:
        return jsonify(result), status
    
    return jsonify({
        "branch": "main",
        "latest_commit": {
            "sha": result['sha'][:7],
            "message": result['commit']['message'],
            "author": result['commit']['author']['name'],
            "date": result['commit']['author']['date']
        },
        "status": "clean"
    })

@app.route('/git/commit', methods=['POST'])
@require_api_key
def git_commit():
    """Commit changes via GitHub API"""
    data = request.json or {}
    message = data.get('message', 'GPT automated commit')
    files = data.get('files', [])  # [{path: str, content: str}, ...]
    
    logger.info(f"Git commit requested: {message[:50]}...")
    
    if not files:
        return jsonify({"error": "No files to commit"}), 400
    
    try:
        # Get current branch SHA
        ref_endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/ref/heads/main"
        ref_data, status = github_request('GET', ref_endpoint)
        if status != 200:
            return jsonify(ref_data), status
        
        base_sha = ref_data['object']['sha']
        
        # Get base tree
        commit_endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/commits/{base_sha}"
        commit_data, status = github_request('GET', commit_endpoint)
        if status != 200:
            return jsonify(commit_data), status
        
        base_tree_sha = commit_data['tree']['sha']
        
        # Create blobs for each file
        tree_items = []
        for file_info in files:
            blob_data = {
                "content": file_info['content'],
                "encoding": "utf-8"
            }
            blob_endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/blobs"
            blob_result, status = github_request('POST', blob_endpoint, blob_data)
            
            if status != 201:
                return jsonify(blob_result), status
            
            tree_items.append({
                "path": file_info['path'],
                "mode": "100644",
                "type": "blob",
                "sha": blob_result['sha']
            })
        
        # Create tree
        tree_data = {
            "base_tree": base_tree_sha,
            "tree": tree_items
        }
        tree_endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/trees"
        tree_result, status = github_request('POST', tree_endpoint, tree_data)
        
        if status != 201:
            return jsonify(tree_result), status
        
        # Create commit
        commit_create_data = {
            "message": message,
            "tree": tree_result['sha'],
            "parents": [base_sha]
        }
        commit_create_endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/commits"
        new_commit, status = github_request('POST', commit_create_endpoint, commit_create_data)
        
        if status != 201:
            return jsonify(new_commit), status
        
        # Update reference
        update_ref_data = {
            "sha": new_commit['sha'],
            "force": False
        }
        update_result, status = github_request('PATCH', ref_endpoint, update_ref_data)
        
        if status != 200:
            return jsonify(update_result), status
        
        logger.info(f"Commit created: {new_commit['sha'][:7]}")
        
        return jsonify({
            "success": True,
            "commit": {
                "sha": new_commit['sha'],
                "message": message,
                "url": new_commit['html_url']
            }
        })
        
    except Exception as e:
        logger.error(f"Commit error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/files/read', methods=['GET'])
@require_api_key
def read_file():
    """Read file via GitHub API"""
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Missing 'path' parameter"}), 400
    
    logger.info(f"File read requested: {path}")
    
    endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    result, status = github_request('GET', endpoint)
    
    if status != 200:
        return jsonify(result), status
    
    # Decode base64 content
    try:
        content = base64.b64decode(result['content']).decode('utf-8')
        return jsonify({
            "path": path,
            "content": content,
            "sha": result['sha']
        })
    except Exception as e:
        logger.error(f"Decode error: {str(e)}")
        return jsonify({"error": "Failed to decode file"}), 500

@app.route('/files/write', methods=['POST'])
@require_api_key
def write_file():
    """Write file via GitHub API"""
    data = request.json
    if not data or 'path' not in data or 'content' not in data:
        return jsonify({"error": "Missing 'path' or 'content'"}), 400
    
    path = data['path']
    content = data['content']
    message = data.get('message', f'Update {path}')
    
    logger.info(f"File write requested: {path}")
    
    # Check if file exists (to get SHA)
    endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    existing, status = github_request('GET', endpoint)
    
    file_data = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    
    if status == 200:
        # File exists, include SHA for update
        file_data['sha'] = existing['sha']
    
    result, status = github_request('PUT', endpoint, file_data)
    
    if status not in [200, 201]:
        return jsonify(result), status
    
    logger.info(f"File written: {path}")
    return jsonify({
        "success": True,
        "path": path,
        "commit": {
            "sha": result['commit']['sha'],
            "url": result['commit']['html_url']
        }
    })

@app.route('/secrets/list', methods=['GET'])
@require_api_key
def list_secrets():
    """List secrets from SECRETS/.env.local"""
    logger.info("Secrets list requested")
    
    endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/SECRETS/.env.local"
    result, status = github_request('GET', endpoint)
    
    if status != 200:
        return jsonify({"secrets": {}})
    
    try:
        content = base64.b64decode(result['content']).decode('utf-8')
        secrets = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if len(v) > 8:
                    secrets[k] = v[:8] + "***"
                else:
                    secrets[k] = "***"
        
        return jsonify({"secrets": secrets})
    except Exception as e:
        logger.error(f"Secrets list error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/secrets/set', methods=['POST'])
@require_api_key
def set_secret():
    """Set secret in SECRETS/.env.local"""
    data = request.json
    if not data or 'key' not in data or 'value' not in data:
        return jsonify({"error": "Missing 'key' or 'value'"}), 400
    
    key = data['key']
    value = data['value']
    
    logger.info(f"Secret set requested: {key}")
    
    try:
        # Read current secrets
        endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/SECRETS/.env.local"
        existing, status = github_request('GET', endpoint)
        
        secrets = {}
        file_sha = None
        
        if status == 200:
            file_sha = existing['sha']
            content = base64.b64decode(existing['content']).decode('utf-8')
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    secrets[k.strip()] = v.strip()
        
        # Update secret
        secrets[key] = value
        
        # Build new content
        new_content = f"# Updated: {datetime.now().isoformat()}\n"
        for k, v in secrets.items():
            new_content += f"{k}={v}\n"
        
        # Write back
        file_data = {
            "message": f"[Secrets] Update {key}",
            "content": base64.b64encode(new_content.encode('utf-8')).decode('utf-8'),
            "branch": "main"
        }
        
        if file_sha:
            file_data['sha'] = file_sha
        
        result, status = github_request('PUT', endpoint, file_data)
        
        if status not in [200, 201]:
            return jsonify(result), status
        
        logger.info(f"Secret set: {key}")
        return jsonify({"success": True, "key": key})
        
    except Exception as e:
        logger.error(f"Secret set error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/tokens/generate', methods=['POST'])
@require_api_key
def generate_token():
    """Generate token and save to secrets"""
    import secrets
    import string
    
    data = request.json or {}
    service = data.get('service', 'GENERATED_TOKEN')
    prefix = data.get('prefix', '')
    length = data.get('length', 64)
    
    logger.info(f"Token generation: {service}")
    
    try:
        # Generate token
        chars = string.ascii_letters + string.digits
        token = prefix + ''.join(secrets.choice(chars) for _ in range(length))
        
        # Save via secrets/set
        set_result = set_secret_internal(service, token)
        
        if not set_result.get('success'):
            return jsonify(set_result), 500
        
        return jsonify({
            "success": True,
            "service": service,
            "token": token,
            "length": len(token)
        })
    except Exception as e:
        logger.error(f"Token generation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def set_secret_internal(key, value):
    """Internal function to set secret (no auth check)"""
    try:
        endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/SECRETS/.env.local"
        existing, status = github_request('GET', endpoint)
        
        secrets = {}
        file_sha = None
        
        if status == 200:
            file_sha = existing['sha']
            content = base64.b64decode(existing['content']).decode('utf-8')
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    secrets[k.strip()] = v.strip()
        
        secrets[key] = value
        
        new_content = f"# Updated: {datetime.now().isoformat()}\n"
        for k, v in secrets.items():
            new_content += f"{k}={v}\n"
        
        file_data = {
            "message": f"[Token] Generate {key}",
            "content": base64.b64encode(new_content.encode('utf-8')).decode('utf-8'),
            "branch": "main"
        }
        
        if file_sha:
            file_data['sha'] = file_sha
        
        result, status = github_request('PUT', endpoint, file_data)
        
        return {"success": status in [200, 201]}
    except:
        return {"success": False}

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 GPT_CONTROL_API_V1 - GitHub API Mode")
    logger.info("=" * 60)
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"📦 Repo: {GITHUB_OWNER}/{GITHUB_REPO}")
    logger.info(f"🔐 Auth: {'ENABLED' if API_KEY else 'DISABLED'}")
    logger.info(f"🔑 GitHub: {'CONFIGURED' if GITHUB_TOKEN else 'MISSING'}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=PORT)
