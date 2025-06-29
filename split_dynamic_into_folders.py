# split_dynamic_into_folders.py
import pathlib, shutil, re

ROOT = pathlib.Path("MSL-dynamic-signs-frontal-view/MSL-dynamic-signs")
LETTER_REGEX = re.compile(r"S\d+-(.+?)-frontal")   # captura J, K, Ñ, ...

for split in ("train", "test"):
    split_dir = ROOT / split
    for vid in split_dir.glob("*.mp4"):
        m = LETTER_REGEX.match(vid.stem)
        if not m:
            print("Saltando", vid.name)
            continue
        letter = m.group(1)
        dest_dir = split_dir / letter
        dest_dir.mkdir(exist_ok=True)
        shutil.move(vid, dest_dir / vid.name)
    print(f"✓ Reorganizado {split_dir}")
