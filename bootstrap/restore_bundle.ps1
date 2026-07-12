$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ArchiveDir = Join-Path $PSScriptRoot "archive"
$Output = Join-Path $RepoRoot "brisez_les_systemes_v1_0_rc1.tar.xz"
$Expected = "c88f59116ffd8eddd5c0254508b814e7f84d2efdef9ff6ccce0dc62729aec225"
$Pattern = "brisez_les_systemes_v1_0_rc1.tar.xz.b64.part*"

$Parts = @(Get-ChildItem $ArchiveDir -Filter $Pattern | Sort-Object Name)
$ExpectedNames = @(0..19 | ForEach-Object { "brisez_les_systemes_v1_0_rc1.tar.xz.b64.part{0:D2}" -f $_ })
$ActualNames = @($Parts | ForEach-Object { $_.Name })

if ($ActualNames.Count -ne $ExpectedNames.Count -or (Compare-Object $ExpectedNames $ActualNames)) {
    throw "Archive segments are missing, duplicated, or misnamed."
}

$Base64 = -join ($Parts | ForEach-Object { (Get-Content $_.FullName -Raw) -replace '\s', '' })
try {
    $Bytes = [Convert]::FromBase64String($Base64)
}
catch {
    throw "Invalid base64 archive data: $($_.Exception.Message)"
}

[IO.File]::WriteAllBytes($Output, $Bytes)
$Actual = (Get-FileHash $Output -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) {
    Remove-Item $Output -Force -ErrorAction SilentlyContinue
    throw "SHA-256 mismatch: expected $Expected, got $Actual"
}

Write-Host "Archive reconstructed: $Output"
Write-Host "SHA-256 verified:      $Actual"

tar -xJf $Output -C $RepoRoot
$LabReadme = Join-Path $RepoRoot "brisez_les_systemes_v1/LAB/README_LAB.md"
if (-not (Test-Path $LabReadme)) {
    throw "Extraction completed but the expected project files were not found."
}

Write-Host "Project restored: $(Join-Path $RepoRoot 'brisez_les_systemes_v1')"
Write-Host "Next: cd brisez_les_systemes_v1; ./LAB/run_static_qa.sh"
