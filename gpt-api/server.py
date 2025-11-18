from flask import Flask, request, jsonify
import subprocess
import os
import json
from datetime import datetime
import base64

app = Flask(__name__)

REPO_PATH = r"C:\Users\edri2\Work\AI-Projects\make-ops-clean"
SECRETS_FILE = os.path.join(REPO_PATH, "SECRETS", ".env.local")
GITHUB_TOKEN_FILE = r"C:\Users\edri2\.github_token"

def run_git_command(cmd):
    """Execute git command in repo"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

def run_command(cmd, cwd=None):
    """Execute any command"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd or REPO_PATH,
        capture_output=True,
        text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

# ============================================
# BASIC ENDPOINTS
# ============================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "repo": REPO_PATH,
        "api_version": "2.0",
        "capabilities": [
            "git", "files", "secrets", "tokens", "github-actions",
            "environment", "processes", "system"
        ]
    })

# ============================================
# GIT OPERATIONS
# ============================================

@app.route('/git/status', methods=['GET'])
def git_status():
    """Get current git status"""
    result = run_git_command("git status")
    return jsonify(result)

@app.route('/git/pull', methods=['POST'])
def git_pull():
    """Pull latest changes"""
    result = run_git_command("git pull origin main")
    return jsonify(result)

@app.route('/git/commit', methods=['POST'])
def git_commit():
    """Add, commit and push changes"""
    data = request.json
    message = data.get('message', 'GPT automated commit')
    push = data.get('push', True)
    
    # Add all changes
    run_git_command("git add .")
    
    # Commit
    result = run_git_command(f'git commit -m "{message}"')
    
    # Push if requested
    if push and result['returncode'] == 0:
        push_result = run_git_command("git push origin main")
        return jsonify({
            "commit": result,
            "push": push_result
        })
    
    return jsonify(result)

@app.route('/git/log', methods=['GET'])
def git_log():
    """Get git log"""
    limit = request.args.get('limit', 10)
    result = run_git_command(f"git log --oneline -n {limit}")
    return jsonify(result)

@app.route('/git/diff', methods=['GET'])
def git_diff():
    """Get git diff"""
    result = run_git_command("git diff")
    return jsonify(result)

@app.route('/git/branch', methods=['GET', 'POST'])
def git_branch():
    """List or create branches"""
    if request.method == 'GET':
        result = run_git_command("git branch -a")
        return jsonify(result)
    else:
        data = request.json
        branch = data.get('branch')
        result = run_git_command(f"git checkout -b {branch}")
        return jsonify(result)

# ============================================
# FILE OPERATIONS
# ============================================

@app.route('/files/list', methods=['GET'])
def list_files():
    """List files in repo"""
    path = request.args.get('path', '')
    full_path = os.path.join(REPO_PATH, path)
    
    try:
        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            items.append({
                "name": item,
                "type": "dir" if os.path.isdir(item_path) else "file",
                "path": os.path.relpath(item_path, REPO_PATH),
                "size": size
            })
        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/read', methods=['GET'])
def read_file():
    """Read file content"""
    path = request.args.get('path')
    full_path = os.path.join(REPO_PATH, path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"path": path, "content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/write', methods=['POST'])
def write_file():
    """Write file content"""
    data = request.json
    path = data.get('path')
    content = data.get('content')
    
    full_path = os.path.join(REPO_PATH, path)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True, "path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/delete', methods=['DELETE'])
def delete_file():
    """Delete file"""
    path = request.args.get('path')
    full_path = os.path.join(REPO_PATH, path)
    
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            import shutil
            shutil.rmtree(full_path)
        return jsonify({"success": True, "path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/search', methods=['GET'])
def search_files():
    """Search files by pattern"""
    pattern = request.args.get('pattern', '')
    path = request.args.get('path', '')
    
    try:
        full_path = os.path.join(REPO_PATH, path)
        matches = []
        
        for root, dirs, files in os.walk(full_path):
            # Skip .git directory
            if '.git' in root:
                continue
                
            for file in files:
                if pattern.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, REPO_PATH)
                    matches.append({
                        "name": file,
                        "path": rel_path,
                        "size": os.path.getsize(file_path)
                    })
        
        return jsonify({"matches": matches, "count": len(matches)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# SECRETS & TOKENS MANAGEMENT
# ============================================

@app.route('/secrets/list', methods=['GET'])
def list_secrets():
    """List all secrets (masked)"""
    try:
        secrets = {}
        
        # Read from .env.local if exists
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Mask the value
                        secrets[key] = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '***'
        
        # Check GitHub token
        if os.path.exists(GITHUB_TOKEN_FILE):
            with open(GITHUB_TOKEN_FILE, 'r') as f:
                token = f.read().strip()
                secrets['GITHUB_TOKEN'] = token[:7] + '*' * (len(token) - 7)
        
        # Environment variables
        for key in ['GITHUB_TOKEN', 'GOOGLE_OAUTH_CLIENT_ID', 'GOOGLE_OAUTH_CLIENT_SECRET']:
            if key in os.environ:
                val = os.environ[key]
                secrets[key + '_ENV'] = val[:4] + '*' * (len(val) - 4) if len(val) > 4 else '***'
        
        return jsonify({"secrets": secrets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/secrets/get', methods=['GET'])
def get_secret():
    """Get specific secret (full value)"""
    key = request.args.get('key')
    
    try:
        # Check .env.local
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, 'r') as f:
                for line in f:
                    if line.startswith(f"{key}="):
                        value = line.split('=', 1)[1].strip()
                        return jsonify({"key": key, "value": value})
        
        # Check environment
        if key in os.environ:
            return jsonify({"key": key, "value": os.environ[key]})
        
        # Check GitHub token file
        if key == 'GITHUB_TOKEN' and os.path.exists(GITHUB_TOKEN_FILE):
            with open(GITHUB_TOKEN_FILE, 'r') as f:
                return jsonify({"key": key, "value": f.read().strip()})
        
        return jsonify({"error": "Secret not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/secrets/set', methods=['POST'])
def set_secret():
    """Set or update a secret"""
    data = request.json
    key = data.get('key')
    value = data.get('value')
    location = data.get('location', 'env')  # 'env', 'github', or 'all'
    
    try:
        results = {}
        
        if location in ['env', 'all']:
            # Update .env.local
            os.makedirs(os.path.dirname(SECRETS_FILE), exist_ok=True)
            
            # Read existing
            existing = {}
            if os.path.exists(SECRETS_FILE):
                with open(SECRETS_FILE, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            k, v = line.split('=', 1)
                            existing[k.strip()] = v.strip()
            
            # Update
            existing[key] = value
            
            # Write back
            with open(SECRETS_FILE, 'w') as f:
                f.write(f"# Updated: {datetime.now().isoformat()}\n")
                for k, v in existing.items():
                    f.write(f"{k}={v}\n")
            
            results['env'] = 'updated'
        
        if location in ['github', 'all'] and key == 'GITHUB_TOKEN':
            # Update GitHub token file
            with open(GITHUB_TOKEN_FILE, 'w') as f:
                f.write(value)
            results['github'] = 'updated'
        
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/secrets/delete', methods=['DELETE'])
def delete_secret():
    """Delete a secret"""
    key = request.args.get('key')
    
    try:
        # Remove from .env.local
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, 'r') as f:
                lines = [line for line in f if not line.startswith(f"{key}=")]
            
            with open(SECRETS_FILE, 'w') as f:
                f.writelines(lines)
        
        return jsonify({"success": True, "key": key})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tokens/github/test', methods=['GET'])
def test_github_token():
    """Test GitHub token validity"""
    try:
        result = run_command("gh auth status")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tokens/github/refresh', methods=['POST'])
def refresh_github_token():
    """Refresh GitHub token"""
    data = request.json
    new_token = data.get('token')
    
    try:
        # Save new token
        with open(GITHUB_TOKEN_FILE, 'w') as f:
            f.write(new_token)
        
        # Configure git to use new token
        run_command(f'git config --global credential.helper store')
        
        # Test it
        test_result = run_command("gh auth status")
        
        return jsonify({
            "success": True,
            "token_saved": True,
            "test": test_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# GITHUB ACTIONS
# ============================================

@app.route('/actions/trigger', methods=['POST'])
def trigger_action():
    """Trigger GitHub Action workflow"""
    data = request.json
    workflow = data.get('workflow', 'index-append-manual.yml')
    
    cmd = f'gh workflow run {workflow} --repo edri2or-commits/make-ops-clean'
    result = run_git_command(cmd)
    
    return jsonify(result)

@app.route('/actions/list', methods=['GET'])
def list_actions():
    """List recent workflow runs"""
    limit = request.args.get('limit', 10)
    cmd = f'gh run list --repo edri2or-commits/make-ops-clean --limit {limit}'
    result = run_git_command(cmd)
    
    return jsonify(result)

@app.route('/actions/status', methods=['GET'])
def action_status():
    """Get status of specific run"""
    run_id = request.args.get('run_id')
    cmd = f'gh run view {run_id} --repo edri2or-commits/make-ops-clean'
    result = run_git_command(cmd)
    
    return jsonify(result)

@app.route('/actions/logs', methods=['GET'])
def action_logs():
    """Get logs from workflow run"""
    run_id = request.args.get('run_id')
    cmd = f'gh run view {run_id} --log --repo edri2or-commits/make-ops-clean'
    result = run_git_command(cmd)
    
    return jsonify(result)

# ============================================
# ENVIRONMENT & SYSTEM
# ============================================

@app.route('/env/list', methods=['GET'])
def list_env():
    """List environment variables"""
    return jsonify({"env": dict(os.environ)})

@app.route('/env/get', methods=['GET'])
def get_env():
    """Get specific environment variable"""
    key = request.args.get('key')
    return jsonify({"key": key, "value": os.environ.get(key)})

@app.route('/env/set', methods=['POST'])
def set_env():
    """Set environment variable (for current session)"""
    data = request.json
    key = data.get('key')
    value = data.get('value')
    
    os.environ[key] = value
    return jsonify({"success": True, "key": key})

@app.route('/system/processes', methods=['GET'])
def list_processes():
    """List running processes"""
    result = run_command("Get-Process | Select-Object -First 20 Name, Id, CPU | ConvertTo-Json", cwd=None)
    return jsonify(result)

@app.route('/system/info', methods=['GET'])
def system_info():
    """Get system information"""
    info = {
        "platform": os.name,
        "cwd": os.getcwd(),
        "repo_path": REPO_PATH,
        "python_version": os.sys.version,
        "env_count": len(os.environ)
    }
    return jsonify(info)

@app.route('/command/run', methods=['POST'])
def run_custom_command():
    """Run any custom command"""
    data = request.json
    command = data.get('command')
    cwd = data.get('cwd', REPO_PATH)
    shell = data.get('shell', 'powershell')
    
    if shell == 'powershell':
        cmd = f'powershell -Command "{command}"'
    elif shell == 'cmd':
        cmd = f'cmd /c "{command}"'
    else:
        cmd = command
    
    result = run_command(cmd, cwd=cwd)
    return jsonify(result)

# ============================================
# OPS AUTOMATION
# ============================================

@app.route('/ops/run', methods=['POST'])
def ops_run():
    """Run ops command"""
    data = request.json
    command = data.get('command')
    
    result = run_git_command(f"python autopilot.py {command}")
    return jsonify(result)

@app.route('/ops/status', methods=['GET'])
def ops_status():
    """Get ops status"""
    try:
        # Read autopilot state
        state_file = os.path.join(REPO_PATH, 'autopilot-state.json')
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
            return jsonify({"state": state})
        return jsonify({"state": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# STARTUP
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 GPT API Server v2.0 - FULL CONTROL")
    print("=" * 60)
    print(f"📁 Repository: {REPO_PATH}")
    print(f"🔐 Secrets: {SECRETS_FILE}")
    print(f"🌐 Server: http://localhost:5000")
    print("")
    print("✅ Capabilities:")
    print("   - Git operations (status, commit, push, branch)")
    print("   - File operations (read, write, delete, search)")
    print("   - Secrets management (list, get, set, delete)")
    print("   - Token management (GitHub, Google, etc)")
    print("   - GitHub Actions (trigger, list, status, logs)")
    print("   - Environment variables")
    print("   - System commands")
    print("   - Ops automation")
    print("")
    print("🔒 WARNING: This API has FULL SYSTEM ACCESS!")
    print("   Keep it local and secure.")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
