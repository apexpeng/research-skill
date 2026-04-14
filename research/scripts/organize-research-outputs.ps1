param(
    [ValidateSet("sync", "activate", "status")]
    [string]$Command = "status",
    [string]$ProjectTitle = "",
    [string]$ProjectKey = ""
)

# Use CODEX_BASE env var if set, otherwise use user's home directory
$codexBase = if ($env:CODEX_BASE) { $env:CODEX_BASE } else { Join-Path $HOME ".codex" }
$scriptPath = Join-Path $codexBase "skills\research\scripts\organize_research_outputs.py"
$workspacePath = Join-Path $codexBase "research-workspace"
$arguments = @($scriptPath, "--workspace", $workspacePath, $Command)

if ($Command -eq "sync" -and $ProjectTitle) {
    $arguments += @("--project-title", $ProjectTitle)
}

if ($Command -eq "activate" -and $ProjectKey) {
    $arguments += @("--project-key", $ProjectKey)
}

python @arguments
