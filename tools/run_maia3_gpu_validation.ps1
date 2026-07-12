# Windows GPU worker for Maia-3 validation. Run from PowerShell.
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CourseRoot = Join-Path $RepoRoot "brisez_les_systemes_v1"
$LabRoot = Join-Path $CourseRoot "LAB"
$DataRoot = Join-Path $CourseRoot "DATA"
$OutDir = Join-Path $DataRoot "GPU_LOCAL"
$Python = Join-Path $RepoRoot ".venv-gpu\Scripts\python.exe"

function Fail($Message) {
  Write-Error $Message
  exit 1
}

function Run-Step($Name, $Exe, [string[]]$ArgumentList) {
  Write-Host "`n==> $Name" -ForegroundColor Cyan
  & $Exe @ArgumentList
  if ($LASTEXITCODE -ne 0) {
    Fail "Step failed ($LASTEXITCODE): $Name"
  }
}

Set-Location $RepoRoot
if (!(Test-Path $Python)) {
  Fail "Python GPU environment not found: $Python. Create it with: py -3.11 -m venv .venv-gpu"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$EnvJson = Join-Path $OutDir "maia3_gpu_environment.json"
$EnvCheck = @'
import json, pathlib, platform, sys
try:
    import torch
except Exception as exc:
    raise SystemExit(f"PyTorch import failed: {exc}")
if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available. Refusing to run GPU validation.")
try:
    import maia3  # noqa: F401
except Exception as exc:
    raise SystemExit(f"maia3 import failed: {exc}")
idx = 0
props = torch.cuda.get_device_properties(idx)
out = pathlib.Path(r"__ENV_JSON__")
data = {
    "python_version": sys.version,
    "python_executable": sys.executable,
    "platform": platform.platform(),
    "torch_version": torch.__version__,
    "torch_cuda_version": torch.version.cuda,
    "cuda_available": True,
    "gpu_name": torch.cuda.get_device_name(idx),
    "gpu_total_vram_bytes": int(props.total_memory),
    "device_capability": torch.cuda.get_device_capability(idx),
}
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(data, ensure_ascii=False, indent=2))
'@
$EnvScript = Join-Path $OutDir "_check_cuda_env.py"
Set-Content -Path $EnvScript -Value ($EnvCheck.Replace("__ENV_JSON__", $EnvJson)) -Encoding UTF8
Run-Step "CUDA/PyTorch/Maia-3 environment" $Python @($EnvScript)
Remove-Item $EnvScript -Force -ErrorAction SilentlyContinue

$Manifest = Join-Path $DataRoot "core_40_index.csv"
$CpuProfile = Join-Path $DataRoot "maia3_79m_profiles_corrected.csv"
$Lichess = Join-Path $DataRoot "lichess_test_expanded.csv"
foreach ($Required in @($Manifest, $CpuProfile, $Lichess)) {
  if (!(Test-Path $Required)) { Fail "Required project file missing: $Required" }
}

$Profiler = Join-Path $LabRoot "scripts\maia3_profile.py"
$CompareProfiles = Join-Path $LabRoot "scripts\compare_maia_profiles.py"
$CompareLichess = Join-Path $LabRoot "scripts\compare_full_policy_lichess.py"

$Amp1 = Join-Path $OutDir "maia3_79m_profiles_gpu_amp_run1.csv"
$Amp2 = Join-Path $OutDir "maia3_79m_profiles_gpu_amp_run2.csv"
$Fp32 = Join-Path $OutDir "maia3_79m_profiles_gpu_fp32.csv"
$FullPolicy = Join-Path $OutDir "maia3_79m_full_policy_gpu.csv"
$CpuGpu = Join-Path $OutDir "maia3_cpu_gpu_comparison.csv"
$CpuGpuSummary = Join-Path $OutDir "maia3_cpu_gpu_summary.json"
$LichessCompare = Join-Path $OutDir "maia3_full_policy_gpu_vs_lichess.csv"
$LichessSummary = Join-Path $OutDir "maia3_full_policy_gpu_vs_lichess_summary.json"
$Report = Join-Path $OutDir "RAPPORT_MAIA3_GPU_VALIDATION_V1.md"

Run-Step "Maia-3 79M GPU AMP run 1" $Python @($Profiler, "--manifest", $Manifest, "--model", "maia3-79m", "--device", "cuda", "--multipv", "10", "--amp-mode", "on", "--output", $Amp1)
Run-Step "Maia-3 79M GPU AMP run 2" $Python @($Profiler, "--manifest", $Manifest, "--model", "maia3-79m", "--device", "cuda", "--multipv", "10", "--amp-mode", "on", "--output", $Amp2)
Run-Step "Maia-3 79M GPU FP32" $Python @($Profiler, "--manifest", $Manifest, "--model", "maia3-79m", "--device", "cuda", "--multipv", "10", "--amp-mode", "off", "--output", $Fp32)
Run-Step "Maia-3 79M full legal policy GPU" $Python @($Profiler, "--manifest", $Manifest, "--model", "maia3-79m", "--device", "cuda", "--multipv", "10", "--amp-mode", "on", "--all-legal-moves", "--output", $FullPolicy)

Run-Step "CPU/GPU comparison" $Python @($CompareProfiles, $CpuProfile, $Amp1, "--output", $CpuGpu, "--summary", $CpuGpuSummary)
Run-Step "GPU full policy vs Lichess" $Python @($CompareLichess, "--maia", $FullPolicy, "--lichess", $Lichess, "--manifest", $Manifest, "--output", $LichessCompare, "--summary", $LichessSummary)
Run-Step "AMP determinism comparison" $Python @($CompareProfiles, $Amp1, $Amp2, "--output", (Join-Path $OutDir "maia3_gpu_amp_run1_vs_run2.csv"), "--summary", (Join-Path $OutDir "maia3_gpu_amp_run1_vs_run2_summary.json"))
Run-Step "AMP vs FP32 comparison" $Python @($CompareProfiles, $Amp1, $Fp32, "--output", (Join-Path $OutDir "maia3_gpu_amp_vs_fp32.csv"), "--summary", (Join-Path $OutDir "maia3_gpu_amp_vs_fp32_summary.json"))

$CpuGpuJson = Get-Content $CpuGpuSummary -Raw
$LichessJson = Get-Content $LichessSummary -Raw
$Generated = @($EnvJson, $Amp1, $Amp2, $Fp32, $FullPolicy, $CpuGpu, $CpuGpuSummary, $LichessCompare, $LichessSummary)
$ReportText = @"
# Rapport Maia-3 GPU validation V1

Date locale: $(Get-Date -Format o)
Repo: $RepoRoot
Sorties: $OutDir

## Environnement

````json
$(Get-Content $EnvJson -Raw)
````

## Comparaison GPU / CPU

````json
$CpuGpuJson
````

## Comparaison GPU / Lichess

````json
$LichessJson
````

## Fichiers produits à committer si validation acceptée

$(($Generated | ForEach-Object { "- " + (Resolve-Path $_).Path.Replace($RepoRoot + "\", "") }) -join "`n")
- brisez_les_systemes_v1\DATA\GPU_LOCAL\RAPPORT_MAIA3_GPU_VALIDATION_V1.md

## Note

Ce script ne fait aucun commit et aucun push automatiquement.
"@
Set-Content -Path $Report -Value $ReportText -Encoding UTF8
Write-Host "`nValidation GPU terminée. Rapport: $Report" -ForegroundColor Green
exit 0
