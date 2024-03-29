import os
import shutil
import time
import tempfile

# source = 'D:/Tally Prime/Data'
# destination = 'G:/My Drive/AutoBackup'

source = r"D:\Downloads\Documents"
destination = r"D:\Transit\TRIAL"

# Define exclusion list
exclusions = ["EPIM", ".txt"]

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

# Copy files from source to temporary directory, excluding items in the exclusion list
for root, dirs, files in os.walk(source):
    for exclusion in exclusions:
        if exclusion in dirs:
            dirs.remove(exclusion)
    for file in files:
        if not any(file.endswith(exclusion) for exclusion in exclusions):
            src_file = os.path.join(root, file)
            dst_file = os.path.join(temp_dir, os.path.relpath(src_file, source))
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.copy2(src_file, dst_file)

# Create a zip file with date and time stamp from the temporary directory
timestamp = time.strftime("%d-%m-%y _ %H-%M-%S")
shutil.make_archive(destination + "/" + timestamp, "zip", temp_dir)

# Remove the temporary directory
shutil.rmtree(temp_dir)

# Keep the latest 3 directories and delete the older ones
dirs = sorted([d for d in os.listdir(destination) if d.endswith(".zip")], reverse=True)
for dir in dirs[5:]:
    os.remove(os.path.join(destination, dir))

# Print backup done message
print("Backup done successfully!")
