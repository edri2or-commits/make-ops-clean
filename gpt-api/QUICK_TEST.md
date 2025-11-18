# Quick Token Automation Test

Create 3 tokens with automatic generation:
```
curl -X POST http://localhost:5000/tokens/auto-generate \
  -H "Content-Type: application/json" \
  -d '{"service": "TEST_API", "type": "api_key", "prefix": "test_", "length": 32}'
```

Or use PowerShell:
```powershell
$body = @{
    service = "TEST_API"
    type = "api_key"
    prefix = "test_"
    length = 32
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/tokens/auto-generate" -Method Post -Body $body -ContentType "application/json"
```

The token automation system is ready but server needs restart!
