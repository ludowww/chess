# Windows preflight for Maia-3 GPU worker.
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CourseRoot = Join-Path $RepoRoot "brisez_les_systemes_v1"
$DataRoot = Join-Path $CourseRoot "DATA"
$Python = Join-Path $RepoRoot ".venv-gpu\Scripts\python.exe"

function Fail($Message) {
  Write-Error $Message
  exit 1
}

Set-Location $RepoRoot

if (!(Get-Command nvidia-smi -ErrorAction SilentlyContinue)) {
  Fail "nvidia-smi not found. Install/update the NVIDIA driver first."
}
nvidia-smi
if ($LASTEXITCODE -ne 0) { Fail "nvidia-smi failed." }

if (!(Test-Path $Python)) {
  Fail "Missing GPU virtualenv Python: $Python. Expected .venv-gpu\Scripts\python.exe"
}

$RequiredFiles = @(
  (Join-Path $DataRoot "core_40_index.csv"),
  (Join-Path $DataRoot "maia3_79m_profiles_corrected.csv"),
  (Join-Path $DataRoot "lichess_test_expanded.csv"),
  (Join-Path $CourseRoot "LAB\scripts\maia3_profile.py"),
  (Join-Path $CourseRoot "LAB\scripts\compare_maia_profiles.py"),
  (Join-Path $CourseRoot "LAB\scripts\compare_full_policy_lichess.py")
)
foreach ($Path in $RequiredFiles) {
  if (!(Test-Path $Path)) { Fail "Required project file missing: $Path" }
}

$Py = @'
import json, sys
try:
    import torch
except Exception as exc:
    raise SystemExit(f"torch import failed: {exc}")
if not torch.cuda.is_available():
    raise SystemExit("torch.cuda.is_available() is False")
idx = 0
props = torch.cuda.get_device_properties(idx)
a = torch.randn((512, 512), device="cuda")
b = torch.randn((512, 512), device="cuda")
c = a @ b
torch.cuda.synchronize()
try:
    import maia3  # noqa: F401
except Exception as exc:
    raise SystemExit(f"maia3 import failed: {exc}")
print(json.dumps({
    "python": sys.version,
    "torch": torch.__version__,
    "torch_cuda": torch.version.cuda,
    "cuda_available": True,
    "gpu_name": torch.cuda.get_device_name(idx),
    "gpu_total_vram_bytes": int(props.total_memory),
    "matmul_checksum": float(c[0, 0].detach().cpu()),
    "maia3_import": True,
}, ensure_ascii=False, indent=2))
'@
$Tmp = Join-Path $env:TEMP "maia3_gpu_preflight.py"
Set-Content -Path $Tmp -Value $Py -Encoding UTF8
& $Python $Tmp
if ($LASTEXITCODE -ne 0) { Fail "Python GPU/Maia preflight failed." }
Write-Host "Preflight GPU Maia-3 OK." -ForegroundColor Green
exit 0
