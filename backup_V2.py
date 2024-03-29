from pathlib import Path
import shutil
import time
import os

source = Path("D:/Downloads/Documents")
destination = Path("D:/Transit/trial")
exclusions = ["EPIM", ".txt"]

# Create a new directory with date and time stamp
timestamp = time.strftime("%d-%m-%y _ %H-%M-%S")
new_folder = destination / timestamp
new_folder.mkdir(parents=True, exist_ok=True)

# Copy files from source to destination, excluding items in the exclusion list
for root, dirs, files in os.walk(source):
    dirs[:] = [d for d in dirs if d not in exclusions]
    files = [f for f in files if not any(f.endswith(ex) for ex in exclusions)]
    for file in files:
        src_file = Path(root) / file
        dst_file = new_folder / src_file.relative_to(source)
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)

# Keep the latest 3 directories and delete the older ones
all_dirs = sorted([d for d in destination.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True)
for dir in all_dirs[5:]:
    shutil.rmtree(dir)

print("Backup done successfully!")
