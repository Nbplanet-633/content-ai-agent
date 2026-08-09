from crewai import Task

from agents.researcher import researcher


research_task = Task(
    description=(
        "Research YouTube trends for the exact content niche: {niche}.\n\n"

        "Use the youtube_trend_search tool with the exact value "
        "of {niche} as the search query.\n\n"

        "Do not replace the requested niche with a broader or generic "
        "topic.\n\n"

        "Analyze the returned videos using:\n"
        "- views\n"
        "- views_per_day\n"
        "- engagement_rate\n"
        "- velocity_score\n"
        "- recency_score\n"
        "- trend_score\n"
        "- title\n"
        "- channel\n"
        "- published_at\n"
        "- URL\n\n"

                "Return a maximum of 4 trend clusters.\n\n"

        "Only include the strongest and most relevant clusters.\n\n"

        "Each trend cluster must contain no more than 3 supporting "
        "YouTube video URLs.\n\n"

        "Keep the reason concise, using no more than 2 sentences.\n\n"

        "Do not include the full video metadata in the final answer. "
        "Use the metadata internally to evaluate the trends, but return "
        "only the required trend cluster information.\n\n"

        "Identify recurring content patterns across multiple videos.\n\n"

        "Group related videos into meaningful trend clusters. "
        "A trend cluster must represent an underlying content theme "
        "supported by multiple videos whenever possible.\n\n"

        "Prioritize trends with strong trend scores, high velocity, "
        "good engagement, and recent activity.\n\n"

        "Return ONLY valid JSON using exactly this structure:\n\n"

        "{\n"
        '  "niche": "requested niche",\n'
        '  "trend_clusters": [\n'
        "    {\n"
        '      "trend": "name of trend",\n'
        '      "strength": 85,\n'
        '      "reason": "evidence-based explanation",\n'
        '      "supporting_videos": [\n'
        '        "https://www.youtube.com/watch?v=video1",\n'
        '        "https://www.youtube.com/watch?v=video2"\n'
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"

        "The strength must be between 0 and 100.\n"
        "supporting_videos must contain real URLs from the "
        "YouTube research.\n"
        "Do not invent videos, URLs, metrics, or trends."
    ),

    expected_output=(
        "A valid JSON research report containing the requested niche "
        "and a list of evidence-based trend clusters. "
        "Each cluster must contain trend, strength, reason, and "
        "supporting_videos."
    ),

    agent=researcher
)