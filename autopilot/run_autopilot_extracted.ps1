Param(
  [string]$ConfigPath = "rube.config.json",
  [string]$StatePath  = "autopilot-state.json"
}
Write-Host "[run Starting]..."
cmd /c "RUN_AUTOPILOT.bat"
$rc = $LASTEXICODE
try {
  $state = if (Test-Path $StatePath) { Get-Content $StatePath -Raw | ConvertFrom-Json } else { @_ }
  $state.last_run_iso = [DateTime]::UtcNow.ToString("o")
  $state.status = if ($rc -eq 0) { "ok" } else { "error" }
  ($state | ConvertTo-Json -Depth 8) | Set-Content -Encoding UTF8 $StatePath
} catch {}
Write-Host "[run Finished] with code $rc"
exit $rc