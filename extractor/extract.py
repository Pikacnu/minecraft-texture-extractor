import zipfile
import os
import requests
import sys
import tempfile
import shutil

def download_minecraft_jar(version, dest_path):
    # Get version manifest
    manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
    r = requests.get(manifest_url)
    r.raise_for_status()
    manifest = r.json()
    version_meta = next((v for v in manifest['versions'] if v['id'] == version), None)
    if not version_meta:
        raise Exception(f"Version {version} not found in manifest.")
    version_url = version_meta['url']
    r = requests.get(version_url)
    r.raise_for_status()
    version_json = r.json()
    jar_url = version_json['downloads']['client']['url']
    r = requests.get(jar_url)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded Minecraft {version} jar to {dest_path}")

def extract_textures(jar_path, output_dir):
    for root, _, _ in os.walk(output_dir):
        # Clean up previous output if any
        shutil.rmtree(root)
        break
    with zipfile.ZipFile(jar_path, 'r') as jar:
        for file in jar.namelist():
            if file.startswith("assets/minecraft/textures/") and file.endswith(".png"):
                out_path = os.path.join(output_dir, file.replace("assets/minecraft/textures/", ""))
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "wb") as out_file:
                    out_file.write(jar.read(file))
    print(f"Extracted textures to {output_dir}")

def zip_textures(output_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    print(f"Zipped textures to {zip_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract.py <version> <output_dir>")
        sys.exit(1)
    version = sys.argv[1]
    output_dir = sys.argv[2]
    jar_path = "minecraft-client.jar"

    download_minecraft_jar(version, jar_path)
    extract_textures(jar_path, output_dir)
    zip_path = os.path.join(output_dir, "mc-data.zip")
    zip_textures(output_dir, zip_path)
    print("Done.")
