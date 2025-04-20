"""Command Line Interface for the Research System."""
import typer
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress

from graph.agent_graph import ResearchSystem

# Initialize Typer app
app = typer.Typer(help="Dual-Agent AI Research System")
console = Console()


@app.command()
def research(
    query: str = typer.Argument(..., help="The research query to process"),
    save_to_file: Optional[str] = typer.Option(
        None, "--save", "-s", help="Save the answer to the specified file"
    ),
):
    """Process a research query and display the answer."""
    console.print(Panel.fit("🔍 Research Query", title="Input"))
    console.print(query)
    console.print()
    
    system = ResearchSystem()
    
    with Progress() as progress:
        task1 = progress.add_task("[green]Researching...", total=1)
        
        # Process the query
        result = system.process_query(query)
        progress.update(task1, advance=1)
    
    # Check for errors
    if result.get("error"):
        console.print(Panel.fit(f"❌ Error: {result['error']}", title="Error"))
        raise typer.Exit(code=1)
    
    # Display the answer
    answer = result["answer"]
    console.print(Panel.fit("📝 Research Answer", title="Result"))
    console.print(Markdown(answer.answer))
    
    # Display sources
    console.print(Panel.fit("📚 Sources", title="References"))
    for i, source in enumerate(answer.sources):
        console.print(f"[{i+1}] {source['title']}")
        console.print(f"    URL: {source['url']}")
        console.print()
    
    # Save to file if requested
    if save_to_file:
        with open(save_to_file, "w") as f:
            f.write(f"# Research: {query}\n\n")
            f.write(answer.answer)
            f.write("\n\n## Sources\n\n")
            for i, source in enumerate(answer.sources):
                f.write(f"[{i+1}] {source['title']}\n")
                f.write(f"    URL: {source['url']}\n\n")
        console.print(f"Results saved to [bold]{save_to_file}[/bold]")


if __name__ == "__main__":
    app() 