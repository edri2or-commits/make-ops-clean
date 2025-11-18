from flask import Flask, request, jsonify
import subprocess
import os
import sys
import json
from datetime import datetime
import base64

# Try to import token automation
try:
    from token_automation import TokenAutomation, TokenScheduler
    TOKEN_AUTOMATION_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Token Automation not available: {e}")
    TOKEN_AUTOMATION_AVAILABLE = False

app = Flask(__name__)

REPO_PATH = r"C:\Users\edri2\Work\AI-Projects\make-ops-clean"
SECRETS_FILE = os.path.join(REPO_PATH, "SECRETS", ".env.local")
GITHUB_TOKEN_FILE = r"C:\Users\edri2\.github_token"

# Initialize token automation if available
if TOKEN_AUTOMATION_AVAILABLE:
    try:
        token_automation = TokenAutomation(REPO_PATH)
        token_scheduler = TokenScheduler(token_automation)
        print("✅ Token Automation loaded successfully!")
    except Exception as e:
        print(f"⚠️  Token Automation initialization failed: {e}")
        TOKEN_AUTOMATION_AVAILABLE = False

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

# [כל שאר הקוד נשאר זהה - ממשיך בהודעה הבאה]
