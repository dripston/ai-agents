import os
import sys
import json
from core.executor_client import ExecutorClient

def main():
    """
    Main entry point for the Crew AI Developer and Debugger system
    """
    print("Welcome to the Crew AI Developer and Debugger System")
    print("=" * 50)
    
    # Initialize the executor client
    client = ExecutorClient()
    
    # Get requirements from user
    print("\nEnter your development requirements below (press Enter twice to submit):")
    print("-" * 50)
    
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
            
    requirements = '\n'.join(lines)
    
    if not requirements.strip():
        # Send error update
        error_update = {
            "status": "error",
            "message": "No requirements provided. Exiting.",
            "progress": 0
        }
        print(f"data: {json.dumps(error_update)}")
        sys.stdout.flush()
        return
    
    print("\nStarting development process...")
    print("-" * 50)
    
    # Get max iterations from user (optional)
    try:
        max_iter_input = input("Enter maximum iterations (default 5, press Enter for default): ")
        max_iterations = int(max_iter_input) if max_iter_input.strip() else 5
    except ValueError:
        max_iterations = 5
        print("Invalid input. Using default maximum iterations (5).")
    
    # Run the development process
    result = client.run_development_process(requirements, max_iterations)
    
    # Display results (for compatibility with existing usage)
    print("\nDevelopment process completed!")
    print("=" * 50)
    print("Results:")
    print(result)

if __name__ == "__main__":
    main()