#!/usr/bin/env python3
"""
View recent server logs
"""

import os
import glob
from datetime import datetime

def view_recent_logs():
    """View the most recent log files."""
    print("📋 Recent Server Logs")
    print("=" * 50)
    
    # Look for log files
    log_files = glob.glob("server_logs_*.log")
    
    if not log_files:
        print("❌ No log files found")
        print("💡 Run 'python run_with_logs.py' to create log files")
        return
    
    # Sort by modification time (newest first)
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    print(f"📁 Found {len(log_files)} log files:")
    for i, log_file in enumerate(log_files[:5]):  # Show last 5
        mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        print(f"  {i+1}. {log_file} (Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Show the most recent log
    if log_files:
        latest_log = log_files[0]
        print(f"\n📖 Showing latest log: {latest_log}")
        print("-" * 50)
        
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Show last 50 lines
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            for line in recent_lines:
                print(line.rstrip())
                
        except Exception as e:
            print(f"❌ Error reading log file: {e}")

def view_console_logs():
    """Instructions for viewing console logs."""
    print("\n🖥️  Console Logs (Real-time)")
    print("=" * 50)
    print("To see real-time logs:")
    print("1. Run: python run_minimal.py")
    print("2. Keep the terminal open")
    print("3. All server activity will be displayed there")
    print("\n💡 Press Ctrl+C to stop the server")

if __name__ == "__main__":
    view_recent_logs()
    view_console_logs()
