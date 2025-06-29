# prep_dynamic.py  (ponerlo junto a tus carpetas MSL-*)
import pathlib, shutil, random

random.seed(42)
RATIO_VAL = 0.15
LETTERS = ("J", "K", "Ñ", "Q", "X", "Z")

# -------- 1. Paths de origen --------
SRC_FRONTAL = pathlib.Path("MSL-dynamic-signs-frontal-view") / "MSL-dynamic-signs"
SRC_PROFILE = pathlib.Path("MSL-dynamic-signs-profile")      / "MSL-dynamic-profile-signs"

# -------- 2. Paths destino ----------
DST = pathlib.Path("dataset") / "dynamic"
for view in ("frontal", "profile"):
    for split in ("train", "val", "test"):
        for l in LETTERS:
            (DST/view/split/l).mkdir(parents=True, exist_ok=True)

# -------- 3. Copiar frontal (train + test ya existen) --------
def copy_tree(src_root, view_name, has_split=True):
    if has_split:
        for split in ("train", "test"):
            for l in LETTERS:
                src = src_root / split / l
                if not src.exists():
                    continue
                for vid in src.glob("*.mp4"):
                    dst = DST/view_name/split/l/vid.name
                    if not dst.exists():
                        shutil.copy2(vid, dst)
    else:  # todo es "train"
        for l in LETTERS:
            src = src_root / l
            for vid in src.glob("*.mp4"):
                dst = DST/view_name/"train"/l/vid.name
                if not dst.exists():
                    shutil.copy2(vid, dst)

print("→ Copiando frontal…")
copy_tree(SRC_FRONTAL, "frontal", has_split=True)

print("→ Copiando profile…")
copy_tree(SRC_PROFILE, "profile", has_split=False)

# -------- 4. Crear split de validación (15 %) --------
def make_val(view_name):
    for l in LETTERS:
        train_dir = DST/view_name/"train"/l
        vids = list(train_dir.glob("*.mp4"))
        n_val = int(len(vids) * RATIO_VAL)
        val_samples = random.sample(vids, n_val)
        for vid in val_samples:
            vid.rename(DST/view_name/"val"/l/vid.name)
        print(f"{view_name}/{l}: movidos {n_val}/{len(vids)} a val")

print("→ Generando val …")
make_val("frontal")
make_val("profile")

print("✓ Dinámicas listas en dataset/dynamic/")
