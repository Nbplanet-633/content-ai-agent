from crewai import Agent, LLM

from tools.youtube_trend_tool import youtube_trend_search


llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0
)


researcher = Agent(
    role="Content Trend Researcher",

    goal=(
        "Find relevant YouTube content trends for the exact "
        "niche provided by the user."
    ),

    backstory=(
        "You are a YouTube trend researcher. "
        "You use the YouTube search tool to find videos "
        "related to the requested niche."
    ),

    tools=[youtube_trend_search],

    llm=llm,

    verbose=True
)