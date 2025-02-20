import logging

def setup_logger(name="retail_app"):
    """Sets up a logger for the retail sales application."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File Handler - Logs will be stored in 'app.log'
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler - Logs will also be printed in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()

# Example usage
if __name__ == "__main__":
    logger.info("Retail Sales Application started")
    logger.debug("Debugging mode is active")
    logger.warning("This is a warning message")
    logger.error("An error occurred")


# Features of this logging setup:
# Logs to a File (app.log) – Keeps records of transactions, errors, and other details.
# Console Logging – Displays logs in the terminal for real-time debugging.
# Multiple Logging Levels – Debug, Info, Warning, Error.
# Timestamped Logs – Each log entry has a timestamp for tracking events.
# This logger can be used in your FastAPI application by calling logger.info(), logger.error(), etc., wherever needed. 🚀