#!/usr/bin/env python3
"""
MindCare Backend Server Startup Script
Runs the FastAPI application with optimized uvicorn configuration
"""

import uvicorn
import warnings
import logging
from uvicorn_config import CUSTOM_LOGGING_CONFIG

# Suppress warnings before importing the app
warnings.filterwarnings("ignore", message="Some weights of the model checkpoint.*were not used")
warnings.filterwarnings("ignore", message=".*return_all_scores.*is now deprecated.*")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Set logging levels
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=CUSTOM_LOGGING_CONFIG,
        log_level="info",
        access_log=True,
        use_colors=True
    )
