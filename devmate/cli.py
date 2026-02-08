import typer
from rich import print
from devmate.logger import get_logger
from devmate.core.agent import Agent




logger= get_logger("cli")

app=typer.Typer(
    add_completion=False,
    
)

# 🔑 THIS IS THE MISSING PIECE
@app.callback()
def main():
    """
    Devmate CLI – AI-powered developer assistant.
    """
    pass

@app.command()
def health():
    """
    health check for devmate cli

    """

    logger.info("Health check for devmate cli invoked")
    print("[green]Devmate CLI is running successfully[/green]")



@app.command()
def run(intent: str):
    """ Run the Devmate agent with a given intent """
    logger.info(f"Running agent with intent: {intent}")

    agent=Agent()

    results=agent.run(intent)

    print("[bold green]Agent execution completed[/bold green]")

    for step in results:
        print(f"[cyan]- Action:[/cyan] {step['action']}")
        print(f" Result: {step['result']}")













