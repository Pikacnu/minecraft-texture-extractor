# Minecraft Resource Extractor Action

This GitHub Action extracts all Minecraft block/item textures (PNGs) from the official client .jar for a specified version.

## Usage

1. Trigger the `Extract Minecraft Textures` workflow manually.
2. Enter the desired Minecraft version (e.g., `1.20.1`).
3. After the workflow runs, download the textures from the workflow artifact.

## How it works

- Downloads the official Minecraft client .jar for the specified version.
- Extracts all PNG textures from `assets/minecraft/textures/` in the jar.
- Uploads the extracted images as an artifact.

## Structure

- `extractor/extract.py`: Python script to handle download and extraction.
- `.github/workflows/extract-textures.yml`: GitHub Action workflow file.