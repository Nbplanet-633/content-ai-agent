from crewai import Task

from agents.analyst import analyst
from schemas.content_schema import ContentAnalysis
from tasks.research_task import research_task


analysis_task = Task(
    description=(
        "Analyze the YouTube trend research produced by the "
        "Content Trend Researcher.\n\n"

        "Use the actual YouTube videos and metrics provided by "
        "the Researcher as the basis for your analysis.\n\n"

        "Identify the strongest recurring topics, content formats, "
        "audience interests, and opportunities for the requested "
        "niche.\n\n"

        "Generate 5 to 10 actionable content ideas based directly "
        "on the researched YouTube trends.\n\n"

        "Every idea must be relevant to the requested niche and "
        "should be supported by the research.\n\n"

        "For each idea provide:\n"
        "- topic\n"
        "- suggested_angle\n"
        "- suggested_title\n"
        "- hook\n"
        "- trend_strength from 0 to 100\n"
        "- source_reference using a relevant YouTube URL"
    ),

    expected_output=(
        "Return a ContentAnalysis containing 5 to 10 actionable "
        "content ideas based on the YouTube research."
    ),

    output_pydantic=ContentAnalysis,

    agent=analyst,

    context=[research_task]
)