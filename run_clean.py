#!/usr/bin/env python3
"""
Clean MindCare Backend Server Startup Script
Runs the FastAPI application with complete warning suppression
"""

import os
import sys
import warnings
import logging
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

# Suppress ALL warnings and output before any imports
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set all logging to critical level
logging.getLogger().setLevel(logging.CRITICAL)
for logger_name in ["transformers", "torch", "urllib3", "httpx", "asyncio"]:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

class SuppressAllOutput:
    def __enter__(self):
        self._original_stderr = sys.stderr
        self._original_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        return self
    
    def __exit__(self, *args):
        sys.stderr = self._original_stderr
        sys.stdout = self._original_stdout

def main():
    """Main function to start the server."""
    print("🚀 Starting MindCare Backend Server...")
    
    # Import and initialize with output suppression
    with SuppressAllOutput():
        import uvicorn
        from uvicorn_config import CUSTOM_LOGGING_CONFIG
    
    print("✅ Server configuration loaded")
    print("🌐 Starting server on http://0.0.0.0:8000")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the server
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

if __name__ == "__main__":
    main()
