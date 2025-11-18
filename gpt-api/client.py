#!/usr/bin/env python3
"""
MakeOpsClean API Client
Simple Python client for interacting with make-ops-clean repository
"""

import requests
from typing import Dict, Any, Optional


class MakeOpsCleanClient:
    """Client for make-ops-clean API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip("/")
    
    def _handle_response(self, resp: requests.Response) -> Any:
        """Handle API response and errors"""
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            msg = f"HTTP {resp.status_code}: {resp.text[:300]}"
            raise RuntimeError(msg) from e
        
        try:
            return resp.json()
        except ValueError:
            return resp.text
    
    # Health & Status
    def health(self) -> Dict[str, Any]:
        """Check API health"""
        resp = requests.get(f"{self.base_url}/health")
        return self._handle_response(resp)
    
    # Git Operations
    def git_status(self) -> Dict[str, Any]:
        """Get git status"""
        resp = requests.get(f"{self.base_url}/git/status")
        return self._handle_response(resp)
    
    def git_pull(self) -> Dict[str, Any]:
        """Pull latest changes"""
        resp = requests.post(f"{self.base_url}/git/pull")
        return self._handle_response(resp)
    
    def git_commit(self, message: str) -> Dict[str, Any]:
        """Commit and push changes"""
        resp = requests.post(
            f"{self.base_url}/git/commit",
            json={"message": message}
        )
        return self._handle_response(resp)
    
    # File Operations
    def list_files(self, path: str = "") -> Dict[str, Any]:
        """List files in directory"""
        resp = requests.get(
            f"{self.base_url}/files/list",
            params={"path": path}
        )
        return self._handle_response(resp)
    
    def read_file(self, path: str) -> str:
        """Read file content"""
        resp = requests.get(
            f"{self.base_url}/files/read",
            params={"path": path}
        )
        result = self._handle_response(resp)
        if isinstance(result, dict):
            return result.get("content", "")
        return result
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write file content"""
        resp = requests.post(
            f"{self.base_url}/files/write",
            json={"path": path, "content": content}
        )
        return self._handle_response(resp)
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """Delete file"""
        resp = requests.delete(
            f"{self.base_url}/files/delete",
            params={"path": path}
        )
        return self._handle_response(resp)
    
    # GitHub Actions
    def trigger_workflow(self, workflow: str) -> Dict[str, Any]:
        """Trigger GitHub Actions workflow"""
        resp = requests.post(
            f"{self.base_url}/actions/trigger",
            json={"workflow": workflow}
        )
        return self._handle_response(resp)
    
    def list_workflow_runs(self) -> Dict[str, Any]:
        """List recent workflow runs"""
        resp = requests.get(f"{self.base_url}/actions/list")
        return self._handle_response(resp)
    
    # Ops Commands
    def run_ops_command(self, command: str) -> Dict[str, Any]:
        """Run autopilot ops command"""
        resp = requests.post(
            f"{self.base_url}/ops/run",
            json={"command": command}
        )
        return self._handle_response(resp)
    
    # Convenience Methods
    def quick_update(self, path: str, content: str, message: str):
        """Update file and commit in one go"""
        self.write_file(path, content)
        return self.git_commit(message)
    
    def read_multiple(self, paths: list) -> Dict[str, str]:
        """Read multiple files at once"""
        results = {}
        for path in paths:
            try:
                results[path] = self.read_file(path)
            except Exception as e:
                results[path] = f"ERROR: {e}"
        return results


# Demo usage
if __name__ == "__main__":
    print("🚀 MakeOpsClean API Client Demo\n")
    
    client = MakeOpsCleanClient()
    
    # Check health
    print("1. Checking API health...")
    health = client.health()
    print(f"   Status: {health.get('status')}")
    print(f"   Repo: {health.get('repo')}\n")
    
    # Get git status
    print("2. Getting git status...")
    status = client.git_status()
    print(f"   {status.get('stdout', '')[:100]}...\n")
    
    # List files
    print("3. Listing root files...")
    files = client.list_files()
    items = files.get('items', [])
    print(f"   Found {len(items)} items")
    for item in items[:5]:
        print(f"   - [{item['type']}] {item['name']}")
    print("   ...\n")
    
    # Read a file
    print("4. Reading README.md (first 200 chars)...")
    content = client.read_file("README.md")
    print(f"   {content[:200]}...\n")
    
    print("✅ All operations successful!")
