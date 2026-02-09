# PowerShell script to rename claude_parasite_brain_suck to black_swarm
# Run this AFTER closing Claude Code

$oldName = "claude_parasite_brain_suck"
$newName = "black_swarm"
$projectRoot = "D:\codingProjects"

Write-Host "Renaming project folder from $oldName to $newName..." -ForegroundColor Cyan

# Step 1: Rename the directory
Set-Location $projectRoot
if (Test-Path $oldName) {
    Rename-Item -Path $oldName -NewName $newName
    Write-Host "✓ Folder renamed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Folder $oldName not found" -ForegroundColor Red
    exit 1
}

# Step 2: Update all file references
Set-Location "$projectRoot\$newName"
Write-Host "`nUpdating file references..." -ForegroundColor Cyan

$files = Get-ChildItem -Recurse -File | Where-Object {
    $_.Extension -in @('.py', '.bat', '.json', '.md', '.txt', '.sh', '.ps1', '.yml', '.yaml', '.html', '.js', '.css')
}

$count = 0
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match $oldName) {
        $newContent = $content -replace [regex]::Escape($oldName), $newName
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        $count++
        Write-Host "  Updated: $($file.Name)" -ForegroundColor Gray
    }
}

Write-Host "`n✓ Updated $count files" -ForegroundColor Green
Write-Host "`nProject renamed to 'black_swarm' successfully!" -ForegroundColor Green
Write-Host "You can now cd to D:\codingProjects\black_swarm and restart Claude Code." -ForegroundColor Yellow
