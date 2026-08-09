from crewai import Task

from agents.analyst import analyst
from schemas.content_schema import ContentAnalysis
from tasks.research_task import research_task


analysis_task = Task(
    description=(
        "Analyze the structured trend research produced by the "
        "Content Trend Researcher.\n\n"

        "The research contains trend clusters identified from "
        "multiple YouTube videos.\n\n"

        "Use the trend clusters as the PRIMARY source for generating "
        "content ideas.\n\n"

        "For each trend cluster, consider:\n"
        "- trend name\n"
        "- trend strength\n"
        "- reason the trend is promising\n"
        "- supporting YouTube videos\n\n"

        "Prioritize the strongest trend clusters rather than treating "
        "every individual video as a separate opportunity.\n\n"

        "Generate 5 to 10 unique and actionable content ideas.\n\n"

        "Avoid generating multiple ideas that are essentially the "
        "same topic.\n\n"

        "For every content idea provide:\n"
        "- topic\n"
        "- suggested_angle\n"
        "- suggested_title\n"
        "- hook\n"
        "- trend_strength from 0 to 100\n"
        "- content_format\n"
        "- target_audience\n"
        "- source_reference using a supporting YouTube URL\n\n"

        "content_format must describe the recommended format for "
        "creating the content. Use a concise format such as "
        "Long-form Video, Short, Vlog, Tutorial, Interview, "
        "Comparison, or Challenge.\n\n"

        "target_audience must identify the primary audience for the "
        "idea, such as IIT aspirants, JEE aspirants, current IIT "
        "students, college students, or parents.\n"

        "The content ideas must remain relevant to the requested "
        "niche and must be grounded in the identified trend clusters.\n\n"

        "Do not invent YouTube URLs or claim a trend is supported "
        "unless it appears in the research."
                "IMPORTANT RULES FOR EVIDENCE:\n"

        "1. Every content idea must be directly derived from "
        "one of the provided trend clusters.\n\n"

        "2. Do not introduce a new topic, angle, or content category "
        "that is not supported by the trend cluster.\n\n"

        "3. The suggested_angle must clearly match the trend.\n\n"

        "4. The suggested_title must clearly match both the topic "
        "and suggested_angle.\n\n"

        "5. trend_strength must be based on the strength of the "
        "trend cluster that produced the idea.\n\n"

        "6. source_reference must be one of the supporting_videos "
        "from that same trend cluster.\n\n"

        "7. Do not use a supporting video from one cluster as the "
        "source for an idea generated from another cluster.\n\n"

        "8. Prefer specific creator-oriented ideas over generic "
        "informational topics.\n\n"
    ),

    expected_output=(
        "Return a ContentAnalysis containing 5 to 10 unique content "
        "ideas derived from the strongest trend clusters in the "
        "research. Each idea must include topic, suggested_angle, "
        "suggested_title, hook, trend_strength, content_format, "
        "target_audience, and source_reference."
    ),

    output_pydantic=ContentAnalysis,

    agent=analyst,

    context=[research_task]
)