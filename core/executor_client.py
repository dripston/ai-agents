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
            updates = crew.run_crew(requirements)
            
            # Yield each update
            for update in updates:
                yield update
                
        except Exception as e:
            # Send error update
            error_update = {
                "status": "error",
                "message": f"Error occurred during development process: {str(e)}",
                "progress": 0
            }
            yield f"data: {json.dumps(error_update)}\n\n"

# For direct CLI usage
def main():
    # Example usage - only run when called directly with --cli flag
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        client = ExecutorClient()
        requirements = input("Enter your development requirements: ")
        
        # For CLI, collect all updates and print the final result
        final_result = ""
        for update in client.run_development_process(requirements):
            print(update, end='')
            sys.stdout.flush()
            
            # Try to extract result from completed update
            if "data:" in update:
                try:
                    json_str = update.split("data:")[1].strip()
                    data = json.loads(json_str)
                    if data.get("status") == "completed" and "result" in data:
                        final_result = data["result"]
                except:
                    pass
        
        print("\nDevelopment process completed with result:")
        print(final_result)

if __name__ == "__main__":
    main()