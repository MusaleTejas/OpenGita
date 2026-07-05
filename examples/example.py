# ruff: noqa: E402
import sys
import io

# Force stdout and stderr to use UTF-8 encoding on Windows to prevent UnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from rich.console import Console
from rich.panel import Panel
from opengita import Gita

# Initialize Rich console with UTF-8 force
console = Console(force_terminal=True, color_system="truecolor")
gita = Gita()

def run_example():
    console.print("[bold green]Initializing OpenGita SDK...[/bold green]\n")

    # 1. Retrieve and display a specific Chapter
    console.print("[bold yellow]1. Fetching Chapter 2...[/bold yellow]")
    ch2 = gita.chapter(2)
    ch_info = (
        f"[bold]Sanskrit Title:[/bold] {ch2.name}\n"
        f"[bold]Translation:[/bold] {ch2.translation} ({ch2.transliteration})\n"
        f"[bold]Meaning:[/bold] {ch2.meaning.get('en', 'N/A')}\n"
        f"[bold]Verses Count:[/bold] {ch2.verses_count}\n\n"
        f"[bold]Summary (English):[/bold] {ch2.summary.get('en', 'N/A')}"
    )
    console.print(Panel(ch_info, title=f"Chapter {ch2.number}", border_style="green"))
    console.print("\n" + "-"*50 + "\n")

    # 2. Retrieve and display a specific Verse
    console.print("[bold yellow]2. Fetching Verse 2.47 (Karma Yoga)...[/bold yellow]")
    v = gita.verse(2, 47)
    
    # Extract translation
    en_translation = next((t.description for t in v.translations if t.language == "en"), "N/A")
    # Extract commentary
    siva_commentary = next((c.description for c in v.commentaries if c.author == "Swami Sivananda" and c.language == "en"), "N/A")
    
    verse_info = (
        f"[bold]Original Sanskrit (Slok):[/bold]\n{v.slok}\n\n"
        f"[bold]Transliteration:[/bold]\n{v.transliteration}\n\n"
        f"[bold]English Translation (General):[/bold]\n{en_translation}\n\n"
        f"[bold]Sivananda Commentary Sample:[/bold]\n{siva_commentary[:300]}..."
    )
    console.print(Panel(verse_info, title=v.id, border_style="cyan"))
    console.print("\n" + "-"*50 + "\n")

    # 3. Retrieve a Random Verse
    console.print("[bold yellow]3. Fetching Random Verse...[/bold yellow]")
    r = gita.random()
    r_translation = next((t.description for t in r.translations if t.language == "en"), "N/A")
    random_info = (
        f"[bold]ID:[/bold] {r.id}\n\n"
        f"[bold]Slok:[/bold]\n{r.slok}\n\n"
        f"[bold]English Translation:[/bold]\n{r_translation}"
    )
    console.print(Panel(random_info, title="Random Verse of the Day", border_style="magenta"))
    console.print("\n" + "-"*50 + "\n")

    # 4. Dataset Statistics
    console.print("[bold yellow]4. Fetching SDK statistics...[/bold yellow]")
    stats = gita.statistics()
    stats_info = (
        f"[bold]Total Chapters:[/bold] {stats.total_chapters}\n"
        f"[bold]Total Canonical Verses:[/bold] {stats.total_verses}\n"
        f"[bold]Total Files (including colophons):[/bold] {stats.total_files}\n"
        f"[bold]Supported Languages:[/bold] {', '.join(stats.languages)}\n"
        f"[bold]Distinct Translators:[/bold] {stats.translators_count}\n"
        f"[bold]Distinct Commentators:[/bold] {stats.commentators_count}"
    )
    console.print(Panel(stats_info, title="OpenGita Dataset Statistics", border_style="yellow"))

if __name__ == "__main__":
    run_example()
