# 🤖 Content AI Agent

An AI-powered YouTube content trend research agent that discovers trending topics within a given niche, analyzes high-performing videos, identifies trend clusters, generates actionable content ideas, and stores the research in MongoDB and Google Sheets.

The project uses **CrewAI for multi-agent orchestration**, the **YouTube Data API for research**, **Python-based trend scoring**, **Groq LLMs for reasoning**, **MongoDB Atlas for persistent storage**, and **Google Sheets for easy content-idea management**.

---

## 🚀 What It Does

Given a niche such as:

```text
student life at IIT Madras
```

the agent:

```text
User Niche
    ↓
YouTube Search
    ↓
20 Candidate Videos
    ↓
Views / Likes / Comments
    ↓
Views-per-Day + Engagement Rate
    ↓
Trend Score
    ↓
Top 8 Videos
    ↓
Content Trend Researcher
    ↓
Trend Clusters
    ↓
Content Strategy Analyst
    ↓
Content Ideas
    ├──→ MongoDB
    └──→ Google Sheets
```

---

## ✨ Features

### 🔎 YouTube Trend Research

The agent searches YouTube for videos related to the requested niche using the YouTube Data API.

For each video, it collects information such as:

* Video ID
* Title
* Channel
* Publication date
* Views
* Likes
* Comments
* YouTube URL

---

### 📊 Trend Scoring

Videos are ranked using a custom trend-scoring system.

The scoring considers:

* Views velocity
* Engagement rate
* Recency

### Views Per Day

```text
Views Per Day =
Total Views / Video Age in Days
```

### Engagement Rate

```text
Engagement Rate =
(Likes + Comments) / Views × 100
```

### Trend Score

The current scoring model uses:

```text
Views Velocity → 50%
Engagement     → 30%
Recency        → 20%
```

Logarithmic scaling is used for views velocity so that extremely viral videos do not completely dominate the ranking.

---

## 🧠 AI Agent Architecture

The project currently uses two CrewAI agents.

### 1. Content Trend Researcher

Responsibilities:

* Analyze the top YouTube videos
* Identify common trends
* Group related videos into trend clusters
* Estimate trend strength
* Explain why each trend is promising
* Provide supporting YouTube videos

Example output:

```json
{
  "trend": "Campus Life at IIT Madras",
  "strength": 85,
  "reason": "Multiple videos showcasing campus life...",
  "supporting_videos": [
    "https://www.youtube.com/watch?v=..."
  ]
}
```

---

### 2. Content Strategy Analyst

The Analyst uses the Researcher's trend clusters as its primary source.

It generates actionable content ideas containing:

* Topic
* Suggested angle
* Suggested title
* Hook
* Trend strength
* Content format
* Target audience
* Source reference

Example:

```json
{
  "topic": "Hostel Life at IIT Madras",
  "suggested_angle": "Honest hostel experience",
  "suggested_title": "7 Things Nobody Tells You About IIT Hostel Life",
  "hook": "Think IIT hostel life is just rooms and studying? Think again.",
  "trend_strength": 82,
  "content_format": "Vlog",
  "target_audience": "IIT students",
  "source_reference": "https://www.youtube.com/watch?v=..."
}
```

---

# 🗄️ Data Storage

The project currently uses **MongoDB Atlas** as the primary persistent database.

### Database

```text
content_ai_agent
```

### Collections

```text
content_ai_agent
│
├── videos
├── trend_clusters
└── content_ideas
```

### `videos`

Stores YouTube research data:

```text
video_id
niche
title
channel
published_at
views
likes
comments
views_per_day
engagement_rate
trend_score
url
created_at
```

### `trend_clusters`

Stores Researcher findings:

```text
niche
trend
strength
reason
supporting_videos
created_at
```

### `content_ideas`

Stores Analyst-generated ideas:

```text
niche
topic
suggested_title
suggested_angle
hook
trend_strength
content_format
target_audience
source_reference
created_at
```

MongoDB writes use update/upsert logic where appropriate to reduce duplicate records.

---

# 📋 Google Sheets Integration

Generated content ideas are also exported to Google Sheets.

The Sheets integration:

* Adds new ideas
* Detects duplicate topics
* Skips existing topics
* Prevents duplicates within the same AI response
* Adds the generation date

This makes the output easy to review and manage manually.

---

# 🛠️ Tech Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core application          |
| CrewAI                | Multi-agent orchestration |
| Groq                  | LLM inference             |
| Llama 3.1 / Llama 3.3 | AI reasoning              |
| YouTube Data API      | YouTube research          |
| PyMongo               | MongoDB integration       |
| MongoDB Atlas         | Persistent database       |
| Google Sheets API     | Content idea management   |
| Pydantic              | Structured AI output      |
| python-dotenv         | Environment configuration |

---

# 📁 Project Structure

```text
content-trend-agent/
│
├── agents/
│   ├── researcher.py
│   └── analyst.py
│
├── config/
│   └── settings.py
│
├── services/
│   ├── mongo_service.py
│   └── sheets_service.py
│
├── tasks/
│   ├── research_task.py
│   └── analysis_task.py
│
├── tools/
│   ├── youtube_api.py
│   └── youtube_trend_tool.py
│
├── test/
│   ├── test_mongo.py
│   ├── test_mongo_videos.py
│   ├── test_mongo_clusters.py
│   ├── test_mongo_ideas.py
│   └── test_youtube_mongo.py
│
├── .env
├── .gitignore
├── crew.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd content-trend-agent
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
YOUTUBE_API_KEY=your_youtube_api_key

GOOGLE_SHEET_ID=your_google_sheet_id

MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=content_ai_agent
```

Never commit your `.env` file.

Your `.gitignore` should contain:

```gitignore
.env
credentials.json
token.json
venv/
__pycache__/
*.pyc
```

---

# 📊 Google Sheets Setup

The project uses Google Sheets API authentication.

Place your Google OAuth credentials file in the project root:

```text
credentials.json
```

The first authentication run will generate:

```text
token.json
```

Both files should remain local and must **not** be committed to GitHub.

---

# 🍃 MongoDB Atlas Setup

Create a MongoDB Atlas cluster and database user.

Set the connection string in `.env`:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
MONGO_DB_NAME=content_ai_agent
```

The application will automatically create the required collections when data is inserted:

```text
videos
trend_clusters
content_ideas
```

---

# ▶️ Running the Agent

Run the agent with:

```powershell
python main.py --niche "student life at IIT Madras"
```

You can use any meaningful niche.

For example:

```powershell
python main.py --niche "college student productivity"
```

```powershell
python main.py --niche "Indian college life"
```

```powershell
python main.py --niche "AI tools for students"
```

---

# 🔄 Example Workflow

For:

```text
student life at IIT Madras
```

the agent might discover:

```text
20 YouTube candidate videos
        ↓
Trend scoring
        ↓
Top 8 videos
        ↓
Researcher
        ↓
Campus Life
Hostel Life
Placements
Student Experiences
        ↓
Analyst
        ↓
Content Ideas
```

The final ideas are saved to:

```text
MongoDB
+
Google Sheets
```

---

# 🧪 Testing

The project contains independent tests for the major components.

### Test MongoDB connection

```powershell
python -m test.test_mongo
```

### Test video storage

```powershell
python -m test.test_mongo_videos
```

### Test trend-cluster storage

```powershell
python -m test.test_mongo_clusters
```

### Test content-idea storage

```powershell
python -m test.test_mongo_ideas
```

### Test YouTube → MongoDB integration

```powershell
python -m test.test_youtube_mongo
```

---

# 🛡️ Error Handling

The project includes handling for several common failures:

* Invalid niche queries
* YouTube API failures
* Missing YouTube results
* Missing video metrics
* MongoDB connection errors
* Duplicate database records
* Duplicate content ideas
* Invalid structured LLM responses
* LLM rate-limit errors

The application also validates the requested niche before starting the CrewAI workflow.

---

# 📌 Current Status

### Core Agent

* [x] YouTube API integration
* [x] YouTube video search
* [x] Video metrics collection
* [x] Views-per-day calculation
* [x] Engagement-rate calculation
* [x] Trend-score calculation
* [x] Top-video filtering
* [x] CrewAI Researcher agent
* [x] Trend clustering
* [x] CrewAI Analyst agent
* [x] Structured content ideas
* [x] Content idea validation

### Storage

* [x] MongoDB Atlas
* [x] Video storage
* [x] Trend-cluster storage
* [x] Content-idea storage
* [x] Duplicate-safe database updates
* [x] Google Sheets integration
* [x] Duplicate idea filtering

### Testing

* [x] MongoDB connection test
* [x] Video storage test
* [x] Trend-cluster test
* [x] Content-idea test
* [x] YouTube + MongoDB integration test
* [x] End-to-end pipeline testing

---

# 🔮 Future Roadmap

The core AI research pipeline is currently functional. Planned improvements include:

### Backend API

Build a FastAPI layer:

```text
POST /research
GET /ideas
GET /trends
GET /videos
GET /research/history
```

### Web Dashboard

Create a React dashboard for:

* Running research
* Viewing trends
* Browsing content ideas
* Viewing research history
* Tracking trend performance

### Historical Trend Analysis

Store research runs over time to identify:

```text
🔥 Emerging trends
📈 Growing trends
🟢 Stable trends
📉 Declining trends
```

### Automation

Allow users to schedule recurring research instead of manually running the CLI.

### Notifications

Send alerts when a significant new trend is detected.

---

# 🎯 Project Goal

The long-term goal is to build an **AI-powered content intelligence platform** that doesn't simply generate random content ideas.

Instead, it should:

```text
Discover
   ↓
Measure
   ↓
Analyze
   ↓
Cluster
   ↓
Identify Opportunities
   ↓
Generate
   ↓
Store
   ↓
Track
```

The focus is on generating content ideas that are **grounded in actual audience and YouTube trend data** rather than relying solely on an LLM's general knowledge.

---

## 👨‍💻 Author

**Neeraj Meena**

Built as an AI/ML engineering project exploring:

* LLM-powered agents
* Multi-agent orchestration
* YouTube data analysis
* Trend detection
* Generative AI
* MongoDB
* API integrations
* Automated content strategy

---

## ⭐ Future Vision

> **Turn raw YouTube data into actionable content opportunities using autonomous AI agents.**
