# make_mini_dataset.py
import pathlib, shutil, random, math

SOURCE = pathlib.Path("dataset")   # carpeta original
TARGET = pathlib.Path("data")      # nueva carpeta “ligera”
RATIO  = 0.08                      # 8 %
SEED   = 42
EXT_MEDIA = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".mp4", ".avi", ".mov", ".mkv"}

random.seed(SEED)

def replicate_tree(src_dir: pathlib.Path):
    """Replica directorios y copia 8 % de los ficheros multimedia."""
    for root, dirs, files in os.walk(src_dir):
        rel_root = pathlib.Path(root).relative_to(src_dir)
        dst_root = TARGET / rel_root
        dst_root.mkdir(parents=True, exist_ok=True)

        # Separa multimedia vs otros archivos
        media_files = [f for f in files if pathlib.Path(f).suffix.lower() in EXT_MEDIA]
        other_files = [f for f in files if f not in media_files]

        # 1️⃣ Copiar otros archivos tal cual
        for fname in other_files:
            shutil.copy2(src_dir / rel_root / fname, dst_root / fname)

        # 2️⃣ Copiar solo 8 % de multimedia (al menos 1 si existe)
        if media_files:
            k = max(1, math.ceil(len(media_files) * RATIO))
            for fname in random.sample(media_files, k):
                shutil.copy2(src_dir / rel_root / fname, dst_root / fname)

if __name__ == "__main__":
    import os
    if TARGET.exists():
        print(f"⚠️  Ya existe '{TARGET}'. Elimínala o cambia TARGET antes de continuar.")
        raise SystemExit(1)

    replicate_tree(SOURCE)
    print("✓ Carpeta 'data/' creada con el 8 % de los archivos multimedia.")
