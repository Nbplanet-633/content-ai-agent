from tools.youtube_api import search_niche_videos


query = "student life at IIT"

print("\n===== YOUTUBE API TEST =====")
print("Query:", query)

videos = search_niche_videos(
    query=query,
    region_code="IN",
    max_results=5
)

print("Videos found:", len(videos))

for i, video in enumerate(videos, start=1):

    print(f"\n--- Video {i} ---")
    print("Title:", video.get("title"))
    print("Channel:", video.get("channel"))
    print("Views:", video.get("views"))
    print("URL:", video.get("url"))