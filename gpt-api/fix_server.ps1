# Fix Server Script
Write-Host "Fixing server.py..." -ForegroundColor Cyan

$sourceFile = "C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api\server.py"
$backupFile = "C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api\server.py.backup"

# Backup current
Copy-Item $sourceFile $backupFile -Force
Write-Host "✅ Backup created: server.py.backup" -ForegroundColor Green

# Download fixed version from Claude
Write-Host ""
Write-Host "Please download the fixed server.py from:" -ForegroundColor Yellow
Write-Host "computer:///mnt/user-data/outputs/server_fixed.py" -ForegroundColor White
Write-Host ""
Write-Host "Then save it as:" -ForegroundColor Yellow
Write-Host "$sourceFile" -ForegroundColor White
Write-Host ""
Write-Host "Or manually fix these lines in server.py:" -ForegroundColor Cyan
Write-Host "1. Remove duplicate code around lines 672-810" -ForegroundColor Gray
Write-Host "2. Remove orphaned 'except' block around line 672" -ForegroundColor Gray
Write-Host ""
Write-Host "After fixing, run: python server.py" -ForegroundColor Green
