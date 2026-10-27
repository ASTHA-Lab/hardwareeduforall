# Starts the course site and opens it in the default browser.
$site = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $site
$listener = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if (-not $listener) {
    Start-Process -FilePath python -ArgumentList "-m","http.server","8765","--bind","127.0.0.1" -WorkingDirectory $site -WindowStyle Minimized
    Start-Sleep -Seconds 1
}
Start-Process "http://127.0.0.1:8765/"
