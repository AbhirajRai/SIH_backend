#!/usr/bin/env python3
"""
Silent MindCare Backend Server Startup Script
Completely suppresses all warnings and output during startup
"""

import os
import sys
import warnings
import logging
import subprocess
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

# Suppress EVERYTHING
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Redirect all output
class SilentOutput:
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
    print("🚀 Starting MindCare Backend Server (Silent Mode)...")
    
    # Import with complete silence
    with SilentOutput():
        import uvicorn
        from uvicorn_config import CUSTOM_LOGGING_CONFIG
    
    print("✅ Server ready!")
    print("🌐 Server: http://0.0.0.0:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Start server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=CUSTOM_LOGGING_CONFIG,
        log_level="warning",  # Only show warnings and errors
        access_log=False,     # Disable access logs
        use_colors=False      # Disable colors
    )

if __name__ == "__main__":
    main()
