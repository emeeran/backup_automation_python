from pathlib import Path
import shutil
import time


def backup_files(source, destination, exclusions):
    source = Path(source).resolve()
    destination = Path(destination).resolve()

    timestamp = time.strftime("%d-%m-%y _ %H-%M-%S")
    new_folder = destination / timestamp
    new_folder.mkdir(parents=True, exist_ok=True)

    for file in source.rglob("*"):
        if not any(
            file.name.endswith(exclusion) for exclusion in exclusions
        ) and not any(exclusion in file.parts for exclusion in exclusions):
            dst_file = new_folder / file.relative_to(source)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dst_file)

    # Keep the latest 3 directories and delete the older ones
    dirs = sorted(
        [x for x in destination.iterdir() if x.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )
    for dir_path in dirs[3:]:
        shutil.rmtree(dir_path)

    print("Backup done successfully!")


if __name__ == "__main__":
    source = r"D:\Transit\Conv"
    destination = r"D:\Transit\TRIAL"
    exclusions = ["Scripts"]
    backup_files(source, destination, exclusions)
