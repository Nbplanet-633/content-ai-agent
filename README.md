# AI Content Trend Agent

An AI-powered content research agent that discovers YouTube trends for a given niche and generates actionable content ideas.

## Features

- YouTube trend research
- Trend scoring based on:
  - Views per day
  - Engagement rate
  - Recency
- AI-powered trend analysis using CrewAI
- Content idea generation
- Duplicate detection
- Google Sheets integration
- CLI-based niche input
- Invalid input handling

## Architecture

User
↓
CLI
↓
CrewAI
↓
Content Trend Researcher
↓
YouTube API
↓
Trend Scoring
↓
Content Strategy Analyst
↓
Google Sheets

## Tech Stack

- Python
- CrewAI
- Groq
- Llama 3.3 70B
- YouTube Data API
- Google Sheets API
- Pydantic
- Google OAuth

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd content-trend-agent