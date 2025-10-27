change=Enable "Watch updates (instant)" in scenario 7598259
window=10m ; owner=<you> ; chat=@SALAMTUKBOT
success=Make History shows new Execution ; getWebhookInfo.url != ""
fail_if=no execution OR url==""
rollback=Scenario 7598259 -> OFF
