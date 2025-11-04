# Rube Automation System

Rube operates runtime sequences to create, test, and repair workflow files in GitHub automatically.

## **Usage**
- Rube starts every full scheduled bootstrap routine on a regular basis
- Automatically runs steps from `rube-runner.py` with configuration loaded from `rube-meta.json`
- If steps fail - rube retries and tries again automatically
- Docs can be extended by user, or automatically updated by other rubemates
