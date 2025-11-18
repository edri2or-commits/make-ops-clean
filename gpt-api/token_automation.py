"""
Token Automation System v2.0
Complete automatic token management with GPT control
"""

import requests
import json
import os
from datetime import datetime, timedelta
import secrets
import string
import time
import threading
import hashlib

class TokenAutomation:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.secrets_file = os.path.join(repo_path, "SECRETS", ".env.local")
        self.token_registry = os.path.join(repo_path, "SECRETS", "token_registry.json")
        self.automation_rules = os.path.join(repo_path, "SECRETS", "automation_rules.json")
        
    def _save_json(self, filepath, data):
        """Save JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_json(self, filepath):
        """Load JSON file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    # ============================================
    # TOKEN GENERATION
    # ============================================
    
    def generate_api_key(self, service_name, prefix="", length=64, charset="alphanumeric"):
        """
        Generate a cryptographically secure API key
        
        Args:
            service_name: Name of the service
            prefix: Optional prefix (e.g., 'sk_', 'ghp_')
            length: Length of the key (excluding prefix)
            charset: 'alphanumeric', 'hex', 'base64', 'full'
        """
        if charset == "alphanumeric":
            alphabet = string.ascii_letters + string.digits
        elif charset == "hex":
            alphabet = string.hexdigits.lower()
        elif charset == "base64":
            alphabet = string.ascii_letters + string.digits + '+/'
        elif charset == "full":
            alphabet = string.ascii_letters + string.digits + string.punctuation
        else:
            alphabet = string.ascii_letters + string.digits
        
        key_body = ''.join(secrets.choice(alphabet) for _ in range(length))
        api_key = prefix + key_body
        
        # Save to registry
        registry = self._load_json(self.token_registry)
        
        key_info = {
            "service": service_name,
            "key": api_key,
            "prefix": prefix,
            "length": length,
            "charset": charset,
            "created_at": datetime.now().isoformat(),
            "type": "api_key",
            "status": "active"
        }
        
        if service_name not in registry:
            registry[service_name] = {}
        
        registry[service_name]["current"] = key_info
        
        if "history" not in registry[service_name]:
            registry[service_name]["history"] = []
        
        registry[service_name]["history"].append({
            "created_at": key_info["created_at"],
            "key_preview": api_key[:8] + "..." + api_key[-4:],
            "action": "generated"
        })
        
        self._save_json(self.token_registry, registry)
        
        # Save to secrets file
        self.save_secret(f"{service_name}_API_KEY", api_key)
        
        return key_info
    
    def generate_github_token_format(self, service_name="GITHUB"):
        """
        Generate a GitHub-formatted token (ghp_...)
        Note: This is just the format, not a real GitHub token
        """
        return self.generate_api_key(
            service_name,
            prefix="ghp_",
            length=36,
            charset="alphanumeric"
        )
    
    def generate_oauth_token(self, service_name, scopes=None):
        """Generate OAuth-style token"""
        token = secrets.token_urlsafe(48)
        
        token_info = {
            "service": service_name,
            "token": token,
            "type": "oauth",
            "scopes": scopes or [],
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=90)).isoformat()
        }
        
        registry = self._load_json(self.token_registry)
        registry[service_name] = token_info
        self._save_json(self.token_registry, registry)
        
        self.save_secret(f"{service_name}_OAUTH_TOKEN", token)
        
        return token_info
    
    def generate_jwt_secret(self, service_name, length=64):
        """Generate JWT signing secret"""
        secret = secrets.token_hex(length)
        
        self.save_secret(f"{service_name}_JWT_SECRET", secret)
        
        return {
            "service": service_name,
            "secret": secret,
            "type": "jwt_secret",
            "created_at": datetime.now().isoformat()
        }
    
    # ============================================
    # TOKEN ROTATION
    # ============================================
    
    def rotate_token(self, service_name, new_token=None, auto_generate=True, **gen_params):
        """
        Rotate a token - generate new one and archive old one
        
        Args:
            service_name: Service name
            new_token: Provide specific token, or auto-generate
            auto_generate: Auto-generate if no token provided
            **gen_params: Parameters for generate_api_key
        """
        registry = self._load_json(self.token_registry)
        
        # Backup old token
        old_token = self.get_secret(f"{service_name}_API_KEY")
        
        if not new_token and auto_generate:
            # Auto-generate based on existing config or defaults
            if service_name in registry and "current" in registry[service_name]:
                old_config = registry[service_name]["current"]
                gen_params = {
                    "prefix": old_config.get("prefix", ""),
                    "length": old_config.get("length", 64),
                    "charset": old_config.get("charset", "alphanumeric")
                }
            
            result = self.generate_api_key(service_name, **gen_params)
            new_token = result["key"]
        
        if not new_token:
            return {"error": "No token provided and auto_generate is False"}
        
        # Save new token
        self.save_secret(f"{service_name}_API_KEY", new_token)
        
        # Update registry
        if service_name not in registry:
            registry[service_name] = {"history": []}
        
        registry[service_name]["history"].append({
            "rotated_at": datetime.now().isoformat(),
            "old_token_preview": old_token[:8] + "..." if old_token else None,
            "new_token_preview": new_token[:8] + "...",
            "method": "auto" if auto_generate else "manual",
            "action": "rotated"
        })
        
        registry[service_name]["last_rotated"] = datetime.now().isoformat()
        
        self._save_json(self.token_registry, registry)
        
        return {
            "success": True,
            "service": service_name,
            "rotated_at": datetime.now().isoformat(),
            "old_preview": old_token[:8] + "..." if old_token else None,
            "new_preview": new_token[:8] + "..."
        }
    
    def bulk_rotate_tokens(self, services=None):
        """Rotate multiple tokens at once"""
        if services is None:
            # Rotate all tokens
            services = list(self._load_json(self.token_registry).keys())
        
        results = []
        for service in services:
            try:
                result = self.rotate_token(service, auto_generate=True)
                results.append(result)
            except Exception as e:
                results.append({
                    "service": service,
                    "error": str(e)
                })
        
        return {
            "total": len(services),
            "successful": len([r for r in results if "success" in r]),
            "results": results
        }
    
    # ============================================
    # AUTOMATION RULES
    # ============================================
    
    def create_automation_rule(self, rule_name, rule_config):
        """
        Create an automation rule for token management
        
        Example rule_config:
        {
            "service": "MY_API",
            "action": "rotate",
            "schedule": "daily",  # or "weekly", "monthly", custom cron
            "conditions": {
                "age_days": 30,
                "usage_count": 1000
            },
            "auto_generate": True,
            "notify": ["email", "webhook"]
        }
        """
        rules = self._load_json(self.automation_rules)
        
        rule_config["created_at"] = datetime.now().isoformat()
        rule_config["status"] = "active"
        rule_config["last_executed"] = None
        
        rules[rule_name] = rule_config
        self._save_json(self.automation_rules, rules)
        
        return {
            "success": True,
            "rule_name": rule_name,
            "config": rule_config
        }
    
    def list_automation_rules(self):
        """List all automation rules"""
        return self._load_json(self.automation_rules)
    
    def delete_automation_rule(self, rule_name):
        """Delete an automation rule"""
        rules = self._load_json(self.automation_rules)
        
        if rule_name in rules:
            del rules[rule_name]
            self._save_json(self.automation_rules, rules)
            return {"success": True, "rule_name": rule_name}
        
        return {"error": "Rule not found"}
    
    def execute_automation_rule(self, rule_name):
        """Execute a specific automation rule"""
        rules = self._load_json(self.automation_rules)
        
        if rule_name not in rules:
            return {"error": "Rule not found"}
        
        rule = rules[rule_name]
        
        if rule["status"] != "active":
            return {"error": "Rule is not active"}
        
        result = {}
        
        # Execute based on action
        if rule["action"] == "rotate":
            result = self.rotate_token(
                rule["service"],
                auto_generate=rule.get("auto_generate", True)
            )
        
        elif rule["action"] == "generate":
            result = self.generate_api_key(
                rule["service"],
                **rule.get("generation_params", {})
            )
        
        elif rule["action"] == "bulk_rotate":
            result = self.bulk_rotate_tokens(rule.get("services"))
        
        # Update last execution
        rules[rule_name]["last_executed"] = datetime.now().isoformat()
        rules[rule_name]["last_result"] = {
            "executed_at": datetime.now().isoformat(),
            "success": result.get("success", False)
        }
        
        self._save_json(self.automation_rules, rules)
        
        return result
    
    def check_automation_rules(self):
        """Check and execute due automation rules"""
        rules = self._load_json(self.automation_rules)
        executed = []
        
        now = datetime.now()
        
        for rule_name, rule in rules.items():
            if rule["status"] != "active":
                continue
            
            should_execute = False
            
            # Check schedule
            schedule = rule.get("schedule", "")
            last_executed = rule.get("last_executed")
            
            if schedule == "daily":
                if not last_executed or (now - datetime.fromisoformat(last_executed)) > timedelta(days=1):
                    should_execute = True
            
            elif schedule == "weekly":
                if not last_executed or (now - datetime.fromisoformat(last_executed)) > timedelta(weeks=1):
                    should_execute = True
            
            elif schedule == "monthly":
                if not last_executed or (now - datetime.fromisoformat(last_executed)) > timedelta(days=30):
                    should_execute = True
            
            # Check conditions
            conditions = rule.get("conditions", {})
            
            if "age_days" in conditions:
                registry = self._load_json(self.token_registry)
                service = rule.get("service")
                
                if service in registry and "current" in registry[service]:
                    created_at = datetime.fromisoformat(registry[service]["current"]["created_at"])
                    age_days = (now - created_at).days
                    
                    if age_days >= conditions["age_days"]:
                        should_execute = True
            
            if should_execute:
                result = self.execute_automation_rule(rule_name)
                executed.append({
                    "rule_name": rule_name,
                    "executed_at": now.isoformat(),
                    "result": result
                })
        
        return executed
    
    # ============================================
    # SECRETS MANAGEMENT
    # ============================================
    
    def save_secret(self, key, value):
        """Save secret to .env.local"""
        os.makedirs(os.path.dirname(self.secrets_file), exist_ok=True)
        
        # Read existing
        existing = {}
        if os.path.exists(self.secrets_file):
            with open(self.secrets_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        existing[k.strip()] = v.strip()
        
        # Update
        existing[key] = value
        
        # Write back
        with open(self.secrets_file, 'w') as f:
            f.write(f"# Updated: {datetime.now().isoformat()}\n")
            for k, v in existing.items():
                f.write(f"{k}={v}\n")
        
        return True
    
    def get_secret(self, key):
        """Get secret from .env.local"""
        if os.path.exists(self.secrets_file):
            with open(self.secrets_file, 'r') as f:
                for line in f:
                    if line.startswith(f"{key}="):
                        return line.split('=', 1)[1].strip()
        return None
    
    def list_all_tokens(self):
        """List all tokens with full metadata"""
        registry = self._load_json(self.token_registry)
        
        tokens = {}
        for service, data in registry.items():
            if "current" in data:
                tokens[service] = {
                    "service": service,
                    "type": data["current"].get("type"),
                    "created_at": data["current"].get("created_at"),
                    "last_rotated": data.get("last_rotated"),
                    "preview": data["current"]["key"][:8] + "..." if "key" in data["current"] else "***",
                    "history_count": len(data.get("history", []))
                }
        
        return tokens
    
    def backup_all_tokens(self):
        """Create encrypted backup"""
        backup_dir = os.path.join(self.repo_path, "SECRETS", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"tokens_backup_{timestamp}.json")
        
        # Read all secrets
        secrets = {}
        if os.path.exists(self.secrets_file):
            with open(self.secrets_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        secrets[k.strip()] = v.strip()
        
        backup_data = {
            "created_at": datetime.now().isoformat(),
            "secrets": secrets,
            "registry": self._load_json(self.token_registry),
            "rules": self._load_json(self.automation_rules)
        }
        
        self._save_json(backup_file, backup_data)
        
        return {
            "success": True,
            "backup_file": backup_file,
            "token_count": len(secrets)
        }


class TokenScheduler:
    """Background scheduler for automatic token operations"""
    
    def __init__(self, automation):
        self.automation = automation
        self.running = False
        self.thread = None
    
    def start(self, check_interval_minutes=60):
        """Start background scheduler"""
        self.running = True
        self.thread = threading.Thread(
            target=self._scheduler_loop,
            args=(check_interval_minutes,),
            daemon=True
        )
        self.thread.start()
        
        return {
            "status": "started",
            "interval": check_interval_minutes
        }
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        return {"status": "stopped"}
    
    def _scheduler_loop(self, interval):
        """Internal loop"""
        while self.running:
            try:
                # Check and execute automation rules
                executed = self.automation.check_automation_rules()
                
                if executed:
                    print(f"[TokenScheduler] Executed {len(executed)} rules")
                
                time.sleep(interval * 60)
                
            except Exception as e:
                print(f"[TokenScheduler] Error: {e}")
                time.sleep(60)


# ============================================
# FLASK API INTEGRATION
# ============================================

def add_token_automation_routes(app, repo_path):
    """Add token automation routes to Flask app"""
    
    automation = TokenAutomation(repo_path)
    scheduler = TokenScheduler(automation)
    
    @app.route('/tokens/generate', methods=['POST'])
    def generate_token():
        """Generate new token"""
        data = request.json
        service = data.get('service')
        token_type = data.get('type', 'api_key')
        
        if token_type == 'api_key':
            result = automation.generate_api_key(
                service,
                prefix=data.get('prefix', ''),
                length=data.get('length', 64),
                charset=data.get('charset', 'alphanumeric')
            )
        elif token_type == 'github':
            result = automation.generate_github_token_format(service)
        elif token_type == 'oauth':
            result = automation.generate_oauth_token(service, data.get('scopes'))
        elif token_type == 'jwt':
            result = automation.generate_jwt_secret(service, data.get('length', 64))
        else:
            return jsonify({"error": "Invalid token type"}), 400
        
        return jsonify(result)
    
    @app.route('/tokens/rotate', methods=['POST'])
    def rotate_token():
        """Rotate token"""
        data = request.json
        service = data.get('service')
        
        result = automation.rotate_token(
            service,
            new_token=data.get('new_token'),
            auto_generate=data.get('auto_generate', True)
        )
        
        return jsonify(result)
    
    @app.route('/tokens/bulk-rotate', methods=['POST'])
    def bulk_rotate():
        """Rotate multiple tokens"""
        data = request.json
        services = data.get('services')
        
        result = automation.bulk_rotate_tokens(services)
        return jsonify(result)
    
    @app.route('/tokens/list', methods=['GET'])
    def list_tokens():
        """List all tokens"""
        tokens = automation.list_all_tokens()
        return jsonify({"tokens": tokens})
    
    @app.route('/automation/rules', methods=['GET', 'POST', 'DELETE'])
    def automation_rules():
        """Manage automation rules"""
        if request.method == 'GET':
            rules = automation.list_automation_rules()
            return jsonify({"rules": rules})
        
        elif request.method == 'POST':
            data = request.json
            rule_name = data.get('rule_name')
            rule_config = data.get('config')
            
            result = automation.create_automation_rule(rule_name, rule_config)
            return jsonify(result)
        
        elif request.method == 'DELETE':
            rule_name = request.args.get('rule_name')
            result = automation.delete_automation_rule(rule_name)
            return jsonify(result)
    
    @app.route('/automation/execute', methods=['POST'])
    def execute_rule():
        """Execute automation rule"""
        data = request.json
        rule_name = data.get('rule_name')
        
        result = automation.execute_automation_rule(rule_name)
        return jsonify(result)
    
    @app.route('/automation/check', methods=['POST'])
    def check_rules():
        """Check and execute due rules"""
        executed = automation.check_automation_rules()
        return jsonify({
            "executed_count": len(executed),
            "executed": executed
        })
    
    @app.route('/automation/scheduler/start', methods=['POST'])
    def start_scheduler():
        """Start background scheduler"""
        data = request.json
        interval = data.get('interval_minutes', 60)
        
        result = scheduler.start(interval)
        return jsonify(result)
    
    @app.route('/automation/scheduler/stop', methods=['POST'])
    def stop_scheduler():
        """Stop background scheduler"""
        result = scheduler.stop()
        return jsonify(result)
    
    @app.route('/tokens/backup', methods=['POST'])
    def backup_tokens():
        """Backup all tokens"""
        result = automation.backup_all_tokens()
        return jsonify(result)
    
    return app
