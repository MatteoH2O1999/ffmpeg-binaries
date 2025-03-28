$root = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location -Path $root

$originalPyproject = Join-Path -Path $root -ChildPath "pyproject.toml"
$renamedOriginalPyproject = Join-Path -Path $root -ChildPath "old-pyproject.toml"
$namespacePyproject = Join-Path -Path $root -ChildPath "pyproject-namespace.toml"
$buildFolder = Join-Path -Path $root -ChildPath "build"

$PSStyle.OutputRendering = 'Ansi'
$RESET = $PSStyle.Reset
$BLUE = $PSStyle.Foreground.Blue

Write-Output "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Output "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}

Write-Output "Building original package..."
Write-Output "$BLUE$root> python -m build -o ./dist $args$RESET"
python -m build -o ./dist $args

Write-Output "Swapping project files..."
Rename-Item -Path $originalPyproject -NewName $renamedOriginalPyproject
Rename-Item -Path $namespacePyproject -NewName $originalPyproject

Write-Output "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Output "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}

Write-Output "Building namespace package..."
Write-Output "$BLUE$root> python -m build -o ./dist $args$RESET" -ForegroundColor Blue
python -m build -o ./dist $args

Write-Output "Restoring project files..."
Rename-Item -Path $originalPyproject -NewName $namespacePyproject
Rename-Item -Path $renamedOriginalPyproject -NewName $originalPyproject

Write-Output "Removing egg-info folders..."
Get-ChildItem $root -Recurse -Filter "*egg-info" | Remove-Item -Confirm:$false -Recurse
if (Test-Path -Path $buildFolder) {
    Write-Output "Removing build folder..."
    Remove-Item -Confirm:$false -Recurse -Path $buildFolder
}