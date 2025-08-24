# Minecraft Resource Extractor Action

This repository provides:
- A Python extractor script that downloads the official Minecraft client `.jar` for a specified version and pulls out all block & item texture PNGs (and any other PNGs under `assets/minecraft/textures/`).
- A GitHub Actions workflow (Extract Minecraft Textures) that you can trigger manually with a version number to produce either:
  - A workflow artifact containing the textures (current README baseline), and/or
  - (If the new workflow file is added) a GitHub Release with a downloadable `mc-texture.zip`.

> NOTE: The workflow file `.github/workflows/extract-textures.yml` must exist in the default branch for the manual dispatch option to appear. If you haven’t successfully added it yet, follow the instructions in the previous assistant messages.

---

## Features

- Fetches Mojang official client jar for a given version
- Extracts all PNG textures from `assets/minecraft/textures/`
- Packages them into a zip archive
- (Optional) Publishes a release asset named `mc-texture.zip`
- Replaces an existing release/tag of the same version if configured to do so

---

## Quick Start (GitHub Action)

1. Go to the Actions tab in the repository.
2. Select the workflow: “Extract Minecraft Textures”.
3. Click “Run workflow”.
4. Enter a Minecraft version (example: `1.21.7` or `1.20.1`).
5. Run it and wait for completion.
6. Retrieve results:
   - Artifact download: Open the workflow run, scroll to “Artifacts” and download the zip.
   - Release asset (if the workflow creates a release): Go to “Releases” and download `mc-texture.zip`.

---

## Output Contents

Inside the extracted archive you will find the directory structure mirroring the jar path:
```
assets/minecraft/textures/...
```
All PNG files under that path are included. No transformation is performed (you get the raw PNGs).

---

## Repository Structure

| Path | Description |
|------|-------------|
| `extractor/extract.py` | Core Python script to download the jar and extract texture PNGs. |
| `.github/workflows/extract-textures.yml` | (Planned / Added) GitHub Actions workflow definition for manual extraction. |

If the workflow file is not yet in the repo, add it at `.github/workflows/extract-textures.yml`.

---

## Example Workflow (Planned)

```yaml
name: Extract Minecraft Textures
on:
  workflow_dispatch:
    inputs:
      version:
        description: "Minecraft version (e.g., 1.21.7)"
        required: true
        default: "1.21.7"
jobs:
  extract:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: pip install -r extractor/requirements.txt
      - run: python extractor/extract.py "${{ github.event.inputs.version }}" extracted_textures
      - name: Rename zip file
        run: |
          if [ -f "extracted_textures/mc-data.zip" ]; then
            mv extracted_textures/mc-data.zip extracted_textures/mc-texture.zip
          else
            echo "mc-data.zip not found"; exit 1
          fi
      - name: Remove previous release if exists
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          TAG="${{ github.event.inputs.version }}"
          if gh release view "$TAG" &>/dev/null; then
            gh release delete "$TAG" --yes
          fi
          if git rev-parse "refs/tags/$TAG" &>/dev/null; then
            git push origin --delete "$TAG"
          fi
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: "${{ github.event.inputs.version }}"
          name: "Minecraft Textures ${{ github.event.inputs.version }}"
          body: |
            Minecraft texture pack for version ${{ github.event.inputs.version }}
          files: extracted_textures/mc-texture.zip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Local Usage (Manual Extraction)

You can run the script locally if you have Python 3.x:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r extractor/requirements.txt
python extractor/extract.py 1.21.7 output_dir
```

After success:
```
output_dir/
  mc-data.zip (or renamed zip)
  assets/minecraft/textures/...
```

---

## Potential Enhancements (Feel free to request)

- Add caching for pip dependencies (actions/cache) to speed runs.
- Add concurrency control to avoid duplicate version runs.
- Make “overwrite existing release” optional (input flag).
- Add version input validation (regex).
- Upload both artifact and release asset for redundancy.
- Include a manifest (JSON) listing all extracted file paths and checksums.

If you want any of these built in, open an issue or ask and we can update the workflow.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Workflow not visible | File missing or disabled actions | Ensure `.github/workflows/extract-textures.yml` exists and Actions are enabled |
| 403 on push attempt | Missing write permissions or branch protection | Adjust GitHub App / token perms or create a PR |
| Release not created | Release step failed or token lacks permission | Check job logs; ensure GITHUB_TOKEN has contents: write |
| No `mc-data.zip` | Extraction script failed or jar layout changed | Review logs; verify version exists |

---

## Legal / Disclaimer

Minecraft assets are subject to Mojang/Microsoft’s EULA and guidelines. This tool merely automates extraction of files you could manually obtain from your legally downloaded client. 
- Do not redistribute textures in violation of Mojang’s terms.
- Respect any restrictions on commercial use.

You are responsible for compliance with applicable licenses and terms.

---

## License

(Choose and add a LICENSE file, e.g., MIT / Apache-2.0. Then update this section.)

---

## Contributing

Pull requests and suggestions welcome.
1. Fork / create a feature branch.
2. Make changes with clear commit messages.
3. Open a PR describing the change.

---

## Status

Active: open to improvements and refinements.

---

Feel free to suggest edits or ask for the workflow to be updated simultaneously.
