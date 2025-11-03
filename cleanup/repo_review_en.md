## Repo Cleanup Structure Flow

This file is used to organize and manage the repository files to support the loop automations.

Recommended structure:

```make/ops-clean
`- agents/
    - mail_bot.py
    - form_filler.py
- services/
    - gmail_reader.py
    - make_api_wrapper.py
- utils/
    - json_utils.py
- workflows/
    - github_actions
- tests/
    - test_mail.py
```