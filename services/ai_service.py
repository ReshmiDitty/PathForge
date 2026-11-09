"""
PathForge AI Service
--------------------
Handles intelligent generative completions using the Anthropic Claude API.
Gracefully and seamlessly falls back to `services.fallback_engine` whenever
no API key is configured or when external network calls are unavailable.
"""

import json
import logging
from config import config
from services import fallback_engine

logger = logging.getLogger(__name__)

# Initialize Anthropic client if key is configured
anthropic_client = None
if config.has_anthropic_key:
    try:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        logger.info("Anthropic Claude client initialized successfully.")
    except Exception as e:
        logger.warning(f"Could not initialize Anthropic client: {e}. Using fallback engine.")

def is_using_live_ai() -> bool:
    """Returns True if live Claude API is active and ready."""
    return anthropic_client is not None

def generate_ideas_ai(assessment_data: dict) -> list:
    """
    Generates 3-5 personalized venture ideas tailored to student's profile.
    """
    if not is_using_live_ai():
        return fallback_engine.generate_venture_ideas(assessment_data)

    try:
        prompt = (
            f"You are an expert venture ideation mentor for college students in India.\n"
            f"Generate 4 innovative, practical, and highly viable startup ideas for a student with this profile:\n"
            f"- Academic Branch: {assessment_data.get('branch')}\n"
            f"- Year of Study: {assessment_data.get('year_of_study')}\n"
            f"- Interests: {assessment_data.get('interests')}\n"
            f"- Skills: {assessment_data.get('skills')}\n"
            f"- Strengths: {assessment_data.get('strengths')}\n"
            f"- Risk Appetite (1-10): {assessment_data.get('risk_appetite')}\n\n"
            f"Return ONLY valid JSON as a list of objects with these exact keys: "
            f"title, tagline, category, problem_statement, target_customer, solution, why_now, revenue_model, complexity (Low, Medium, High)."
        )
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        content_text = message.content[0].text.strip()
        # Clean any markdown code blocks
        if content_text.startswith("```json"):
            content_text = content_text[7:]
        if content_text.endswith("```"):
            content_text = content_text[:-3]
        parsed = json.loads(content_text.strip())
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
    except Exception as e:
        logger.warning(f"Claude API idea generation error: {e}. Falling back to rule-based engine.")

    return fallback_engine.generate_venture_ideas(assessment_data)


def generate_lean_canvas_ai(idea_data: dict) -> dict:
    """
    Auto-populates Ash Maurya's 9-block Lean Canvas for an idea.
    """
    if not is_using_live_ai():
        return fallback_engine.generate_lean_canvas(idea_data)

    try:
        prompt = (
            f"You are an expert startup advisor teaching Lean Startup and Ash Maurya's Lean Canvas.\n"
            f"Create a complete 9-block Lean Canvas for the following venture idea:\n"
            f"Title: {idea_data.get('title')}\n"
            f"Problem: {idea_data.get('problem_statement')}\n"
            f"Target Customer: {idea_data.get('target_customer')}\n"
            f"Solution: {idea_data.get('solution')}\n"
            f"Why Now: {idea_data.get('why_now')}\n"
            f"Revenue: {idea_data.get('revenue_model')}\n\n"
            f"Return ONLY a valid JSON object with the following keys:\n"
            f"title, problem, existing_alternatives, customer_segments, early_adopters, "
            f"unique_value_proposition, high_level_concept, solution, channels, "
            f"revenue_streams, cost_structure, key_metrics, unfair_advantage."
        )
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        content_text = message.content[0].text.strip()
        if content_text.startswith("```json"):
            content_text = content_text[7:]
        if content_text.endswith("```"):
            content_text = content_text[:-3]
        parsed = json.loads(content_text.strip())
        if isinstance(parsed, dict) and "problem" in parsed:
            return parsed
    except Exception as e:
        logger.warning(f"Claude API Lean Canvas error: {e}. Using fallback.")

    return fallback_engine.generate_lean_canvas(idea_data)


def validate_idea_ai(idea_data: dict) -> dict:
    """
    Evaluates venture idea across 5 dimensions, calculates TAM/SAM/SOM, and produces SWOT.
    """
    if not is_using_live_ai():
        return fallback_engine.validate_idea_scorecard(idea_data)

    try:
        prompt = (
            f"Perform a rigorous venture validation scorecard on this startup idea:\n"
            f"Title: {idea_data.get('title')}\n"
            f"Problem: {idea_data.get('problem_statement')}\n"
            f"Customer: {idea_data.get('target_customer')}\n"
            f"Solution: {idea_data.get('solution')}\n\n"
            f"Score each dimension out of 20: Problem-Solution Fit, Market Sizing, Moat, Tech Feasibility, Unit Economics.\n"
            f"Total score is 0-100. Verdict must be 'GO' (>=78), 'REFINE' (65-77), or 'PIVOT' (<65).\n"
            f"Provide Indian TAM/SAM/SOM and SWOT analysis.\n"
            f"Return ONLY valid JSON matching this schema: "
            f'{{"total_score": int, "verdict": str, "verdict_message": str, "dimensions": dict, "swot": dict, "tam_sam_som": dict}}'
        )
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        content_text = message.content[0].text.strip()
        if content_text.startswith("```json"):
            content_text = content_text[7:]
        if content_text.endswith("```"):
            content_text = content_text[:-3]
        parsed = json.loads(content_text.strip())
        if isinstance(parsed, dict) and "total_score" in parsed:
            # Set appropriate badge style
            if parsed["total_score"] >= 78:
                parsed["verdict_badge"] = "bg-emerald-100 text-emerald-800 border-emerald-300"
            elif parsed["total_score"] >= 65:
                parsed["verdict_badge"] = "bg-amber-100 text-amber-800 border-amber-300"
            else:
                parsed["verdict_badge"] = "bg-rose-100 text-rose-800 border-rose-300"
            return parsed
    except Exception as e:
        logger.warning(f"Claude API validator error: {e}. Using fallback.")

    return fallback_engine.validate_idea_scorecard(idea_data)


def mentor_chat_ai(query: str, user_profile: dict, active_idea: dict = None) -> str:
    """
    Answers student questions regarding career choices, venture ideation, or coursework.
    """
    if not is_using_live_ai():
        return fallback_engine.ai_mentor_respond(query, user_profile, active_idea)

    try:
        system_prompt = (
            f"You are the PathForge AI Mentor, an empathetic, highly knowledgeable advisor "
            f"specializing in college career guidance, entrepreneurship courses, Lean Startup, "
            f"and the Indian startup ecosystem (SISFS, NIDHI-PRAYAS, T-Hub, etc.).\n"
            f"Current Student: {user_profile.get('name', 'Student')}, Major: {user_profile.get('branch', 'Engineering')}.\n"
            f"Active Venture: {active_idea.get('title') if active_idea else 'None selected yet'}.\n"
            f"Provide crisp, structured, practical guidance using markdown bullet points and bold highlights."
        )
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": query}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.warning(f"Claude API chat error: {e}. Using fallback.")
        return fallback_engine.ai_mentor_respond(query, user_profile, active_idea)

