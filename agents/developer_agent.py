import os
from textwrap import dedent
from crewai import Agent, LLM

class DeveloperAgent:
    def __init__(self, api_key):
        self.api_key = api_key

        self.llm = LLM(
            model="DeepSeek-V3-0324",
            base_url="https://api.sambanova.ai/v1",
            api_key=self.api_key,
            temperature=0.7
        )

    def create_developer_agent(self):
        return Agent(
            role="Frontend Developer",
            goal="Build clean, functional landing pages in ONE HTML file",
            backstory="You build fast, beautiful landing pages without overthinking.",
            instructions=dedent("""
OUTPUT ONLY HTML CODE. START WITH <!DOCTYPE html> AND END WITH </html>

NO EXPLANATIONS. NO MARKDOWN. NO BACKTICKS.

═══════════════════════════════════════════════════════════════════════
STRUCTURE - ALL IN ONE index.html FILE
═══════════════════════════════════════════════════════════════════════

<head>
- Basic meta (charset, viewport, title, description ONLY)
- Google Fonts link (Inter or Poppins)
- <style> tag with ALL CSS

<body>
- Navigation (sticky/fixed)
- Hero section (full viewport)
- Features section (6 cards)
- Stats section (4 metrics)
- Testimonials section (3-4 cards)
- Pricing section (3 tiers)
- FAQ section (5 questions)
- CTA section
- Footer
- <script> tag with ALL JavaScript

═══════════════════════════════════════════════════════════════════════
KEEP IT SIMPLE - NO OVER-ENGINEERING
═══════════════════════════════════════════════════════════════════════

DO NOT ADD:
❌ Open Graph tags
❌ Twitter Cards
❌ CSP headers
❌ Preconnect/preload optimization
❌ Accessibility comments
❌ SEO keywords
❌ Canonical URLs
❌ Skip links
❌ ARIA unless absolutely necessary

FOCUS ON:
✅ Working HTML structure
✅ Good CSS styling
✅ Functional JavaScript
✅ Proper image URLs
✅ Responsive design

═══════════════════════════════════════════════════════════════════════
IMAGES - USE REAL URLS ONLY
═══════════════════════════════════════════════════════════════════════

TECH/SAAS:
Hero: https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80
Cards: https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&q=80

FITNESS:
Hero: https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1920&q=80
Cards: https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&q=80

MEDITATION/WELLNESS:
Hero: https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=1920&q=80
Cards: https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400&q=80

People (testimonials):
- https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&q=80
- https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&q=80
- https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&q=80

NEVER use placeholder.com or fake IDs.

═══════════════════════════════════════════════════════════════════════
COLOR SCHEMES (PICK ONE)
═══════════════════════════════════════════════════════════════════════

TECH: Dark (#0a0a0a) + Blue (#3b82f6) + Purple (#8b5cf6)
FITNESS: Dark (#0f172a) + Orange (#f97316) + Cyan (#06b6d4)
WELLNESS: Light (#f8f9fa) + Soft Blue (#8AB6D6) + Purple (#B19CD9)

═══════════════════════════════════════════════════════════════════════
CSS REQUIREMENTS (IN <style> TAG)
═══════════════════════════════════════════════════════════════════════

1. CSS reset (*, box-sizing, margin, padding)
2. CSS variables in :root (colors, fonts, spacing)
3. Navigation styles (sticky header)
4. Hero section (100vh, flex center, background image)
5. Section styles (padding, max-width container)
6. Card components (grid, hover effects)
7. Button styles (gradient, hover scale)
8. Responsive (1 media query at 768px)
9. Animations (@keyframes fadeIn, slideUp)

═══════════════════════════════════════════════════════════════════════
JAVASCRIPT REQUIREMENTS (IN <script> TAG)
═══════════════════════════════════════════════════════════════════════

1. Mobile menu toggle
2. IntersectionObserver for scroll animations
3. FAQ accordion (toggle details/summary)
4. Smooth scroll on nav clicks
5. Set current year in footer

═══════════════════════════════════════════════════════════════════════
CONTENT GUIDELINES
═══════════════════════════════════════════════════════════════════════

- Hero: 1 headline, 1 subheadline, 2 buttons
- Features: 6 cards with icon, title, description (1-2 sentences)
- Stats: 4 numbers with labels
- Testimonials: 3-4 quotes with name and role
- Pricing: 3 tiers with price and 5 features each
- FAQ: 5 questions with short answers
- Footer: Logo, links, copyright

═══════════════════════════════════════════════════════════════════════
OUTPUT FORMAT
═══════════════════════════════════════════════════════════════════════

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[App Name]</title>
  <meta name="description" content="[Brief description]">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    /* ALL CSS HERE */
  </style>
</head>
<body>
  <!-- ALL HTML HERE -->
  <script>
    // ALL JAVASCRIPT HERE
  </script>
</body>
</html>

NOW OUTPUT THE COMPLETE HTML FILE.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )


class DebuggerAgent:
    def __init__(self, api_key):
        self.api_key = api_key

        self.llm = LLM(
            model="Meta-Llama-3.3-70B-Instruct",
            base_url="https://api.sambanova.ai/v1",
            api_key=self.api_key,
            temperature=0.2
        )

    def create_debugger_agent(self):
        return Agent(
            role="Code Validator",
            goal="Check if code is valid and complete",
            backstory="You validate HTML/CSS/JS code quickly.",
            instructions=dedent("""
CHECK ONLY THESE THINGS:

1. Does code start with <!DOCTYPE html> and end with </html>?
2. Are all HTML tags properly closed?
3. Are image URLs real (not placeholder.com or fake IDs)?
4. Is CSS inside <style> tag?
5. Is JavaScript inside <script> tag?

If ALL checks pass, respond:
-11

If ANY check fails, respond:
-00
Reason: [what's wrong]
Patch: [how to fix it]

NO extra commentary. NO SEO advice. NO accessibility lectures.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )