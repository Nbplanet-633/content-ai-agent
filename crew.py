from crewai import Crew, Process

from agents.researcher import researcher
from agents.analyst import analyst

from tasks.research_task import research_task
from tasks.analysis_task import analysis_task


crew = Crew(
    agents=[
        researcher,
        analyst
    ],

    tasks=[
        research_task,
        analysis_task
    ],

    process=Process.sequential,

    verbose=True
)