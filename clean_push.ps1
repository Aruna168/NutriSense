<#
Usage: Run this script in the repository root in PowerShell.
It creates a new orphan branch with only the current working tree (no history),
commits, and pushes it to a new remote repository URL you provide.

It will NOT touch your existing remotes or branches. You can provide a new remote
URL (for example a new GitHub repo) when prompted.
#>

$remote = Read-Host "Enter the new remote repository URL (e.g. https://github.com/you/new-repo.git)"
if (-not $remote) {
    Write-Host "No remote provided — exiting"
    exit 1
}

Write-Host "Creating a clean orphan branch 'clean-main'..."
git checkout --orphan clean-main

Write-Host "Removing all files from the index (they will be re-added from working tree)..."
git rm -rf --cached .

Write-Host "Adding files (respecting .gitignore)..."
git add .

Write-Host "Committing clean snapshot..."
git commit -m "Initial commit (clean history)"

Write-Host "Setting remote to: $remote"
try { git remote remove origin } catch { }
git remote add origin $remote

Write-Host "Pushing clean branch to origin (main)..."
git branch -M main
git push -u origin main

Write-Host "Done. If you used an existing remote, be aware the old history is still on that remote."
