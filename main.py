import argparse
import json

from tools.youtube_trend_tool import is_valid_query
import crewai.llms.cache as crewai_cache

# CrewAI/Groq compatibility workaround.
crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crew import crew
from services.sheets_service import add_content_ideas
from services.mongo_service import (
    save_trend_clusters,
    save_content_ideas
)
def parse_arguments():

    parser = argparse.ArgumentParser(
        description="AI-powered YouTube content trend research agent."
    )

    parser.add_argument(
        "--niche",
        type=str,
        default="student life",
        help="Content niche to research."
    )

    return parser.parse_args()

def parse_research_output(raw_output):
    """
    Parse the Researcher's JSON output.
    """

    if not raw_output:
        return None

    raw_output = raw_output.strip()

    # Remove markdown code fences if the LLM added them.
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw_output = "\n".join(lines).strip()

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError as error:
        print("\nResearch output could not be parsed as JSON.")
        print(f"JSON error: {error}")
        return None

def main():

    args = parse_arguments()

    if not is_valid_query(args.niche):
        print(
            f"\nInvalid niche: '{args.niche}'"
        )
        print(
            "Please provide a meaningful content niche."
        )
        return

    print(
        f"\nStarting Content Trend Agent for niche: "
        f"{args.niche}\n"
    )

    result = crew.kickoff(
        inputs={
            "niche": args.niche
        }
    )

    # ---------------------------------------------------------
    # Save Researcher trend clusters to MongoDB
    # ---------------------------------------------------------

    if result.tasks_output:

        researcher_output = result.tasks_output[0]

        research_data = parse_research_output(
            researcher_output.raw
        )

        if research_data:

            trend_clusters = research_data.get(
                "trend_clusters",
                []
            )

            if trend_clusters:

                saved_clusters = save_trend_clusters(
                    args.niche,
                    trend_clusters
                )

                print(
                    f"\nSaved {saved_clusters} trend clusters "
                    f"to MongoDB."
                )

            else:
                print(
                    "\nResearcher returned no trend clusters."
                )

        else:
            print(
                "\nCould not parse Researcher output."
            )

    print("\n===== DEBUG RESULT =====")
    print("RAW:")
    print(result.raw)

    print("\nPYDANTIC:")
    print(result.pydantic)

    if result.pydantic:
        print("\nIDEAS:")
        print(result.pydantic.ideas)

    print("\n\n===== FINAL RESULT =====\n")
    print(result)

    if hasattr(result, "pydantic") and result.pydantic:

        ideas = result.pydantic.ideas

        if not ideas:
            print(
                "\nNo valid content ideas were generated."
            )
            return

        mongo_ideas_result = save_content_ideas(
            args.niche,
            [
                idea.model_dump()
                for idea in ideas
            ]
        )

        print(
            f"\nSaved {mongo_ideas_result} content ideas "
            f"to MongoDB."
        )

        sheets_result = add_content_ideas(
            [
                idea.model_dump()
                for idea in ideas
            ]
        )

        print(
            f"\nAdded {sheets_result['added']} new ideas "
            f"to Google Sheets."
        )

        print(
            f"Skipped {sheets_result['skipped']} duplicate ideas."
        )

    else:
        print(
            "\nNo structured ContentAnalysis was returned."
        )


if __name__ == "__main__":
    main()