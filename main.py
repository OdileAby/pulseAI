import click
from rich.console import Console
from detector import load_csv, get_numeric_columns, detect_anomalies, get_most_critical
from report import print_summary, print_report, print_ai_report
from agent import run_agent

console = Console()

@click.command()
@click.argument('filepath')
@click.option('--sensitivity', default=2.5, help='Z-score threshold (lower = more sensitive). Default: 2.5')
@click.option('--export', type=click.Choice(['json', 'markdown']), help='Export report to file')
@click.option('--no-ai', is_flag=True, help='Skip AI analysis and show detection only')
@click.option('--top', default=0, help='Only analyze top N anomalies by severity')
def analyze(filepath, sensitivity, export, no_ai, top):
    """Ops Anomaly Agent — detects and explains anomalies in any CSV file."""

    console.print("\n[bold cyan]Ops Anomaly Agent[/bold cyan]")
    console.print(f"[dim]Loading file: {filepath}[/dim]\n")

    # Load CSV
    df = load_csv(filepath)
    console.print(f"[green]Loaded[/green] {len(df)} rows x {len(df.columns)} columns")

    # Detect numeric columns
    columns = get_numeric_columns(df)
    if not columns:
        console.print("[red]No numeric columns found to analyze.[/red]")
        return
    console.print(f"[green]Analyzing columns:[/green] {', '.join(columns)}\n")

    # Detect anomalies
    anomalies = detect_anomalies(df, columns, z_threshold=sensitivity)

    if not anomalies:
        console.print("[bold green]No anomalies detected![/bold green]")
        return

    # Show most critical first
    most_critical = get_most_critical(anomalies)
    print_summary(anomalies, most_critical)

    # Limit to top N if requested
    if top > 0:
        anomalies = anomalies[:top]
        console.print(f"\n[dim]Showing top {top} anomalies by severity[/dim]")

    # Print detection report
    print_report(anomalies, df)

    # Skip AI if --no-ai flag is passed
    if no_ai:
        return

    # Run AI agent
    results = run_agent(anomalies, df)

    # Print AI report
    print_ai_report(results, export)

if __name__ == '__main__':
    analyze()