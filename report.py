import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

console = Console()


def print_summary(anomalies, most_critical):
    console.print(f"\n[bold red]Most Critical Anomaly[/bold red]")
    body = (
        "Column: " + str(most_critical["column"]) + "\n"
        "Row: " + str(most_critical["row"]) + "\n"
        "Value: " + str(most_critical["value"]) + "\n"
        "Severity Score: " + str(most_critical["severity"]) + "\n"
        "Z-Score: " + str(most_critical["z_score"]) + "\n"
        "% Change: " + str(most_critical["pct_change"]) + "%"
    )
    console.print(Panel(body, title="Needs Immediate Attention", border_style="bold red", padding=(1, 2)))


def print_report(anomalies, df, export=None):
    console.print(f"\n[bold red]Found " + str(len(anomalies)) + " anomaly(s)[/bold red]\n")

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Severity", style="bold red", width=10)
    table.add_column("Row", style="dim", width=6)
    table.add_column("Column", style="cyan")
    table.add_column("Value", style="yellow")
    table.add_column("Z-Score", style="red")
    table.add_column("% Change", style="red")
    table.add_column("Reason", style="white")

    for a in anomalies:
        table.add_row(
            str(a["severity"]),
            str(a["row"]),
            a["column"],
            str(round(a["value"], 4)),
            str(a["z_score"]),
            str(a["pct_change"]) + "%",
            a["reason"]
        )

    console.print(table)


def print_ai_report(results, export=None):
    console.print(f"\n[bold cyan]AI Insights[/bold cyan]\n")

    for i, result in enumerate(results):
        col = result["column"]
        row = result["row"]
        value = result["value"]
        analysis = result.get("analysis", "No analysis available.")

        header = "Anomaly " + str(i+1) + " — " + str(col) + " at row " + str(row) + " — Severity: " + str(result["severity"])
        body = "Value: " + str(value) + "  |  Z-Score: " + str(result["z_score"]) + "  |  Change: " + str(result["pct_change"]) + "%\n\n" + analysis

        console.print(Panel(body, title=header, border_style="red", padding=(1, 2)))
        console.print()

    if export == "json":
        filename = "anomaly_report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        console.print("\nReport exported to " + filename)

    elif export == "markdown":
        filename = "anomaly_report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".md"
        with open(filename, "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write("**Total anomalies:** " + str(len(results)) + "\n\n")
            for i, result in enumerate(results):
                f.write("## Anomaly " + str(i+1) + " — " + result["column"] + " at row " + str(result["row"]) + "\n\n")
                f.write("- **Severity:** " + str(result["severity"]) + "\n")
                f.write("- **Value:** " + str(result["value"]) + "\n")
                f.write("- **Z-Score:** " + str(result["z_score"]) + "\n")
                f.write("- **% Change:** " + str(result["pct_change"]) + "%\n\n")
                f.write(str(result.get("analysis", "")) + "\n\n---\n\n")
        console.print("\nReport exported to " + filename)