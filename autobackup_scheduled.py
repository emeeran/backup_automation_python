import os
import shutil
import time
from apscheduler.schedulers.background import BackgroundScheduler


def backup_files(source, destination, exclusions):
    # Normalize paths
    source = os.path.normpath(source)
    destination = os.path.normpath(destination)

    # Create a new directory with date and time stamp
    timestamp = time.strftime("%d-%m-%y _ %H-%M-%S")
    new_folder = os.path.join(destination, timestamp)
    os.makedirs(new_folder)

    # Copy files from source to destination, excluding items in the exclusion list
    for root, dirs, files in os.walk(source):
        for exclusion in exclusions:
            if exclusion in dirs:
                dirs.remove(exclusion)
        for file in files:
            if not any(file.endswith(exclusion) for exclusion in exclusions):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(new_folder, os.path.relpath(src_file, source))
                dst_dir = os.path.dirname(dst_file)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copy2(src_file, dst_file)

    # Keep the latest 3 directories and delete the older ones
    dirs = sorted(os.listdir(destination), reverse=True)
    for dir_name in dirs[3:]:
        dir_path = os.path.join(destination, dir_name)
        shutil.rmtree(dir_path)

    print("Backup done successfully!")


# Set the source, destination, and exclusions
source = r"D:\Transit\Conv"
destination = r"D:\Transit\TRIAL"
exclusions = ["Scripts"]

# Create a default Background Scheduler
sched = BackgroundScheduler()

# Schedule the backup
sched.add_job(
    backup_files, "cron", hour=21, minute=15, args=[source, destination, exclusions]
)

# Start the Scheduled jobs
sched.start()

# Keep the script running
while True:
    time.sleep(1)
