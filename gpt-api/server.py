from flask import Flask, request, jsonify
import subprocess
import os
import json
from datetime import datetime

app = Flask(__name__)

REPO_PATH = r"C:\Users\edri2\Work\AI-Projects\make-ops-clean"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

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

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "repo": REPO_PATH})

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
    
    # Add all changes
    run_git_command("git add .")
    
    # Commit
    result = run_git_command(f'git commit -m "{message}"')
    
    # Push
    if result['returncode'] == 0:
        push_result = run_git_command("git push origin main")
        return jsonify({
            "commit": result,
            "push": push_result
        })
    
    return jsonify(result)

@app.route('/files/list', methods=['GET'])
def list_files():
    """List files in repo"""
    path = request.args.get('path', '')
    full_path = os.path.join(REPO_PATH, path)
    
    try:
        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            items.append({
                "name": item,
                "type": "dir" if os.path.isdir(item_path) else "file",
                "path": os.path.relpath(item_path, REPO_PATH)
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
    cmd = 'gh run list --repo edri2or-commits/make-ops-clean --limit 10'
    result = run_git_command(cmd)
    
    return jsonify(result)

@app.route('/ops/run', methods=['POST'])
def ops_run():
    """Run ops command"""
    data = request.json
    command = data.get('command')
    
    result = run_git_command(f"python autopilot.py {command}")
    return jsonify(result)

if __name__ == '__main__':
    print(f"🚀 GPT API Server starting...")
    print(f"📁 Repo: {REPO_PATH}")
    print(f"🌐 Server: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
