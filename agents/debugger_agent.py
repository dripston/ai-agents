import os
from textwrap import dedent
from crewai import Agent, LLM

class DebuggerAgent:
    def __init__(self, api_key):
        self.api_key = api_key

        # More deterministic reviewer model
        self.llm = LLM(
            model="Meta-Llama-3.3-70B-Instruct",
            base_url="https://api.sambanova.ai/v1",
            api_key=self.api_key,
            temperature=0.2
        )

    def create_debugger_agent(self):
        return Agent(
            role="Code Reviewer",
            goal="Strictly validate code quality and correctness.",
            backstory="You are a strict senior engineer who never misses bugs.",
            instructions=dedent("""
                REVIEW RULES:
                
                If the code has NO issues:
                Respond ONLY with:
                -11
                
                If there are ANY issues:
                Respond EXACTLY in this format:
                
                -00
                Reason:
                <short explanation>
                
                Patch:
                <diff style patch>
                
                NO extra text.
                NO markdown.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )