import typer
import csv
from papers_fetcher.fetch import fetch_papers

app = typer.Typer()

@app.command()
def get(
    query: str = typer.Argument(..., help="PubMed search query"),
    file: str = typer.Option(None, "--file", "-f", help="Output CSV file name"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug info")
):
    """Fetch PubMed papers with pharmaceutical affiliations."""
    papers = fetch_papers(query, debug=debug)

    if file:
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=papers[0].to_dict().keys())
            writer.writeheader()
            for paper in papers:
                writer.writerow(paper.to_dict())
        print(f"✅ Saved {len(papers)} records to {file}")
    else:
        for paper in papers:
            print(paper.to_dict())

if __name__ == "__main__":
    app()
