# Ops Anomaly Agent

A local AI-powered CLI tool that detects and explains anomalies in any CSV file.
Runs 100% offline using Ollama — no API keys, no cloud, no cost.

## What it does
- Loads any CSV file and auto-detects numeric columns
- Detects anomalies using z-score and % change analysis
- Ranks anomalies by severity score
- Uses a local AI model to generate hypotheses and investigation steps

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- `llama3.1` model pulled

## Installation

```bash
git clone <your-repo>
cd ops-anomaly-agent
python3 -m venv venv
source venv/bin/activate
pip install -e .
ollama pull llama3.1
```

## Usage

```bash
# Full analysis with AI insights
anomaly-agent data/yourfile.csv

# Detection only, no AI
anomaly-agent data/yourfile.csv --no-ai

# Adjust sensitivity (lower = catches more anomalies)
anomaly-agent data/yourfile.csv --sensitivity 1.5

# Only analyze top 3 anomalies
anomaly-agent data/yourfile.csv --top 3

# Export report
anomaly-agent data/yourfile.csv --export markdown
anomaly-agent data/yourfile.csv --export json
```

## Project Structure
ops-anomaly-agent/

├── main.py        # CLI entry point

├── detector.py    # Anomaly detection engine

├── agent.py       # AI reasoning agent

├── report.py      # Terminal output formatting

├── setup.py       # Package installation

└── data/          # Drop your CSV files here


## How it works
1. Loads your CSV and identifies numeric columns
2. Runs z-score and % change detection to find outliers
3. Scores each anomaly by severity
4. Sends each anomaly with surrounding context to a local LLM
5. Displays ranked anomalies with AI-generated hypotheses and next steps