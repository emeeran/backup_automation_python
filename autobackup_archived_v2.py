import os
import shutil
import time
import tempfile

source = r"D:\Downloads\Documents"
destination = r"D:\Transit\TRIAL"
exclusions = ["EPIM", ".txt"]

def ignore_patterns(path, names):
    ignored_names = []
    for name in names:
        if name in exclusions or any(name.endswith(ext) for ext in exclusions):
            ignored_names.append(name)
    return set(ignored_names)

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

# Copy files from source to temporary directory, excluding items in the exclusion list
shutil.copytree(source, temp_dir, ignore=ignore_patterns, dirs_exist_ok=True)

# Create a zip file with date and time stamp from the temporary directory
timestamp = time.strftime("%d-%m-%y _ %H-%M-%S")
shutil.make_archive(os.path.join(destination, timestamp), "zip", temp_dir)

# Remove the temporary directory
shutil.rmtree(temp_dir)

# Keep the latest 3 directories and delete the older ones
backup_files = sorted([d for d in os.listdir(destination) if d.endswith(".zip")], reverse=True)
for old_backup in backup_files[3:]:
    os.remove(os.path.join(destination, old_backup))

print("Backup done successfully!")
