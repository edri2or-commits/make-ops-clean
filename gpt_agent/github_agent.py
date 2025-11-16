from pathlib import Path
import argparse
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

DESIGN_PATH = ROOT / "DOCS" / "AGENT_GPT_MASTER_DESIGN.md"
SNAPSHOT_PATH = ROOT / "DOCS" / "STATE_FOR_GPT_SNAPSHOT.md"
MATRIX_PATH = ROOT / "CAPABILITIES_MATRIX.md"

def load_text(path: Path) -> str:
    if not path.exists():
        return f"[WARN] File not found: {path}\n"
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"[ERROR] Failed to read {path}: {e}\n"

def plan_github_task(intent: str) -> str:
    design = load_text(DESIGN_PATH)
    snapshot = load_text(SNAPSHOT_PATH)
    matrix = load_text(MATRIX_PATH)

    lines = []
    lines.append("# GPT GitHub Agent — DRY RUN PLAN")
    lines.append("")
    lines.append("## 1. Intent")
    lines.append(intent.strip() or "(no intent provided)")
    lines.append("")
    lines.append("## 2. Context Files Loaded")
    lines.append(f"- DESIGN:   {DESIGN_PATH}")
    lines.append(f"- SNAPSHOT: {SNAPSHOT_PATH}")
    lines.append(f"- MATRIX:   {MATRIX_PATH}")
    lines.append("")
    lines.append("## 3. Notes")
    lines.append("- This is a DRY RUN only.")
    lines.append("- No files are modified and no commits are created.")
    lines.append("- The agent is expected to follow AGENT_GPT_MASTER_DESIGN.md.")
    lines.append("")
    lines.append("## 4. High-level Next Steps (Conceptual)")
    lines.append("1. Classify the requested intent as OS_SAFE or CLOUD_OPS_HIGH based on CAPABILITIES_MATRIX.")
    lines.append("2. Identify which files would be affected (Docs/State vs. Code/Workflows).")
    lines.append("3. For OS_SAFE:")
    lines.append("   - Propose updates to Docs/State files only.")
    lines.append("4. For CLOUD_OPS_HIGH:")
    lines.append("   - Propose creating a dedicated branch and PR instead of direct commits to main.")
    lines.append("")
    lines.append("## 5. Implementation TODOs (for future versions)")
    lines.append("- Replace this static planner with a real LLM-backed planner.")
    lines.append("- Add logic to parse and update specific sections of the Docs/Matrix.")
    lines.append("- Integrate with GitHub via Actions or an external GPT-Agent service.")
    lines.append("")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="GPT GitHub Agent — DRY RUN planner")
    parser.add_argument(
        "--intent",
        type=str,
        required=True,
        help="High-level task description for the agent"
    )
    args = parser.parse_args()
    plan = plan_github_task(args.intent)
    print(plan)

if __name__ == "__main__":
    main()
