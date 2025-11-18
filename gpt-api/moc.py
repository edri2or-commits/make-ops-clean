#!/usr/bin/env python3
"""
MOC - Make-Ops-Clean CLI
Command line interface for managing make-ops-clean repository
"""

import argparse
import sys
from pathlib import Path
from client import MakeOpsCleanClient


def cmd_read(client, args):
    """Read and display file content"""
    content = client.read_file(args.path)
    print(content, end="")


def cmd_write(client, args):
    """Write content to file"""
    if args.from_stdin:
        content = sys.stdin.read()
    elif args.from_file:
        content = Path(args.from_file).read_text(encoding="utf-8")
    else:
        content = args.content
    
    result = client.write_file(args.path, content)
    print(f"✅ Written: {args.path}")
    if result.get('success'):
        print(f"   Path: {result['path']}")


def cmd_commit(client, args):
    """Commit and push changes"""
    result = client.git_commit(args.message)
    commit_info = result.get('commit', {})
    push_info = result.get('push', {})
    
    if commit_info.get('returncode') == 0:
        print("✅ Committed and pushed!")
        stdout = commit_info.get('stdout', '')
        if stdout:
            print(f"   {stdout.strip()}")
    else:
        print("❌ Commit failed")
        print(f"   {commit_info.get('stderr', '')}")


def cmd_status(client, args):
    """Show git status"""
    result = client.git_status()
    print(result.get('stdout', ''))


def cmd_pull(client, args):
    """Pull latest changes"""
    result = client.git_pull()
    print(result.get('stdout', ''))


def cmd_list(client, args):
    """List files in directory"""
    result = client.list_files(args.path or "")
    items = result.get('items', [])
    
    for item in items:
        icon = "[DIR]" if item['type'] == 'dir' else "[FILE]"
        print(f"{icon} {item['name']}")


def cmd_delete(client, args):
    """Delete file or directory"""
    if not args.force:
        confirm = input(f"Delete {args.path}? (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
    
    result = client.delete_file(args.path)
    if result.get('success'):
        print(f"✅ Deleted: {args.path}")
    else:
        print(f"❌ Failed to delete: {result.get('error')}")


def cmd_trigger(client, args):
    """Trigger GitHub Actions workflow"""
    result = client.trigger_workflow(args.workflow)
    print(f"✅ Triggered workflow: {args.workflow}")
    print(f"   {result.get('stdout', '')}")


def cmd_runs(client, args):
    """List recent workflow runs"""
    result = client.list_workflow_runs()
    print(result.get('stdout', ''))


def cmd_quick(client, args):
    """Quick update: write file and commit"""
    content = Path(args.from_file).read_text(encoding='utf-8')
    result = client.quick_update(args.path, content, args.message)
    print(f"✅ Updated and committed: {args.path}")


def cmd_health(client, args):
    """Check API health"""
    result = client.health()
    print(f"Status: {result.get('status')}")
    print(f"Repo: {result.get('repo')}")


def main():
    parser = argparse.ArgumentParser(
        prog="moc",
        description="Make-Ops-Clean CLI - Manage your repository from command line"
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:5000",
        help="API base URL"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # health
    subparsers.add_parser("health", help="Check API health")
    
    # status
    subparsers.add_parser("status", help="Show git status")
    
    # pull
    subparsers.add_parser("pull", help="Pull latest changes")
    
    # list
    p_list = subparsers.add_parser("list", help="List files")
    p_list.add_argument("path", nargs="?", default="", help="Directory path")
    
    # read
    p_read = subparsers.add_parser("read", help="Read file")
    p_read.add_argument("path", help="File path")
    
    # write
    p_write = subparsers.add_parser("write", help="Write to file")
    p_write.add_argument("path", help="File path")
    src = p_write.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-stdin", action="store_true", help="Read from stdin")
    src.add_argument("--from-file", help="Read from local file")
    src.add_argument("--content", help="Content as string")
    
    # delete
    p_delete = subparsers.add_parser("delete", help="Delete file")
    p_delete.add_argument("path", help="File path")
    p_delete.add_argument("-f", "--force", action="store_true", help="Skip confirmation")
    
    # commit
    p_commit = subparsers.add_parser("commit", help="Commit and push")
    p_commit.add_argument("message", help="Commit message")
    
    # trigger
    p_trigger = subparsers.add_parser("trigger", help="Trigger workflow")
    p_trigger.add_argument("workflow", help="Workflow name (e.g., index-append-manual.yml)")
    
    # runs
    subparsers.add_parser("runs", help="List recent workflow runs")
    
    # quick
    p_quick = subparsers.add_parser("quick", help="Quick update: write and commit")
    p_quick.add_argument("path", help="File path")
    p_quick.add_argument("--from-file", required=True, help="Local file")
    p_quick.add_argument("-m", "--message", required=True, help="Commit message")
    
    args = parser.parse_args()
    
    # Create client
    client = MakeOpsCleanClient(base_url=args.base_url)
    
    # Route to command
    commands = {
        "health": cmd_health,
        "status": cmd_status,
        "pull": cmd_pull,
        "list": cmd_list,
        "read": cmd_read,
        "write": cmd_write,
        "delete": cmd_delete,
        "commit": cmd_commit,
        "trigger": cmd_trigger,
        "runs": cmd_runs,
        "quick": cmd_quick,
    }
    
    try:
        command_func = commands[args.command]
        command_func(client, args)
    except Exception as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
