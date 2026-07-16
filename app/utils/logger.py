import logging


logger = logging.getLogger("ai_personal_os")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# Formatter
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File Handler
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)

# Add handlers only once
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)