import logging
import os

LOG_DIR = os.getenv("LOG_DIR")

logger = logging.getLogger("font_analyzer")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Always add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Only add file handler in Docker environment or debug mode
if LOG_DIR:
    try:
        LOG_FILENAME = os.path.join(LOG_DIR, "font-analyzer.log")

        # Create log directory if it does not exist
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        file_handler = logging.FileHandler(LOG_FILENAME, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(f"Log file: {LOG_FILENAME}")
    except Exception as e:
        print(
            f"Warning: Could not create log file ({e}), "
            "only console logging will be used."
        )
else:
    print("File logging disabled - using console logging only")


def log(msg: str, level: str = "info") -> None:
    if level == "info":
        logger.info(msg)
    elif level == "warning":
        logger.warning(msg)
    elif level == "error":
        logger.error(msg)
    else:
        logger.debug(msg)
