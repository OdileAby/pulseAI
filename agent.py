import ollama
from rich.console import Console

console = Console()

SYSTEM_PROMPT = """You are an expert business operations analyst. 
You will be given a data anomaly detected in a business CSV dataset.
Your job is to:
1. Suggest 2-3 likely hypotheses for why this anomaly occurred
2. Provide 3 concrete investigation steps an analyst should take

Be specific, practical, and concise. Format your response exactly like this:

HYPOTHESES:
- [hypothesis 1]
- [hypothesis 2]
- [hypothesis 3]

INVESTIGATION STEPS:
- [step 1]
- [step 2]
- [step 3]
"""

def build_prompt(anomaly, df):
    """Build a context-rich prompt for the anomaly."""
    col = anomaly["column"]
    row = anomaly["row"]
    value = anomaly["value"]
    z_score = anomaly["z_score"]
    pct_change = anomaly["pct_change"]

    # Get surrounding rows for context
    start = max(0, row - 3)
    end = min(len(df), row + 3)
    context_rows = df.iloc[start:end].to_string()

    prompt = f"""
I detected an anomaly in a business dataset:

- Column: {col}
- Row: {row}
- Anomalous Value: {value}
- Z-Score: {z_score} (normal is below 2.5)
- % Change from previous row: {pct_change}%

Here is the surrounding data for context:
{context_rows}

Please analyze this anomaly and provide hypotheses and investigation steps.
"""
    return prompt

def analyze_anomaly(anomaly, df, model="llama3.1:latest"):
    """Send anomaly to Ollama and get AI analysis."""
    prompt = build_prompt(anomaly, df)

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]

def run_agent(anomalies, df, model="llama3.1:latest"):
    """Run the AI agent over all anomalies."""
    results = []

    console.print(f"\n[bold cyan]🤖 AI Agent Analysis[/bold cyan] — using {model}\n")

    for i, anomaly in enumerate(anomalies):
        col = anomaly["column"]
        row = anomaly["row"]

        console.print(f"[dim]Analyzing anomaly {i+1}/{len(anomalies)}: {col} at row {row}...[/dim]")

        with console.status(f"[yellow]Thinking...[/yellow]"):
            analysis = analyze_anomaly(anomaly, df, model)

        results.append({
            **anomaly,
            "analysis": analysis
        })

        console.print(f"[green]✅ Done[/green]\n")

    return results