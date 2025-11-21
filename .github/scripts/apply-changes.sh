#!/bin/bash

#################################################################
# apply-changes.sh
# Purpose: Validate changes after merge (placeholder for L1.2)
# Usage: ./apply-changes.sh <task_id>
#################################################################

set -euo pipefail

TASK_ID="${1:-unknown}"

echo "🔍 Validating changes for task: $TASK_ID"

# Get list of changed files in last commit
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

echo "📋 Changed files:"
echo "$CHANGED_FILES"

# Basic validation checks
ERROR_COUNT=0

# Check 1: Verify YAML syntax for workflow files
for file in $CHANGED_FILES; do
  if [[ "$file" =~ \.ya?ml$ ]]; then
    echo "🔍 Validating YAML: $file"
    if ! python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
      echo "❌ Invalid YAML: $file"
      ((ERROR_COUNT++))
    else
      echo "✅ Valid YAML: $file"
    fi
  fi
done

# Check 2: Verify shell scripts are executable
for file in $CHANGED_FILES; do
  if [[ "$file" =~ \.sh$ ]]; then
    if [ ! -x "$file" ]; then
      echo "⚠️  Setting executable: $file"
      chmod +x "$file"
    fi
    
    echo "🔍 Checking shell syntax: $file"
    if ! bash -n "$file"; then
      echo "❌ Syntax error in: $file"
      ((ERROR_COUNT++))
    else
      echo "✅ Valid shell script: $file"
    fi
  fi
done

# Check 3: Verify no secrets in files
echo "🔐 Checking for secrets..."
PATTERNS=(
  "ghp_[a-zA-Z0-9]{36}"        # GitHub PAT
  "[0-9]{9,10}:[A-Za-z0-9_-]+" # Telegram Bot Token
  "-----BEGIN.*PRIVATE KEY-----" # Private keys
)

for file in $CHANGED_FILES; do
  for pattern in "${PATTERNS[@]}"; do
    if grep -qP "$pattern" "$file" 2>/dev/null; then
      echo "❌ Potential secret found in: $file"
      ((ERROR_COUNT++))
    fi
  done
done

# Summary
if [ $ERROR_COUNT -eq 0 ]; then
  echo "✅ All validations passed"
  echo "Task $TASK_ID: VALIDATED"
  exit 0
else
  echo "❌ Validation failed with $ERROR_COUNT errors"
  echo "Task $TASK_ID: FAILED"
  exit 1
fi

#################################################################
# Future Enhancements (L2+):
# - Run integration tests
# - Terraform plan/apply validation
# - Database migration checks
# - API endpoint health checks
# - Performance benchmarks
#################################################################
