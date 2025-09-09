# main.py

import typer
from rich.console import Console
import os
import subprocess

from code_indexer import CodeIndexer

app = typer.Typer()
console = Console()

@app.command()
def index(
    path: str = typer.Argument(..., help="The path to the codebase directory to index."),
):
    """
    Indexes a codebase directory and stores it in the vector database.
    """
    if not os.path.isdir(path):
        console.print(f"[bold red]Error: The path '{path}' is not a valid directory.[/bold red]")
        raise typer.Exit(code=1)
        
    indexer = CodeIndexer()
    indexer.index_directory(path)
    console.print("\n[bold green]✅ Codebase successfully indexed![/bold green]")

@app.command()
def run():
    """
    Runs the Flask web server.
    """
    console.print("[bold green]🚀 Starting the Code Agent web server...[/bold green]")
    console.print("Navigate to [bold blue]http://127.0.0.1:5001[/bold blue] in your browser.")
    
    # We use subprocess to run Flask so we can manage it from Typer
    # This is a simple way to integrate them.
    try:
        subprocess.run(["flask", "run", "--port=5001"], check=True)
    except FileNotFoundError:
        console.print("[bold red]Error: 'flask' command not found. Did you install dependencies and activate the virtual environment?[/bold red]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Web server failed to start. Error: {e}[/bold red]")


if __name__ == "__main__":
    app()


    