#!/usr/bin/env python3
"""
GitHub App Authentication Test - READ ONLY (Cloud-ready)
Validates JWT generation and Installation Token minting
NO WRITES - Only GET operations for smoke tests

Supports multiple credential sources:
- GitHub Actions Secret (GH_APP_PRIVATE_KEY_PEM)
- Google Secret Manager
- Environment variable
- File path (for local testing)
"""

import json
import time
import sys
import os
from datetime import datetime, timedelta

try:
    import jwt
    import requests
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyJWT[crypto]", "requests"])
    import jwt
    import requests

def read_private_key():
    """
    Read private key from multiple sources (in order of preference):
    1. Environment variable: GH_APP_PRIVATE_KEY_PEM
    2. Google Secret Manager (if available)
    3. File path: GH_APP_PRIVATE_KEY_FILE
    """
    # Try environment variable first (GitHub Actions Secret)
    if 'GH_APP_PRIVATE_KEY_PEM' in os.environ:
        print("✅ Reading private key from environment variable (GitHub Secret)")
        key = os.environ['GH_APP_PRIVATE_KEY_PEM']
        # Handle potential base64 encoding or escaped newlines
        if '\\n' in key:
            key = key.replace('\\n', '\n')
        return key
    
    # Try Google Secret Manager
    try:
        from google.cloud import secretmanager
        print("🔍 Attempting to read from Google Secret Manager...")
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get('GCP_PROJECT_ID', 'your-project-id')
        secret_id = os.environ.get('GH_APP_SECRET_NAME', 'github-app-2251005-private-key')
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        print(f"✅ Reading private key from Google Secret Manager ({secret_id})")
        return response.payload.data.decode('utf-8')
    except ImportError:
        pass  # Google Secret Manager not available
    except Exception as e:
        print(f"⚠️  Google Secret Manager not available: {e}")
    
    # Try file path
    if 'GH_APP_PRIVATE_KEY_FILE' in os.environ:
        file_path = os.environ['GH_APP_PRIVATE_KEY_FILE']
        print(f"✅ Reading private key from file: {file_path}")
        with open(file_path, 'r') as f:
            return f.read()
    
    # No source available
    print("❌ No private key source found")
    print("   Set one of:")
    print("   - GH_APP_PRIVATE_KEY_PEM (environment variable / GitHub Secret)")
    print("   - GH_APP_PRIVATE_KEY_FILE (path to .pem file)")
    print("   - Google Secret Manager (with GCP_PROJECT_ID and GH_APP_SECRET_NAME)")
    return None

def generate_jwt(app_id, private_key_pem, exp_minutes=10):
    """Generate GitHub App JWT"""
    now = int(time.time())
    
    # Ensure clock offset (issued 60 seconds in past for clock skew tolerance)
    iat = now - 60
    exp = now + (exp_minutes * 60)
    
    payload = {
        'iat': iat,
        'exp': exp,
        'iss': app_id
    }
    
    token = jwt.encode(payload, private_key_pem, algorithm='RS256')
    
    return token, {
        "iat": iat,
        "exp": exp,
        "iat_offset_sec": 60,
        "exp_minutes": exp_minutes,
        "iat_readable": datetime.fromtimestamp(iat).isoformat(),
        "exp_readable": datetime.fromtimestamp(exp).isoformat()
    }

def get_installation_token(jwt_token, installation_id):
    """Mint Installation Access Token"""
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    expires_at = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
    created_at = datetime.utcnow()
    expires_in_min = (expires_at - created_at).total_seconds() / 60
    
    return data['token'], {
        "token_length": len(data['token']),
        "expires_at": data['expires_at'],
        "expires_in_min": round(expires_in_min),
        "permissions": data.get('permissions', {}),
        "repositories": [r['name'] for r in data.get('repositories', [])]
    }

def smoke_test_readonly(token, owner, repo):
    """Perform READ-ONLY smoke tests"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    results = {}
    
    # Test 1: Get repository metadata
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results["repo_meta"] = {
            "status": "✅ ok",
            "name": data['name'],
            "private": data['private'],
            "default_branch": data['default_branch']
        }
    except Exception as e:
        results["repo_meta"] = {"status": "❌ failed", "error": str(e)}
    
    # Test 2: List issues (read-only)
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=5"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results["issues"] = {
            "status": "✅ ok",
            "count": len(data),
            "sample_titles": [issue['title'][:50] for issue in data[:3]]
        }
    except Exception as e:
        results["issues"] = {"status": "❌ failed", "error": str(e)}
    
    # Test 3: List pull requests (read-only)
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=5"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results["prs"] = {
            "status": "✅ ok",
            "count": len(data),
            "sample_titles": [pr['title'][:50] for pr in data[:3]]
        }
    except Exception as e:
        results["prs"] = {"status": "❌ failed", "error": str(e)}
    
    # Test 4: List workflows (read-only)
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results["workflows"] = {
            "status": "✅ ok",
            "count": data['total_count'],
            "sample_names": [wf['name'][:50] for wf in data['workflows'][:3]]
        }
    except Exception as e:
        results["workflows"] = {"status": "❌ failed", "error": str(e)}
    
    return results

def main():
    print("🔐 GitHub App Authentication Test - READ ONLY (Cloud)")
    print("=" * 60)
    
    # Configuration
    APP_ID = os.environ.get('GH_APP_ID', '2251005')
    INSTALLATION_ID = os.environ.get('GH_INSTALLATION_ID', '60358677')
    OWNER = os.environ.get('GH_REPO_OWNER', 'edri2or-commits')
    REPO = os.environ.get('GH_REPO_NAME', 'make-ops-clean')
    
    print(f"\n📋 Configuration:")
    print(f"   App ID: {APP_ID}")
    print(f"   Installation ID: {INSTALLATION_ID}")
    print(f"   Repository: {OWNER}/{REPO}")
    
    # Step 1: Read private key
    print(f"\n📋 Step 1: Reading private key")
    
    private_key = read_private_key()
    
    if not private_key:
        return {"error": "private_key_read_failed"}
    
    print(f"✅ Private key retrieved (length: {len(private_key)} chars)")
    
    # Step 2: Generate JWT
    print(f"\n🔑 Step 2: Generating JWT")
    print(f"   Expiry: 10 minutes")
    
    try:
        jwt_token, jwt_info = generate_jwt(APP_ID, private_key, exp_minutes=10)
        print(f"✅ JWT generated")
        print(f"   IAT: {jwt_info['iat_readable']} (offset: -{jwt_info['iat_offset_sec']}s)")
        print(f"   EXP: {jwt_info['exp_readable']} ({jwt_info['exp_minutes']} minutes)")
    except Exception as e:
        print(f"❌ JWT generation failed: {e}")
        return {"error": "jwt_generation_failed", "details": str(e)}
    
    # Step 3: Mint Installation Token
    print(f"\n🎫 Step 3: Minting Installation Token")
    
    try:
        install_token, install_info = get_installation_token(jwt_token, INSTALLATION_ID)
        print(f"✅ Installation Token minted")
        print(f"   Expires: {install_info['expires_at']}")
        print(f"   Duration: ~{install_info['expires_in_min']} minutes")
        print(f"   Permissions: {', '.join(install_info['permissions'].keys())}")
        if install_info['repositories']:
            print(f"   Repositories: {', '.join(install_info['repositories'])}")
    except Exception as e:
        print(f"❌ Installation Token minting failed: {e}")
        return {"error": "installation_token_failed", "details": str(e)}
    
    # Step 4: Smoke tests (READ-ONLY)
    print(f"\n🧪 Step 4: Smoke Tests (READ-ONLY)")
    
    smoke_results = smoke_test_readonly(install_token, OWNER, REPO)
    
    for test_name, test_result in smoke_results.items():
        print(f"\n   {test_name}: {test_result['status']}")
        if test_result['status'] == "✅ ok":
            for key, value in test_result.items():
                if key != 'status':
                    print(f"      {key}: {value}")
        else:
            print(f"      Error: {test_result.get('error', 'unknown')}")
    
    # Final Report
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "app_id": APP_ID,
        "installation_id": INSTALLATION_ID,
        "jwt": {
            "exp_minutes": jwt_info['exp_minutes'],
            "iat_offset_sec": jwt_info['iat_offset_sec'],
            "iat": jwt_info['iat_readable'],
            "exp": jwt_info['exp_readable']
        },
        "installation_token": {
            "expires_in_min": f"~{install_info['expires_in_min']}",
            "expires_at": install_info['expires_at'],
            "permissions": list(install_info['permissions'].keys()),
            "repositories": install_info['repositories']
        },
        "smoke": {
            test: result['status'] for test, result in smoke_results.items()
        },
        "smoke_details": smoke_results,
        "killswitch": [
            "Token expires automatically in ~1h",
            "Revoke key: https://github.com/settings/apps",
            "Rotate key: Generate new private key"
        ],
        "status": "✅ all_tests_passed" if all(
            r['status'] == "✅ ok" for r in smoke_results.values()
        ) else "⚠️ some_tests_failed"
    }
    
    print("\n" + "=" * 60)
    print("📊 FINAL REPORT (JSON)")
    print("=" * 60)
    print(json.dumps(report, indent=2))
    
    # Save to file if not in CI
    if os.environ.get('CI') != 'true':
        with open('app_auth_test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("\n✅ Results saved to: app_auth_test_results.json")
    
    return report

if __name__ == "__main__":
    result = main()
    
    # Exit code
    if isinstance(result, dict) and result.get('status') == "✅ all_tests_passed":
        sys.exit(0)
    else:
        sys.exit(1)
