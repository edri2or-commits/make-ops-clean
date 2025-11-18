# Start GPT API Server
Write-Host "Starting GPT API Server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: make-ops-clean" -ForegroundColor Green
Write-Host "API URL: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
python server.py
