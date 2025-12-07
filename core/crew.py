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

    def generate_updates(self, status, message, progress, result=None):
        """Generate update as JSON"""
        update = {
            "status": status,
            "message": message,
            "progress": progress
        }
        if result:
            # Convert result to string if it's not already serializable
            try:
                json.dumps(result)
                update["result"] = result
            except TypeError:
                update["result"] = str(result)
            
        return f"data: {json.dumps(update)}\n\n"

    def run_crew(self, requirements):
        code_context = requirements
        approved = False
        last_code = None
        debug_result = None

        # Send initial update
        yield self.generate_updates("started", "Starting development process...", 0)

        for i in range(self.max_iterations):
            yield self.generate_updates("processing", f"Starting iteration {i+1} of {self.max_iterations}", 10 + (i * 20))
            
            # Developer writes or fixes code
            yield self.generate_updates("processing", f"Developer agent generating code (iteration {i+1})", 15 + (i * 20))
            dev_task = self.create_development_task(code_context)
            dev_crew = Crew(
                agents=[self.developer_agent],
                tasks=[dev_task],
                process=Process.sequential,
            )
            dev_result = dev_crew.kickoff()

            # Convert CrewOutput to string
            last_code = str(dev_result)
            yield self.generate_updates("processing", f"Developer completed code generation (iteration {i+1})", 20 + (i * 20))

            # Debugger reviews the actual code
            yield self.generate_updates("processing", f"Debugger agent reviewing code (iteration {i+1})", 25 + (i * 20))
            debug_task = self.create_debugging_task(last_code)
            debug_crew = Crew(
                agents=[self.debugger_agent],
                tasks=[debug_task],
                process=Process.sequential,
            )
            debug_result = debug_crew.kickoff()
            
            yield self.generate_updates("processing", f"Debugger completed review (iteration {i+1})", 30 + (i * 20))

            # Check for approval codes
            if "-11" in str(debug_result):
                approved = True
                yield self.generate_updates("processing", f"Code approved by debugger (iteration {i+1})", 35 + (i * 20))
                # Only deploy approved code
                yield self.generate_updates("processing", "Deploying approved code", 80)
                deploy_task = self.create_deployment_task(last_code)
                deploy_crew = Crew(
                    agents=[self.debugger_agent],
                    tasks=[deploy_task],
                    process=Process.sequential,
                )
                deploy_result = deploy_crew.kickoff()

                yield self.generate_updates("completed", "Process completed successfully", 100, {
                    "code": last_code,
                    "deployment": str(deploy_result)
                })
                return
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
                yield self.generate_updates("processing", f"Code not approved, sending back to developer (iteration {i+1})", 35 + (i * 20))
            else:
                # Handle case where neither code is found (fallback)
                yield self.generate_updates("warning", f"Neither approval nor rejection code found, treating as rejection (iteration {i+1})", 35 + (i * 20))
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
        yield self.generate_updates("completed", "Max iterations reached without approval", 100, {
            "code": last_code,
            "feedback": str(debug_result),
            "status": "max_iterations_reached"
        })