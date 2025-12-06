import os
import sys
import json
from dotenv import load_dotenv
from core.crew import DevelopmentCrew

class ExecutorClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("SAMBANOVA_API_KEY") or "2cfa9823-371b-4dfa-a79f-f1cdf58905bf"
        
    def run_development_process(self, requirements, max_iterations=5):
        """
        Execute the development process with the given requirements
        """
        try:
            # Create and run the development crew
            crew = DevelopmentCrew(self.api_key, max_iterations)
            result = crew.run_crew(requirements)
            
            return result
        except Exception as e:
            # Send error update
            error_update = {
                "status": "error",
                "message": f"Error occurred during development process: {str(e)}",
                "progress": 0
            }
            print(f"data: {json.dumps(error_update)}")
            sys.stdout.flush()
            return f"Error occurred during development process: {str(e)}"

if __name__ == "__main__":
    # Example usage
    client = ExecutorClient()
    requirements = input("Enter your development requirements: ")
    result = client.run_development_process(requirements)
    print("Development process completed with result:")
    print(result)