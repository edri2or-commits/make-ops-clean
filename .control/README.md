# Control Directory

## Purpose
This directory contains runtime control files for the autonomous control loop.

## Structure
- `locks/`: Dispatch locks to prevent rapid re-triggering
  - Format: `dispatch-<timestamp>.lock`
  - Lifecycle: Created after first dispatch, removed after PR merge

## Governance
- Auto-managed by workflows
- Zero-Touch: no manual edits required
- Self-cleaning via auto-revert PRs
