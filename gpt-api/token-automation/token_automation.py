# NOTE: LAB / EXPERIMENTAL. Not part of GPT_CONTROL_API_V1. Do not use in production flows yet.
# This module provides advanced token automation including rotation, scheduling, and bulk operations.
# For basic token generation, use the /tokens/generate endpoint in GPT_CONTROL_API_V1.

"""
Token Automation System
Automatically generates, rotates, and manages tokens
"""

import os
import json
import secrets
import string
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import schedule
import time
import hashlib

class TokenAutomation:
    def __init__(self, config_file="token_config.json"):
        self.config_file = config_file
        self.api_url = "http://localhost:5000"
        self.load_config()
        
    def load_config(self):
        """Load token automation configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "tokens": {},
                "rotation_rules": {},
                "history": []
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    # ============================================
    # TOKEN GENERATION
    # ============================================
    
    def generate_token(self, token_type: str, length: int = 32, 
                       prefix: str = "", include_special: bool = True) -> str:
        """
        Generate a secure random token
        
        Args:
            token_type: Type of token (api_key, secret, password, etc)
            length: Length of token
            prefix: Prefix for token (e.g., 'ghp_', 'sk-')
            include_special: Include special characters
        """
        if include_special:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
        else:
            chars = string.ascii_letters + string.digits
        
        token = prefix + ''.join(secrets.choice(chars) for _ in range(length))
        
        # Store metadata
        self.config["tokens"][token_type] = {
            "value": token,
            "created_at": datetime.now().isoformat(),
            "last_rotated": datetime.now().isoformat(),
            "rotation_count": 0,
            "hash": hashlib.sha256(token.encode()).hexdigest()
        }
        self.save_config()
        
        return token
    
    def generate_github_token_format(self) -> str:
        """Generate a GitHub-like token format"""
        # GitHub Personal Access Token format: ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        return self.generate_token(
            "github_pat",
            length=40,
            prefix="ghp_",
            include_special=False
        )
    
    def generate_api_key(self, service: str) -> str:
        """Generate API key for a service"""
        return self.generate_token(
            f"api_key_{service}",
            length=32,
            prefix=f"{service[:2].upper()}_",
            include_special=False
        )
    
    def generate_secret_key(self, purpose: str) -> str:
        """Generate a secret key"""
        return self.generate_token(
            f"secret_{purpose}",
            length=64,
            include_special=True
        )
    
    # ============================================
    # TOKEN ROTATION
    # ============================================
    
    def setup_rotation_rule(self, token_name: str, interval_hours: int = 24,
                           auto_rotate: bool = True, notify: bool = True):
        """
        Setup automatic token rotation rule
        
        Args:
            token_name: Name of token to rotate
            interval_hours: Hours between rotations
            auto_rotate: Automatically rotate
            notify: Notify when rotated
        """
        self.config["rotation_rules"][token_name] = {
            "interval_hours": interval_hours,
            "auto_rotate": auto_rotate,
            "notify": notify,
            "next_rotation": (datetime.now() + timedelta(hours=interval_hours)).isoformat(),
            "created_at": datetime.now().isoformat()
        }
        self.save_config()
        
        print(f"✅ Rotation rule set for {token_name}: every {interval_hours} hours")
    
    def rotate_token(self, token_name: str, new_token: Optional[str] = None) -> Dict:
        """
        Rotate a token (generate new one and update everywhere)
        
        Args:
            token_name: Name of token to rotate
            new_token: Specific new token (if None, generates one)
        """
        # Get old token
        old_token = self.config["tokens"].get(token_name, {}).get("value")
        
        # Generate or use provided token
        if new_token is None:
            if "github" in token_name.lower():
                new_token = self.generate_github_token_format()
            elif "api_key" in token_name.lower():
                service = token_name.split("_")[-1]
                new_token = self.generate_api_key(service)
            else:
                new_token = self.generate_secret_key(token_name)
        
        # Update in secrets via API
        response = requests.post(f"{self.api_url}/secrets/set", json={
            "key": token_name,
            "value": new_token,
            "location": "all"
        })
        
        # Update local config
        if token_name in self.config["tokens"]:
            self.config["tokens"][token_name]["rotation_count"] += 1
        else:
            self.config["tokens"][token_name] = {"rotation_count": 0}
        
        self.config["tokens"][token_name].update({
            "value": new_token,
            "last_rotated": datetime.now().isoformat(),
            "hash": hashlib.sha256(new_token.encode()).hexdigest(),
            "previous_hash": hashlib.sha256(old_token.encode()).hexdigest() if old_token else None
        })
        
        # Add to history
        self.config["history"].append({
            "token_name": token_name,
            "action": "rotated",
            "timestamp": datetime.now().isoformat(),
            "old_hash": hashlib.sha256(old_token.encode()).hexdigest() if old_token else None,
            "new_hash": hashlib.sha256(new_token.encode()).hexdigest()
        })
        
        self.save_config()
        
        # Commit changes to git
        self.commit_rotation(token_name)
        
        return {
            "success": True,
            "token_name": token_name,
            "new_token": new_token,
            "rotated_at": datetime.now().isoformat(),
            "api_response": response.json() if response.ok else None
        }
    
    def commit_rotation(self, token_name: str):
        """Commit token rotation to git"""
        try:
            response = requests.post(f"{self.api_url}/git/commit", json={
                "message": f"[Security] Rotate {token_name}",
                "push": True
            })
            return response.json()
        except Exception as e:
            print(f"Warning: Could not commit rotation: {e}")
    
    def check_and_rotate(self):
        """Check all tokens and rotate if needed"""
        now = datetime.now()
        
        for token_name, rule in self.config["rotation_rules"].items():
            if not rule["auto_rotate"]:
                continue
            
            next_rotation = datetime.fromisoformat(rule["next_rotation"])
            
            if now >= next_rotation:
                print(f"🔄 Auto-rotating {token_name}...")
                result = self.rotate_token(token_name)
                
                # Update next rotation
                rule["next_rotation"] = (now + timedelta(hours=rule["interval_hours"])).isoformat()
                self.save_config()
                
                if rule["notify"]:
                    self.notify_rotation(token_name, result)
    
    def notify_rotation(self, token_name: str, result: Dict):
        """Notify about token rotation"""
        print(f"""
╔══════════════════════════════════════════╗
║  🔐 TOKEN ROTATED                        ║
╠══════════════════════════════════════════╣
║  Token: {token_name:<30} ║
║  Time:  {result['rotated_at']:<30} ║
║  Hash:  {result['new_token'][:8]}...        ║
╚══════════════════════════════════════════╝
        """)
    
    # ============================================
    # AUTOMATION WORKFLOWS
    # ============================================
    
    def setup_auto_rotation_schedule(self):
        """Setup automatic rotation scheduler"""
        # Check every hour
        schedule.every().hour.do(self.check_and_rotate)
        
        print("🤖 Auto-rotation scheduler started!")
        print("   Checking every hour for tokens to rotate...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def create_rotation_workflow(self, workflow_name: str, tokens: List[str], 
                                 schedule_cron: str):
        """
        Create a custom rotation workflow
        
        Args:
            workflow_name: Name of workflow
            tokens: List of tokens to rotate
            schedule_cron: Cron-style schedule
        """
        workflow = {
            "name": workflow_name,
            "tokens": tokens,
            "schedule": schedule_cron,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "run_count": 0
        }
        
        if "workflows" not in self.config:
            self.config["workflows"] = {}
        
        self.config["workflows"][workflow_name] = workflow
        self.save_config()
        
        print(f"✅ Workflow '{workflow_name}' created!")
    
    def run_workflow(self, workflow_name: str):
        """Run a specific workflow"""
        if workflow_name not in self.config.get("workflows", {}):
            return {"error": "Workflow not found"}
        
        workflow = self.config["workflows"][workflow_name]
        results = []
        
        print(f"🚀 Running workflow: {workflow_name}")
        
        for token in workflow["tokens"]:
            print(f"   Rotating {token}...")
            result = self.rotate_token(token)
            results.append(result)
        
        # Update workflow stats
        workflow["last_run"] = datetime.now().isoformat()
        workflow["run_count"] += 1
        self.save_config()
        
        return {
            "workflow": workflow_name,
            "results": results,
            "completed_at": datetime.now().isoformat()
        }
    
    # ============================================
    # SMART FEATURES
    # ============================================
    
    def analyze_token_health(self) -> Dict:
        """Analyze health of all tokens"""
        health = {
            "total_tokens": len(self.config["tokens"]),
            "needs_rotation": [],
            "recently_rotated": [],
            "never_rotated": [],
            "high_risk": []
        }
        
        now = datetime.now()
        
        for name, token in self.config["tokens"].items():
            last_rotated = datetime.fromisoformat(token["last_rotated"])
            age_hours = (now - last_rotated).total_seconds() / 3600
            
            if age_hours > 168:  # 1 week
                health["needs_rotation"].append(name)
            elif age_hours < 24:
                health["recently_rotated"].append(name)
            
            if token["rotation_count"] == 0:
                health["never_rotated"].append(name)
            
            if age_hours > 720:  # 30 days
                health["high_risk"].append(name)
        
        return health
    
    def suggest_rotations(self) -> List[str]:
        """Suggest which tokens should be rotated"""
        health = self.analyze_token_health()
        suggestions = []
        
        if health["high_risk"]:
            suggestions.append("⚠️  HIGH PRIORITY: " + ", ".join(health["high_risk"]))
        
        if health["needs_rotation"]:
            suggestions.append("📋 Should rotate: " + ", ".join(health["needs_rotation"]))
        
        if health["never_rotated"]:
            suggestions.append("🆕 Never rotated: " + ", ".join(health["never_rotated"]))
        
        return suggestions
    
    def get_status(self) -> Dict:
        """Get full automation status"""
        return {
            "tokens": self.config["tokens"],
            "rules": self.config["rotation_rules"],
            "workflows": self.config.get("workflows", {}),
            "history": self.config["history"][-10:],  # Last 10 events
            "health": self.analyze_token_health(),
            "suggestions": self.suggest_rotations()
        }


# ============================================
# CLI Interface
# ============================================

if __name__ == "__main__":
    import sys
    
    ta = TokenAutomation()
    
    if len(sys.argv) < 2:
        print("""
Token Automation System
Usage:
    python token_automation.py generate <type> [options]
    python token_automation.py rotate <token_name>
    python token_automation.py setup-rule <token_name> <hours>
    python token_automation.py start-scheduler
    python token_automation.py status
    python token_automation.py health
    python token_automation.py suggest
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        token_type = sys.argv[2] if len(sys.argv) > 2 else "api_key"
        token = ta.generate_token(token_type)
        print(f"Generated token: {token}")
    
    elif command == "rotate":
        token_name = sys.argv[2]
        result = ta.rotate_token(token_name)
        print(f"✅ Rotated {token_name}")
        print(f"   New token: {result['new_token']}")
    
    elif command == "setup-rule":
        token_name = sys.argv[2]
        hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        ta.setup_rotation_rule(token_name, hours)
    
    elif command == "start-scheduler":
        print("Starting auto-rotation scheduler...")
        ta.setup_auto_rotation_schedule()
    
    elif command == "status":
        status = ta.get_status()
        print(json.dumps(status, indent=2))
    
    elif command == "health":
        health = ta.analyze_token_health()
        print(json.dumps(health, indent=2))
    
    elif command == "suggest":
        suggestions = ta.suggest_rotations()
        for s in suggestions:
            print(s)
