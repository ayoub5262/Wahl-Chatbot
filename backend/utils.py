import logging
from backend.config import Config


def setup_logger(name=__name__):
    """
    Set up and configure logger for the application.
    
    Args:
        name: Logger name (typically __name__ from calling module)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set logging level based on DEBUG config
    level = logging.DEBUG if Config.DEBUG else logging.INFO
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # File handler
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
