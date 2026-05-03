"""backup_and_restore.py"""
from google.colab import drive
import shutil, time, threading
from pathlib import Path

COURSE_REPO_DIR = Path("/content/go2_course_repo")
DRIVE_BACKUP = Path("/content/drive/MyDrive/EEC289A_Robotics/run_baseline")
LOCAL_ARTIFACTS = COURSE_REPO_DIR / "artifacts/run_baseline"
_backup_thread = None

def mount_drive():
    drive.mount("/content/drive")
    print("Drive mounted")

def save_to_drive():
    if not LOCAL_ARTIFACTS.exists():
        print("No artifacts to backup")
        return
    DRIVE_BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(LOCAL_ARTIFACTS), str(DRIVE_BACKUP), dirs_exist_ok=True)
    print(f"Saved to {DRIVE_BACKUP}")

def restore_from_drive():
    if not DRIVE_BACKUP.exists():
        print("No Drive backup found")
        return
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(DRIVE_BACKUP), str(LOCAL_ARTIFACTS), dirs_exist_ok=True)
    print(f"Restored from {DRIVE_BACKUP}")

def _auto_backup_loop(interval_sec=300):
    mount_drive()
    while True:
        time.sleep(interval_sec)
        save_to_drive()
        print(f"Auto-backup done (every {interval_sec//60} min)")

def start_auto_backup(interval_sec=300):
    global _backup_thread
    if _backup_thread and _backup_thread.is_alive():
        print("Auto-backup already running")
        return
    _backup_thread = threading.Thread(target=_auto_backup_loop, args=(interval_sec,), daemon=True)
    _backup_thread.start()
    print(f"Auto-backup started (every {interval_sec//60} min)")
    print(f"   Local: {LOCAL_ARTIFACTS}")
    print(f"   Drive: {DRIVE_BACKUP}")
