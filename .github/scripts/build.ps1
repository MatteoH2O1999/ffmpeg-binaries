$root = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location -Path $root

$originalPyproject = Join-Path -Path $root -ChildPath "pyproject.toml"
$renamedOriginalPyproject = Join-Path -Path $root -ChildPath "old-pyproject.toml"
$namespacePyproject = Join-Path -Path $root -ChildPath "pyproject-namespace.toml"
$buildFolder = Join-Path -Path $root -ChildPath "build"

Write-Host "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Host "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}

Write-Host "Building original package..."
Write-Host "$root> python -m build -o ./dist $args" -ForegroundColor Blue
python -m build -o ./dist $args

Write-Host "Swapping project files..."
Rename-Item -Path $originalPyproject -NewName $renamedOriginalPyproject
Rename-Item -Path $namespacePyproject -NewName $originalPyproject

Write-Host "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Host "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}

Write-Host "Building namespace package..."
Write-Host "$root> python -m build -o ./dist $args" -ForegroundColor Blue
python -m build -o ./dist $args

Write-Host "Restoring project files..."
Rename-Item -Path $originalPyproject -NewName $namespacePyproject
Rename-Item -Path $renamedOriginalPyproject -NewName $originalPyproject

Write-Host "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Host "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}