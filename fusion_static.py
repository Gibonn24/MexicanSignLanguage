# fusion_static.py
import shutil, pathlib

src_roots = [
    pathlib.Path("MSL-ABC/lsm-abc-A"),
    pathlib.Path("MSL-ABC/lsm-abc-B"),
    pathlib.Path("MSL-ABC/lsm-abc-C"),
]

dst_root = pathlib.Path("dataset/static")
for src in src_roots:
    for split in ("train", "test"):           # origen ya trae estos splits
        for cls_dir in (src / split).iterdir():   # A, B, C… Y, blank
            dest = dst_root / split / cls_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in cls_dir.iterdir():
                # si un fichero con el mismo nombre ya existe lo omite
                shutil.move(str(f), dest / f.name)
print("✓ Fusión completada en dataset/static/")