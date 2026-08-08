import argparse
from tools.youtube_trend_tool import is_valid_query
import crewai.llms.cache as crewai_cache

# CrewAI/Groq compatibility workaround.
crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crew import crew
from services.sheets_service import add_content_ideas


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