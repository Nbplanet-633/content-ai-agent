from crewai import Task

from agents.researcher import researcher


research_task = Task(
    description=(
        "Research YouTube trends for the exact niche: {niche}.\n\n"

        "Use the youtube_trend_search tool with the exact value "
        "of {niche} as the search query.\n\n"

        "Do not replace the requested niche with a broader topic.\n\n"

        "After receiving the YouTube results, analyze the videos "
        "using views_per_day, engagement_rate, trend_score, "
        "and recency.\n\n"

        "Identify the strongest trends and explain why they are "
        "promising content opportunities."
    ),

    expected_output=(
        "Return a clear research report containing the YouTube "
        "videos found for the requested niche and their relevant "
        "metrics, including title, channel, views, views_per_day, "
        "engagement_rate, trend_score, published_at, URL, and "
        "a concise explanation of the trend."
    ),

    agent=researcher
)