#Requires -Version 5.1
<#
.SYNOPSIS
    MCP ps_exec dispatcher - Whitelisted PowerShell actions only
.DESCRIPTION
    Receives action + args from Node.js MCP server
    NO Invoke-Expression - hardcoded allowlist only
.NOTES
    ExecutionPolicy: Bypass for this process only
    Future: Migrate to AllSigned/RemoteSigned
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet(
        'dir','type','test_path','whoami','get_process',
        'get_service','get_env','test_connection',
        'get_item_property','measure_object','screenshot'
    )]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$ArgsJson = '{}'
)

# Force UTF-8 output
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::UTF8
$OutputEncoding = [System.Text.UTF8Encoding]::UTF8

# Error handling
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

try {
    # Parse arguments
    $args_obj = $ArgsJson | ConvertFrom-Json
    
    # Execute whitelisted action (NO INVOKE-EXPRESSION)
    switch ($Action) {
        'dir' {
            $path = $args_obj.path
            if (-not $path) { throw "Missing required parameter: path" }
            Get-ChildItem -Path $path | Format-Table -AutoSize | Out-String
        }
        
        'type' {
            $path = $args_obj.path
            if (-not $path) { throw "Missing required parameter: path" }
            Get-Content -Path $path -Raw
        }
        
        'test_path' {
            $path = $args_obj.path
            if (-not $path) { throw "Missing required parameter: path" }
            Test-Path -Path $path
        }
        
        'whoami' {
            $env:USERDOMAIN + '\\' + $env:USERNAME
        }
        
        'get_process' {
            if ($args_obj.name) {
                Get-Process -Name $args_obj.name | Format-Table -AutoSize | Out-String
            } else {
                Get-Process | Select-Object -First 20 | Format-Table -AutoSize | Out-String
            }
        }
        
        'get_service' {
            if ($args_obj.name) {
                Get-Service -Name $args_obj.name | Format-Table -AutoSize | Out-String
            } else {
                Get-Service | Select-Object -First 20 | Format-Table -AutoSize | Out-String
            }
        }
        
        'get_env' {
            if ($args_obj.name) {
                Get-ChildItem Env: | Where-Object Name -eq $args_obj.name | Out-String
            } else {
                Get-ChildItem Env: | Format-Table -AutoSize | Out-String
            }
        }
        
        'test_connection' {
            $host_val = $args_obj.host
            if (-not $host_val) { throw "Missing required parameter: host" }
            $count = if ($args_obj.count) { [int]$args_obj.count } else { 1 }
            Test-Connection -ComputerName $host_val -Count $count | Out-String
        }
        
        'get_item_property' {
            $path = $args_obj.path
            if (-not $path) { throw "Missing required parameter: path" }
            if ($args_obj.name) {
                Get-ItemProperty -Path $path -Name $args_obj.name | Out-String
            } else {
                Get-ItemProperty -Path $path | Out-String
            }
        }
        
        'measure_object' {
            $path = $args_obj.path
            if (-not $path) { throw "Missing required parameter: path" }
            $content = Get-Content -Path $path
            if ($args_obj.property) {
                $content | Measure-Object -Property $args_obj.property | Out-String
            } else {
                $content | Measure-Object -Line -Word -Character | Out-String
            }
        }
        
        'screenshot' {
            # Screenshot directory
            $screenshotDir = "C:\Users\edri2\Work\AI-Projects\Claude-Ops\screenshots"
            if (-not (Test-Path $screenshotDir)) {
                New-Item -ItemType Directory -Path $screenshotDir -Force | Out-Null
            }
            
            # Generate filename with timestamp
            $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
            $filename = "screenshot_$timestamp.png"
            $filepath = Join-Path $screenshotDir $filename
            
            # Take screenshot using .NET
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen
            $bounds = $screen.Bounds
            
            $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            
            $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
            
            $bitmap.Save($filepath, [System.Drawing.Imaging.ImageFormat]::Png)
            
            $graphics.Dispose()
            $bitmap.Dispose()
            
            # Return filepath as JSON
            @{
                success = $true
                filepath = $filepath
                filename = $filename
                timestamp = $timestamp
                resolution = "$($bounds.Width)x$($bounds.Height)"
            } | ConvertTo-Json
        }
        
        default {
            throw "Action '$Action' not implemented in dispatcher"
        }
    }
    
    exit 0
    
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
