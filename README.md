# Minecraft Texture Extractor

Trigger a GitHub Action with a Minecraft version and get a ZIP of the extracted vanilla textures.

## How It Works
1. Run the workflow (Actions tab -> “Extract Minecraft Textures” -> Run workflow -> enter version).
2. The script downloads the official client JAR for that version.
3. It extracts all PNGs from `assets/minecraft/textures/`.
4. It zips them and (if the workflow file is present) publishes a GitHub Release containing `mc-texture.zip`.

## Download

After running the workflow for a version (example: 1.21.7), download the ZIP here:

Example (replace VERSION with the version you ran):
https://github.com/pikacnu/minecraft-texture-extractor/releases/download/VERSION/mc-texture.zip

Concrete example:
https://github.com/pikacnu/minecraft-texture-extractor/releases/download/1.21.7/mc-texture.zip

If a release does not exist yet for the version, run the workflow first.

## Run Locally (Optional)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r extractor/requirements.txt
python extractor/extract.py 1.21.7 output_dir
```

Result:
```
output_dir/
  mc-data.zip (or renamed)
  assets/minecraft/textures/... (PNG files)
```

## Notes
- Each version you run creates (or replaces) a release tagged with that version.
- File name: mc-texture.zip
- Contents are raw unmodified textures from the client JAR.
- Respect Mojang/Microsoft EULA—do not redistribute in violation of their terms.

## Issues / Improvements
Open an issue or PR if you’d like caching, validation, or additional outputs.
