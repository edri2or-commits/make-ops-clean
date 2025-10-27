# Listener Stability — Test Plan (READ-ONLY)

goal: Verify that @SALAMTUKBOT routes to Make EU2 scenario 7598259 and remains stable.

prereq:
- Scenario 7598259 is ON
- “Immediately as data arrives” = ON

steps:
1) Pre-state: call GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo and save JSON (pre.json).
2) Trigger: send "ping" to @SALAMTUKBOT from any client.
3) Observe: Make → scenario 7598259 → History shows a new execution.
4) Post-state: call GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo again (post.json).

success:
- New execution appears within seconds in History.
- pre.result.url == post.result.url != "" and contains "hook.eu2.make.com".

failure:
- No execution in History OR result.url == "" OR result.url changed between pre and post.

notes:
- Read-only verification. Do NOT call deleteWebhook/setWebhook.
- If Privacy Mode is ON, direct messages to the bot are still delivered.
