import os
import sys

import yaml
from loguru import logger
from pytz import timezone


# Load config
def load_config(conf_file):
    with open(conf_file, "r") as f:
        config = yaml.safe_load(f)
    return config


# Set timezone
tz = timezone(os.environ.get("TIMEZONE", "Europe/Warsaw"))

# Remove all logger handlers
logger.remove()

# Setup a new logger handler with INFO as default logging level
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {module} | {message}",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)

# YAML config file path
CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.yaml")
CONFIG = load_config(CONFIG_FILE)
