# Worker Windows GPU Maia-3

Ce document sert à préparer le PC Windows de Ludo pour exécuter localement la validation GPU Maia-3. Le VPS ne doit pas exécuter Maia-3 en GPU : il fournit seulement le tooling.

## 1. Installer Python 3.11

1. Télécharger Python 3.11 depuis <https://www.python.org/downloads/windows/>.
2. Pendant l’installation, cocher **Add python.exe to PATH**.
3. Vérifier dans PowerShell :

```powershell
py -3.11 --version
```

## 2. Créer l’environnement `.venv-gpu`

Depuis la racine du repo `chess` :

```powershell
py -3.11 -m venv .venv-gpu
```

Le tooling attend exactement :

```text
.venv-gpu\Scripts\python.exe
```

## 3. Activer l’environnement PowerShell

```powershell
.\.venv-gpu\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip setuptools wheel
```

Si PowerShell bloque l’activation :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Puis relancer l’activation.

## 4. Installer PyTorch CUDA

Commande indicative à adapter selon la version CUDA recommandée par PyTorch :

```powershell
python -m pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Si cette commande n’est plus compatible, ne pas figer une vieille URL : utiliser le sélecteur officiel PyTorch <https://pytorch.org/get-started/locally/> avec `Windows`, `Pip`, `Python`, `CUDA`, puis copier la commande actuelle.

## 5. Installer les dépendances LAB

Depuis la racine du repo :

```powershell
python -m pip install -r .\brisez_les_systemes_v1\LAB\requirements.txt
```

## 6. Installer Maia-3 épinglé

Installer la révision validée par le projet :

```powershell
python -m pip install "git+https://github.com/CSSLab/maia3.git@1e13597c42d4858b7cfd7cfdae01e297263364b2"
```

Ne pas committer les modèles téléchargés, les caches Hugging Face ou les dossiers de cache locaux.

## 7. Lancer le préflight

Depuis n’importe quel dossier du repo :

```powershell
.\tools\test_gpu_environment.ps1
```

Le préflight vérifie `nvidia-smi`, `.venv-gpu`, `torch`, CUDA, le GPU, la VRAM, une multiplication matricielle CUDA, `maia3`, et les fichiers requis du projet. Il retourne un code non nul en cas d’échec.

## 8. Lancer le run complet

```powershell
.\tools\run_maia3_gpu_validation.ps1
```

Le script refuse de fonctionner sans CUDA. Il produit tous les fichiers dans :

```text
brisez_les_systemes_v1\DATA\GPU_LOCAL\
```

## 9. Fichiers à committer après validation

Si les métriques sont acceptables, committer uniquement les résultats reproductibles de validation GPU :

```text
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_gpu_environment.json
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run1.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run2.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_fp32.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_full_policy_gpu.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_comparison.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_summary.json
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv
brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json
brisez_les_systemes_v1/DATA/GPU_LOCAL/RAPPORT_MAIA3_GPU_VALIDATION_V1.md
```

Les comparaisons supplémentaires `maia3_gpu_amp_run1_vs_run2.*` et `maia3_gpu_amp_vs_fp32.*` peuvent aussi être gardées comme annexes si Ludo veut auditer le déterminisme AMP et l’écart AMP/FP32.

## 10. Fichiers à ne jamais committer

Ne jamais committer :

```text
.venv-gpu/
__pycache__/
*.pyc
.cache/
huggingface/
models/
*.pt
*.pth
*.ckpt
*.safetensors
```

Ne pas committer de faux fichiers GPU : les CSV/JSON de `DATA/GPU_LOCAL` doivent venir du PC Windows GPU.

## 11. Procédure de push sur une branche de résultats

Après le run Windows, créer une branche dédiée aux résultats :

```powershell
git switch work/maia3-gpu-results-v1
# ou, si elle n’existe pas encore :
git switch -c work/maia3-gpu-results-v1

git status --short
git add brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_gpu_environment.json `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run1.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run2.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_fp32.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_full_policy_gpu.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_comparison.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_summary.json `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json `
        brisez_les_systemes_v1/DATA/GPU_LOCAL/RAPPORT_MAIA3_GPU_VALIDATION_V1.md

git commit -m "Add Maia3 GPU validation results"
git push -u origin work/maia3-gpu-results-v1
```

Ne pas ouvrir de PR, fusionner ou taguer sans consigne explicite.
