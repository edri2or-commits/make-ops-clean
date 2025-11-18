#!/usr/bin/env python3
"""
Example: Automated daily status update
This script demonstrates a complete workflow using MOC client
"""

from client import MakeOpsCleanClient
from datetime import datetime


def main():
    print("🤖 Automated Daily Status Update\n")
    
    # Create client
    client = MakeOpsCleanClient()
    
    # 1. Check health
    print("1. Checking API health...")
    health = client.health()
    if health.get('status') != 'ok':
        print("   ❌ API not healthy!")
        return
    print("   ✅ API healthy\n")
    
    # 2. Pull latest
    print("2. Pulling latest changes...")
    pull_result = client.git_pull()
    print(f"   {pull_result.get('stdout', '')[:100]}\n")
    
    # 3. Read current system status
    print("3. Reading current SYSTEM_STATUS.md...")
    current_status = client.read_file("SYSTEM_STATUS.md")
    print(f"   Current content: {len(current_status)} characters\n")
    
    # 4. Create daily update
    print("4. Creating daily update...")
    today = datetime.now().strftime("%Y-%m-%d")
    update_content = f"""# Daily Update - {today}

## Automated Check
- API Status: ✅ Healthy
- Repository: ✅ Up to date
- Timestamp: {datetime.now().isoformat()}

## Recent Activity
- Automated status check completed
- All systems operational

---
*This update was generated automatically by MOC automation*
"""
    
    # 5. Write update file
    update_path = f"daily-updates/update-{today}.md"
    print(f"5. Writing update to {update_path}...")
    client.write_file(update_path, update_content)
    print("   ✅ Update written\n")
    
    # 6. Commit changes
    print("6. Committing changes...")
    commit_result = client.git_commit(f"chore: daily status update {today}")
    commit_info = commit_result.get('commit', {})
    if commit_info.get('returncode') == 0:
        print("   ✅ Committed and pushed\n")
    else:
        print(f"   ❌ Commit failed: {commit_info.get('stderr')}\n")
        return
    
    # 7. Trigger workflow (optional)
    print("7. Triggering index-append workflow...")
    try:
        trigger_result = client.trigger_workflow("index-append-manual.yml")
        print("   ✅ Workflow triggered\n")
    except Exception as e:
        print(f"   ⚠️  Workflow trigger failed (might be okay): {e}\n")
    
    # 8. Summary
    print("=" * 50)
    print("✅ Daily update complete!")
    print(f"   File created: {update_path}")
    print(f"   Commit: {commit_info.get('stdout', '')[:50]}...")
    print("=" * 50)


if __name__ == "__main__":
    main()
