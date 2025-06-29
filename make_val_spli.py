# make_val_split.py
import pathlib, random, shutil

train_root = pathlib.Path("dataset/static/train")
val_root   = pathlib.Path("dataset/static/val")
RATIO = 0.15          # 15 %
SEED  = 42
random.seed(SEED)

for cls_dir in train_root.iterdir():          # p. ej. A/, B/, …
    imgs = list(cls_dir.glob("*"))
    n_val = int(len(imgs) * RATIO)
    val_samples = random.sample(imgs, n_val)
    dest_cls = val_root / cls_dir.name
    dest_cls.mkdir(parents=True, exist_ok=True)
    for img in val_samples:
        shutil.move(str(img), dest_cls / img.name)
        
    print(f"{cls_dir.name}: moved {n_val}/{len(imgs)} to val/")
print("✓ Validation split listo (15 %)")