import os
import sys
import logging
from datetime import datetime
from rich.logging import RichHandler

# Create log directory if it doesn't exist
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Lấy tên script đang chạy để đặt tên file log
try:
    main_script = os.path.basename(sys.argv[0])
    script_name = os.path.splitext(main_script)[0]
    if not script_name:
        script_name = "app"
except Exception:
    script_name = "app"

# Setup logging configuration — đặt tên file theo script + timestamp
log_filename = datetime.now().strftime(f"{log_dir}/{script_name}_%Y%m%d_%H%M%S.log")
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    force=True,
    handlers=[
        RichHandler(rich_tracebacks=True, markup=True),
        file_handler
    ]
)

def get_logger(name):
    """
    Returns a logger instance with the specified name, set to DEBUG level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Chỉ source code của bạn (khi dùng get_logger) mới in log từ DEBUG
    return logger
