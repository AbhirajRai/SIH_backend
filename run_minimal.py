#!/usr/bin/env python3
"""
Minimal server startup to isolate issues
"""

import uvicorn
import warnings
import logging
import os

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set logging levels
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("torch").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    print("🚀 Starting minimal server...")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to avoid issues
            log_level="info",
            access_log=True,
            use_colors=True
        )
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
