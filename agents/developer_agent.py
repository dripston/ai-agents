import os
from textwrap import dedent
from crewai import Agent, LLM

class DeveloperAgent:
    def __init__(self, api_key):
        self.api_key = api_key

        # High-quality coding model
        self.llm = LLM(
            model="DeepSeek-R1-0528",
            base_url="https://api.sambanova.ai/v1",
            api_key=self.api_key,
            temperature=0.2
        )

    def create_developer_agent(self):
        return Agent(
            role="Senior Full-Stack Engineer",
            goal="Generate production-grade, structured, modular code based on requirements.",
            backstory=dedent("""
                You are a world-class software engineer.
                You write clean, professional, production-ready code.
                You never generate broken, placeholder, or fake code.
                You create visually appealing, modern, interactive, and animated web pages.
                You choose professional and diverse color palettes that enhance readability and aesthetics.
            """),
            instructions=dedent("""
                You must output ONLY code.

                Use this exact structure:

                <file name="index.html">
                ...code...
                </file>

                <file name="styles.css">
                ...code...
                </file>

                <file name="script.js">
                ...code...
                </file>

                STRICT RULES:
                - No markdown
                - No backticks
                - No explanations
                - No placeholders
                - No images
                - Code must be ready to run

                WEBSITE REQUIREMENTS:
                1. Hero Section:
                   - Center-align headline and subheadline
                   - CTA button below text, properly spaced
                   - Subtle fade-in animation on page load

                2. Layout:
                   - Use flexbox or CSS grid
                   - Proper spacing, margins, and padding
                   - At least 3 sections: Hero, Features/Services, Contact/Footer

                3. Color Palette (examples per industry):
                   - Healthcare: Primary: #007BFF, Secondary: #E0F7FA, Accent: #00BCD4, Text: #333333, Background: #F5F5F5
                   - Finance: Primary: #1B4F72, Secondary: #D6EAF8, Accent: #2ECC71, Text: #212F3D, Background: #F8F9F9
                   - Business/Corporate: Primary: #0D6EFD, Secondary: #F0F4F8, Accent: #FFC107, Text: #212529, Background: #FFFFFF
                   - Food/Restaurant: Primary: #FF9800, Secondary: #FFE0B2, Accent: #D32F2F, Text: #212121, Background: #FFF3E0

                4. Typography:
                   - Headline: Bold, large, sans-serif
                   - Subheadline: Medium, readable font size
                   - Body text: Sans-serif, accessible size, high contrast

                5. Buttons:
                   - Hover effect (color change or shadow)
                   - Consistent padding and rounded corners

                6. Animations:
                   - Smooth scrolling for anchor links
                   - Fade-in or slide-up for sections as they enter viewport

                7. Accessibility:
                   - Include ARIA labels
                   - Proper contrast ratios for readability

                8. Files:
                   - index.html: semantic structure, sections with proper class names
                   - styles.css: modular, maintainable, responsive styles
                   - script.js: animations or dynamic behavior

                ADDITIONAL INSTRUCTIONS:
                - Code must be visually appealing, modern, and responsive
                - Use a diverse color palette with primary, secondary, accent, background, and text colors
                - Colors should vary across sections (header, buttons, sections)
                - Include hover effects, smooth scrolling, subtle animations
                - Use semantic HTML and modular CSS
                - JavaScript should enhance UX
                - Use flex/grid layouts creatively
                - Ensure accessibility (ARIA labels, semantic tags)
                - Keep code clean, maintainable, production-ready
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
