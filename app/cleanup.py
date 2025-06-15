import os
import shutil
from app.helper import logger, monitor

def cleanup_resources():
    total_freed = 0
    for folder in ["temp", "figures"]:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        total_freed += os.path.getsize(filepath)
                        os.remove(filepath)
                    except Exception as e:
                        logger.warning(f"Failed to remove {filepath}: {str(e)}")
            try:
                shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                logger.error(f"Cleanup error: {str(e)}")
    monitor.log_cleanup(total_freed)
    return total_freed
