# LungData

A Streamlit dashboard and AI assistant for exploring a synthetic lung cancer dataset as part of a Big Data project.

This project presents the raw dataset, highlights common data-quality issues, shows the cleaned data, and provides a chatbot that answers questions using project-defined facts about the dataset.

## Overview

LungData is a university-style data project built around a synthetic lung cancer dataset with:

- 10,024,574 rows
- 14 columns
- 21.6% positive diagnoses in the raw dataset
- significant data-cleaning challenges such as missing values, inconsistent labels, invalid ages, and messy dates

The project is designed to demonstrate:

- large-scale data inspection
- preprocessing and cleanup workflows
- exploratory data analysis
- dashboard storytelling
- AI-assisted Q&A using a lightweight knowledge base

> Important: the dataset is synthetic and intended for educational use, not for clinical or medical decision-making.

## Features

- Home dashboard summarizing project goals and key findings
- Messy Data page showing data defects and quality problems in the raw dataset
- Cleaned Data page showing cleaned outputs and processed summaries
- AI Bot page for answering questions about the dataset using project knowledge
- Streamlit-based navigation and custom dark theme
- Power BI embedding support for live or image-based dashboard views

## Tech Stack

- Python
- Streamlit
- Pandas
- OpenAI-compatible LLM client
- Python-dotenv
- Power BI dashboard embeds
- Parquet-oriented data workflow

## Repository Structure

```text
LungData/
├── app.py                  # Streamlit entry point
├── knowledge.py           # Knowledge base and local bot logic
├── utils.py               # Shared config, styling, dashboard utilities
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore
├── .gitattributes
├── .streamlit/
│   └── config.toml       # Streamlit theme configuration
├── assets/                # Dashboard screenshots / image assets
├── views/
│   ├── home.py            # Landing page
│   ├── messy.py           # Raw dataset quality analysis
│   ├── clean.py           # Cleaned data dashboard
│   └── bot.py             # AI assistant interface
├── README.md
└── ...
```

## Dataset Notes

The dataset is synthetic and generated from published reference distributions. It is meant for educational practice in big-data cleaning and analytics, not for real patient analysis or medical advice.

The raw dataset contains multiple issues that are intentionally part of the project, including:

- blank and missing values
- inconsistent gender labels
- multiple smoking-status spellings
- age values written as words or containing impossible values
- junk dates and mixed date formats
- all columns initially stored as text because of the messy input values

## Environment Setup

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Then update `.env` with your API settings, for example:

```dotenv
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=your-api-key
LLM_MODEL=openai/gpt-oss-120b
```

## Run the App

```bash
streamlit run app.py
```

The app will launch in your default browser, where you can navigate between the dashboard pages and the AI Bot.

## Project Goals

This repository demonstrates how to:

- clean and validate a very large synthetic dataset
- explain common defects in raw data
- present findings visually through dashboards
- add a lightweight AI bot with a constrained knowledge base
- communicate technical analysis in a clear user-facing Streamlit app

## License

This project does not currently specify a license file. Please check with the repository owner before using it in a production or public-facing context.

## Team

This project was developed as a group effort for the Introduction to Big Data course:

- RA — Ralph Zedrick Abayon
- LE — Lance Evangelista
- HO — Hansel Nino Ofilan
- DO — Dardy Jr. Onia
- MS — Marc Deanielle Santiago

## Links

- GitHub repository: https://github.com/DJO05555/LungData

