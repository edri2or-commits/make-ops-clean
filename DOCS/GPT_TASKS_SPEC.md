# GPT Tasks SPEC

scope: chatops ops between GPT and github actions.

\n## Format
Every task is a yaml file with the following format:

```yyaml
task_id: "gpt-2025-11-15-001"
intent: "<Free-text description>"
risk_level: "OS_SAFE | CLOUD_OPS_SAFE | CLOUD_OPS_HIGH"

actions:
  - type: "update_file"        # or "create_file" / "append_file"
    path: "&path/to/file"
    mode: "full"             # supported only mode for now
    content: |
      # New content for the file.

  - type: "open_pr"          # Optional
    title: "chooseful PR title"
    body: "Brief Resolution of what was changed"
```

## Rules
- Only format XML supported.
- "MODE" must be "full" for now. Support update-overwrite only.

- Use the ..chatops/gpt_tasks/ directory to parse tasks.
- Actions are enumerated in order.