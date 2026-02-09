import os
import shutil
import json
from datetime import datetime, timezone, timedelta

def cleanup_experiments(base_dir="/app/experiments", manifest_path="/app/experiments_manifest.json"):
    """
    Remove empty experiment folders, archive folders older than 24 hours,
    and update the manifest with kept vs archived experiments.
    """
    archive_dir = os.path.join(base_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)

    kept = []
    archived = []

    # Iterate over sub‑folders in the experiments directory (skip the archive itself)
    for entry in os.scandir(base_dir):
        if not entry.is_dir() or entry.name == "archive":
            continue

        # Remove empty experiment folders
        if not any(os.scandir(entry.path)):
            try:
                os.rmdir(entry.path)
            except OSError:
                pass
            continue

        # Determine folder age via its modification time
        mtime = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc)

        if mtime < cutoff:
            # Archive older experiments
            dest = os.path.join(archive_dir, entry.name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(entry.path, dest)
            archived.append(entry.name)
        else:
            kept.append(entry.name)

    # Write updated manifest
    manifest_data = {
        "kept": kept,
        "archived": archived,
        "last_cleanup": now.isoformat()
    }
    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
    except Exception as e:
        print(f"Failed to write experiments manifest: {e}")

if __name__ == "__main__":
    cleanup_experiments()