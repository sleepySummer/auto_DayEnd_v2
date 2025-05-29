import logging
import os

log_folder = "C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\"
log_file = "error_log.txt"

os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_folder, log_file),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
