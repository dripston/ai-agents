import os
import json
import sys
from textwrap import dedent
from crewai import Crew, Process, Task
from agents.developer_agent import DeveloperAgent
from agents.debugger_agent import DebuggerAgent

class DevelopmentCrew:
    def __init__(self, api_key, max_iterations=5):
        self.api_key = api_key
        self.max_iterations = max_iterations
        self.developer_agent = DeveloperAgent(api_key).create_developer_agent()
        self.debugger_agent = DebuggerAgent(api_key).create_debugger_agent()

    def create_development_task(self, requirements):
        return Task(
            description=dedent(f"""\
                Develop code based on the following requirements:
                {requirements}
                Your task is to create high-quality, well-structured code that meets these requirements.
                Ensure your code follows best practices and is well-documented.
            """),
            agent=self.developer_agent,
            expected_output="Complete implementation of the requirements with clean, well-documented code."
        )

    def create_debugging_task(self, code_to_review):
        return Task(
            description=dedent("""\
                Review the following code and identify any issues.
                Test the functionality and provide detailed feedback for improvements.
                If issues are found, clearly explain what needs to be fixed and why.
                
                IMPORTANT: End your response with one of these codes:
                -00 if the code is NOT approved (needs fixes)
                -11 if the code is approved for deployment
                
                Code to review:
            """) + str(code_to_review),
            agent=self.debugger_agent,
            expected_output="Detailed feedback on the code including any issues found and suggestions for improvements, ending with either '-00' for rejection or '-11' for approval."
        )

    def create_deployment_task(self, final_code):
        return Task(
            description=dedent(f"""\
                The following code has been approved by the debugger agent. Prepare it for deployment.
                Package the final code and provide it as the output.
                
                Approved code:
                {final_code}
            """),
            agent=self.debugger_agent,
            expected_output="Final code ready for deployment."
        )

    def send_update(self, status, message, progress, result=None):
        """Send update as JSON to stdout for streaming"""
        update = {
            "status": status,
            "message": message,
            "progress": progress
        }
        if result:
            update["result"] = result
            
        print(f"data: {json.dumps(update)}")
        sys.stdout.flush()

    def run_crew(self, requirements):
        code_context = requirements
        approved = False
        last_code = None
        debug_result = None

        # Send initial update
        self.send_update("started", "Starting development process...", 0)

        for i in range(self.max_iterations):
            self.send_update("processing", f"Starting iteration {i+1} of {self.max_iterations}", 10 + (i * 20))
            
            # Developer writes or fixes code
            self.send_update("processing", f"Developer agent generating code (iteration {i+1})", 15 + (i * 20))
            dev_task = self.create_development_task(code_context)
            dev_crew = Crew(
                agents=[self.developer_agent],
                tasks=[dev_task],
                process=Process.sequential,
            )
            dev_result = dev_crew.kickoff()

            last_code = dev_result
            self.send_update("processing", f"Developer completed code generation (iteration {i+1})", 20 + (i * 20))

            # Debugger reviews the actual code
            self.send_update("processing", f"Debugger agent reviewing code (iteration {i+1})", 25 + (i * 20))
            debug_task = self.create_debugging_task(last_code)
            debug_crew = Crew(
                agents=[self.debugger_agent],
                tasks=[debug_task],
                process=Process.sequential,
            )
            debug_result = debug_crew.kickoff()
            
            self.send_update("processing", f"Debugger completed review (iteration {i+1})", 30 + (i * 20))

            # Check for approval codes
            if "-11" in str(debug_result):
                approved = True
                self.send_update("processing", f"Code approved by debugger (iteration {i+1})", 35 + (i * 20))
                # Only deploy approved code
                self.send_update("processing", "Deploying approved code", 80)
                deploy_task = self.create_deployment_task(last_code)
                deploy_crew = Crew(
                    agents=[self.debugger_agent],
                    tasks=[deploy_task],
                    process=Process.sequential,
                )
                deploy_result = deploy_crew.kickoff()

                self.send_update("completed", "Process completed successfully", 100, {
                    "code": last_code,
                    "deployment": deploy_result
                })
                return f"Code has been approved and is ready for deployment:\n\n{last_code}\n\nDeployment result:\n\n{deploy_result}"
            elif "-00" in str(debug_result):
                # Feed feedback back to developer (not debugger)
                code_context = f"""
Original requirements:
{requirements}

Current code generated:
{last_code}

Debugger feedback:
{debug_result}

Please fix the code based on the feedback above.
"""
                self.send_update("processing", f"Code not approved, sending back to developer (iteration {i+1})", 35 + (i * 20))
            else:
                # Handle case where neither code is found (fallback)
                self.send_update("warning", f"Neither approval nor rejection code found, treating as rejection (iteration {i+1})", 35 + (i * 20))
                code_context = f"""
Original requirements:
{requirements}

Current code generated:
{last_code}

Debugger feedback:
{debug_result}

Please fix the code based on the feedback above.
"""

        # If we reach here, max iterations were reached without approval
        self.send_update("completed", "Max iterations reached without approval", 100, {
            "code": last_code,
            "feedback": debug_result,
            "status": "max_iterations_reached"
        })
        return f"Maximum iterations reached without approval from debugger. Last code generated:\n\n{last_code}\n\nFinal debugger feedback:\n\n{debug_result}"