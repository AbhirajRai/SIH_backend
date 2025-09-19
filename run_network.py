#!/usr/bin/env python3
"""
Network-optimized server for 0.0.0.0/0 access
"""

import uvicorn
import warnings
import logging
import os
import sys

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
    print("🌐 Starting network-optimized server...")
    print("📍 Server will be accessible on all network interfaces (0.0.0.0:8000)")
    print("🔗 Access URLs:")
    print("   - Local: http://localhost:8000")
    print("   - Local IP: http://127.0.0.1:8000")
    print("   - Network: http://[YOUR_IP]:8000")
    print("   - External: http://0.0.0.0:8000")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",  # Listen on all interfaces
            port=8000,
            reload=False,
            log_level="info",
            access_log=True,
            use_colors=True,
            # Network optimization settings
            loop="asyncio",
            # Increase limits for network access
            limit_max_requests=10000,
            limit_concurrency=1000,
            timeout_keep_alive=30,
            timeout_graceful_shutdown=30
        )
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
