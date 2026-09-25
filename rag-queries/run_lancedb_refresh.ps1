# run_lancedb_refresh.ps1 — detached full-88 LanceDB backfill with per-class
# checkpointing. Loads permanent AWS creds from rag-service/.env, then runs
# backfill_all_queries.py --source lancedb --refresh once per class.
#
# Resume: classes completed successfully are recorded in
# rag-queries/refresh_logs/done.txt; re-running skips them. Failed classes
# are retried (up to $Retries per class, each with a hard timeout — protects
# against SentenceTransformer HF-Hub download stalls that hang forever).
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File run_lancedb_refresh.ps1
$ErrorActionPreference = "Continue"
$root   = "C:\Users\think\Project_v2\drug-quantification-framework"
$script = Join-Path $root "rag-queries\backfill_all_queries.py"
$envFile = "C:\Users\think\Project_v2\LocalNotebook\rag-service\.env"
$logDir = Join-Path $root "rag-queries\refresh_logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

# Per-class budget: a class takes ~20 min (fresh model load + ~33 drugs x 8
# queries). Allow 30 min of wall clock, then kill the python child and treat
# the class as failed (it will be retried / resumed on next run).
$ClassTimeoutSec = 1800
$Retries = 1

# --- load permanent AWS creds from .env ---
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)\s*=\s*(.+)\s*$') {
        Set-Item -Path "env:$($matches[1])" -Value $matches[2].Trim('"').Trim("'")
    }
}
if (-not $env:AWS_ACCESS_KEY_ID -or -not $env:AWS_SECRET_ACCESS_KEY) {
    Write-Host "FATAL: AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY not loaded from $envFile"
    exit 1
}

$classes = @("Antihypertensive","Diabetes","NSAID","Statin","PPI","H2RA",
             "Antacid","Alginate","Mucosal Protectant")
$doneFile = Join-Path $logDir "done.txt"
$done = @()
if (Test-Path $doneFile) { $done = Get-Content $doneFile }
$failed = @()

function Invoke-Class {
    param($Cls, $Log)
    # Run python as a child process; poll until exit or timeout, then kill.
    $p = Start-Process -FilePath "python" -ArgumentList @($script,"--source","lancedb","--refresh","--class",$Cls) `
         -NoNewWindow -RedirectStandardOutput $Log -RedirectStandardError "$Log.err" -PassThru
    $deadline = (Get-Date).AddSeconds($ClassTimeoutSec)
    while (-not $p.HasExited) {
        if ((Get-Date) -gt $deadline) {
            Write-Host ("    [timeout after {0}s] killing python {1}" -f $ClassTimeoutSec, $p.Id)
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 3
            return $false
        }
        Start-Sleep -Seconds 10
    }
    return ($p.ExitCode -eq 0)
}

foreach ($cls in $classes) {
    if ($done -contains $cls) {
        Write-Host ("[{0:HH:mm:ss}] SKIP (already done): {1}" -f (Get-Date), $cls)
        continue
    }
    $log = Join-Path $logDir ("class_" + ($cls -replace '[^A-Za-z0-9]','_') + ".log")
    $ok = $false
    for ($try = 0; $try -le $Retries; $try++) {
        Write-Host ("[{0:HH:mm:ss}] START (try {1}/{2}): {3} -> {4}" -f (Get-Date), ($try+1), ($Retries+1), $cls, $log)
        $ok = Invoke-Class $cls $log
        if ($ok) { break }
        Write-Host ("[{0:HH:mm:ss}] class {1} not OK (try {2}); {3}" -f (Get-Date), $cls, ($try+1),
                    $(if ($try -lt $Retries) { "retrying in 20s..." } else { "giving up for now" }))
        Start-Sleep -Seconds 20
    }
    if ($ok) {
        Add-Content $doneFile $cls
        Write-Host ("[{0:HH:mm:ss}] DONE: {1}" -f (Get-Date), $cls)
    } else {
        $failed += $cls
    }
}

Write-Host "==== BATCH COMPLETE $(Get-Date -Format 'HH:mm:ss') ===="
if ($failed.Count) { Write-Host "FAILED CLASSES: $($failed -join ', ')" }
else               { Write-Host "ALL CLASSES DONE" }
