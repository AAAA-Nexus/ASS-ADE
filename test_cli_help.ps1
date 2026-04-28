$commands = @("scout", "ui", "wakeup", "wire", "cherry-pick", "assimilate", "chat", "init", "doctor", "credits", "plan", "cycle", "pay", "wallet", "search", "sam-status", "wisdom-report", "tca-status", "eco-scan", "recon", "rebuild", "rollback", "enhance", "docs", "lint", "certify", "design", "lora-train", "lora-credit", "lora-status", "setup", "tutorial", "train", "agents-refresh", "nexus", "mcp", "repo", "protocol", "oracle", "ratchet", "trust", "text", "security", "prompt", "llm", "escrow", "reputation", "sla", "discovery", "swarm", "compliance", "defi", "aegis", "control", "identity", "vrf", "bitnet", "vanguard", "mev", "forge", "dev", "data", "context", "workflow", "agent", "a2a", "pipeline", "blueprint", "finish", "feature", "selfbuild", "optimize", "bridge", "launch", "providers", "memory")
$errors = @()
foreach ($cmd in $commands) {
    Write-Host "Checking: ass-ade $cmd --help" -ForegroundColor Cyan
    $output = python -m ass_ade $cmd --help 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL: $cmd" -ForegroundColor Red
        $errors += $cmd
    } else {
        Write-Host "PASS: $cmd" -ForegroundColor Green
    }
}
if ($errors.Count -gt 0) {
    Write-Host "`nSummary: Failed commands: $($errors -join ', ')" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`nSummary: All commands passed." -ForegroundColor Green
    exit 0
}
