#!/usr/bin/env python3
"""
Run server with logging to file
"""

import logging
import sys
from datetime import datetime
import uvicorn
from app.main import app

# Configure logging
log_filename = f"server_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# File handler
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

print(f"📝 Logs will be saved to: {log_filename}")
print("🚀 Starting server with logging...")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
