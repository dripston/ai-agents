#!/usr/bin/env python3
"""
Stream handler for Render deployment - provides continuous updates for Vercel app
"""
import sys
import json
import select
import subprocess
from threading import Thread
from queue import Queue, Empty

def stream_subprocess(command):
    """
    Run a subprocess and stream its output line by line
    """
    try:
        # Start the subprocess
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Read output line by line
        while True:
            # Check if process has terminated
            if process.poll() is not None:
                break
                
            # Read line with timeout
            try:
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
                    sys.stdout.flush()
            except:
                break
                
        # Read any remaining output
        remaining = process.stdout.read()
        if remaining:
            print(remaining.rstrip())
            sys.stdout.flush()
            
        process.wait()
        
    except Exception as e:
        error_msg = {
            "status": "error",
            "message": f"Failed to start process: {str(e)}",
            "progress": 0
        }
        print(f"data: {json.dumps(error_msg)}")
        sys.stdout.flush()

def main():
    """
    Main entry point for streaming handler
    """
    # Send initial connection message
    init_msg = {
        "status": "connected",
        "message": "Stream handler connected",
        "progress": 0
    }
    print(f"data: {json.dumps(init_msg)}")
    sys.stdout.flush()
    
    # Run the main application with streaming
    stream_subprocess([sys.executable, "main.py"])

if __name__ == "__main__":
    main()