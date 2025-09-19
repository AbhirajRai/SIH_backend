"""
Uvicorn Configuration
Custom configuration to suppress warnings and optimize logging
"""

import logging
import warnings
from uvicorn.config import LOGGING_CONFIG

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Some weights of the model checkpoint.*were not used")
warnings.filterwarnings("ignore", message=".*return_all_scores.*is now deprecated.*")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Set logging levels for specific modules
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Custom logging configuration
CUSTOM_LOGGING_CONFIG = LOGGING_CONFIG.copy()
CUSTOM_LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
CUSTOM_LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'

# Disable specific loggers that generate noise
CUSTOM_LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = "INFO"
CUSTOM_LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = "INFO"
