import uuid
import time
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich import box

from agent.tools import client
from agent.agent import agent

console = Console()

BANNER = r"""[bold magenta]
 __        __   _    _____                   _             _
 \ \      / /__| |__|_   _|__ _ __ _ __ ___ | | ___   _ _ __ | |_
  \ \ /\ / / _ \ '_ \| |/ _ \| '__| '_ ` _ \| |/ / | | | '_ \| __|
   \ V  V /  __/ |_) || |  __/ |  | | | | | |   <| |_| | |_) | |_
    \_/\_/ \___|_.__/ |_|\___|_|  |_| |_| |_|_|\_\\__,_| .__/ \__|
                                                        |_|
[/bold magenta][dim]                    v1.0 - Powered by Gemini + Wikipedia MCP[/dim]"""

STATUS_ICONS = {
    "ready": "[bold green]+[/bold green]",
    "thinking": "[bold yellow]*[/bold yellow]",
    "error": "[bold red]![/bold red]",
    "idle": "[dim]-[/dim]",
}


def render_header():
    console.print(BANNER)
    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column(style="bold")
    info.add_column()
    info.add_row("Model", "[cyan]gemini-2.5-flash[/cyan]")
    info.add_row("Tools", "[magenta]search, summary, article[/magenta]")
    info.add_row("Memory", "[green]MemorySaver[/green]")
    info.add_row("MCP", "[yellow]wikipedia-mcp (persistent)[/yellow]")
    console.print(Panel(info, title="[bold]System Info[/bold]", border_style="blue"))
    console.print()


def render_response(messages):
    ai_msg = messages[-1]

    content = ai_msg.content
    if isinstance(content, list):
        content = "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )

    console.print(
        Panel(
            Markdown(content),
            title="[bold green]WikiResearch AI[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )
    console.print()


def render_footer():
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column(style="dim")
    table.add_column()
    table.add_row("Commands:", "[bold]exit[/bold] quit  |  [bold]Ctrl+C[/bold] cancel  |  [bold]clear[/bold] reset")
    console.print(table)


def main():
    console.clear()
    render_header()

    client.start()
    console.print(f"  {STATUS_ICONS['ready']} MCP server connected\n")

    render_footer()
    console.print()

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    turn = 0

    try:
        while True:
            turn += 1
            try:
                question = console.input(
                    "  [bold blue]--[ You ]--[/bold blue]\n  [bold cyan]>[/bold cyan] "
                )
            except (EOFError, KeyboardInterrupt):
                break

            if question.strip().lower() in ("exit", "quit"):
                break
            if question.strip().lower() == "clear":
                console.clear()
                render_header()
                render_footer()
                continue
            if not question.strip():
                continue

            console.print()
            console.print(f"  {STATUS_ICONS['thinking']} [yellow]Thinking...[/yellow]")

            start = time.time()

            try:
                result = agent.invoke(
                    {"messages": [{"role": "user", "content": question}]},
                    config,
                )
                elapsed = time.time() - start

                messages = result["messages"]

                render_response(messages)

                status = Table(box=None, show_header=False, padding=(0, 1))
                status.add_column(style="dim")
                status.add_column()
                status.add_row(
                    f"  {STATUS_ICONS['idle']}",
                    f"[dim]Turn {turn} | {elapsed:.1f}s | {len(messages)} messages in context[/dim]"
                )
                console.print(status)
                console.print()

            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]{type(e).__name__}:[/bold red] {e}",
                        title="[red]Error[/red]",
                        border_style="red",
                    )
                )
                console.print()
    finally:
        client.stop()
        console.print()
        console.print(
            Panel(
                "[dim]Session ended. Goodbye.[/dim]",
                border_style="dim",
            )
        )


if __name__ == "__main__":
    main()
