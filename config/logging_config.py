import sys
from pathlib import Path

from loguru import logger


LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)


logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "{message}",
)

logger.add(
    LOG_PATH / "wealthpilot.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
)

app_logger = logger