from pathlib import Path
import shutil
import time
from apscheduler.schedulers.background import BackgroundScheduler

def backup_files(source, destination, exclusions):
    source = Path(source).resolve()
    destination = Path(destination).resolve()

    # Create a new directory with date and time stamp
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    new_folder = destination / timestamp
    new_folder.mkdir(parents=True)

    # Define ignore function for shutil.copytree()
    def ignore_patterns(path, names):
        ignored_names = []
        for name in names:
            if any(name.endswith(exclusion) for exclusion in exclusions):
                ignored_names.append(name)
        return set(ignored_names)

    # Copy files from source to destination, excluding items in the exclusion list
    shutil.copytree(source, new_folder, ignore=ignore_patterns)

    # Keep the latest 3 directories and delete the older ones
    dirs = sorted(destination.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
    for dir_path in dirs[3:]:
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
    backup_files, "cron", hour=22, minute=19, args=[source, destination, exclusions]
)

# Start the Scheduled jobs
sched.start()

# Keep the script running
while True:
    time.sleep(1)
