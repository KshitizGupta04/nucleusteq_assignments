import logging

from pathlib import (
    Path
)


# Get the backend root directory.
BASE_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)


# Directory where application logs are stored.
LOG_DIR = (
    BASE_DIR
    / "logs"
)


LOG_DIR.mkdir(
    exist_ok=True
)


# Complete path of the application log file.
LOG_FILE = (
    LOG_DIR
    / "assessment_portal.log"
)


# Configure centralized application logging.
logging.basicConfig(
    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)


# Shared application logger.
logger = logging.getLogger(
    "assessment_portal"
)