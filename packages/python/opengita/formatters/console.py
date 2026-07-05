
class ConsoleFormatter:
    @staticmethod
    def render_verse(verse, language="en", commentary=False, transliteration=True) -> str:
        lines = []
        lines.append("────────────────────────────────────")
        lines.append(f"📖 {verse.reference()}")
        lines.append("")
        lines.append("Sanskrit")
        lines.append(verse.slok)
        lines.append("")
        
        if transliteration and verse.transliteration:
            lines.append("Transliteration")
            lines.append(verse.transliteration)
            lines.append("")
            
        trans = verse.translation(language)
        if trans:
            lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
            lines.append(lang_label)
            lines.append(trans)
            lines.append("")
            
        if commentary:
            comm = verse.commentary(language)
            if comm:
                lang_label = "English Commentary" if language == "en" else ("Hindi Commentary" if language == "hi" else f"{language.capitalize()} Commentary")
                lines.append(lang_label)
                lines.append(comm)
                lines.append("")
                
        if lines[-1] == "":
            lines.pop()
        lines.append("────────────────────────────────────")
        return "\n".join(lines)

    @staticmethod
    def render_chapter(chapter, language="en") -> str:
        lines = []
        lines.append("────────────────────────────────────")
        lines.append(f"📖 Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})")
        lines.append("")
        lines.append("Sanskrit Title")
        lines.append(chapter.name)
        lines.append("")
        
        meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
        if meaning:
            lines.append("Meaning")
            lines.append(meaning)
            lines.append("")
            
        lines.append(f"Total Verses: {chapter.verses_count}")
        lines.append("")
        
        summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
        if summary:
            lines.append("Summary")
            lines.append(summary)
            lines.append("")
            
        if lines[-1] == "":
            lines.pop()
        lines.append("────────────────────────────────────")
        return "\n".join(lines)

    @staticmethod
    def render_rich_verse(verse):
        try:
            from rich.panel import Panel
            from rich.text import Text
            from rich.console import Group
            
            elements = []
            elements.append(Text("Sanskrit", style="bold yellow"))
            elements.append(Text(verse.slok, style="italic green"))
            elements.append(Text(""))
            
            if verse.transliteration:
                elements.append(Text("Transliteration", style="bold cyan"))
                elements.append(Text(verse.transliteration, style="dim"))
                elements.append(Text(""))
                
            trans = verse.translation("en")
            if trans:
                elements.append(Text("English", style="bold magenta"))
                elements.append(Text(trans, style="white"))
                
            return Panel(
                Group(*elements),
                title=f"[bold]📖 {verse.reference()}[/bold]",
                border_style="blue",
                expand=False
            )
        except ImportError:
            return ConsoleFormatter.render_verse(verse)

    @staticmethod
    def render_rich_chapter(chapter):
        try:
            from rich.panel import Panel
            from rich.text import Text
            from rich.console import Group
            
            elements = []
            elements.append(Text("Sanskrit Title", style="bold yellow"))
            elements.append(Text(chapter.name, style="italic green"))
            elements.append(Text(""))
            
            meaning = chapter.meaning.get("en", "")
            if meaning:
                elements.append(Text("Meaning", style="bold cyan"))
                elements.append(Text(meaning, style="white"))
                elements.append(Text(""))
                
            elements.append(Text(f"Total Verses: {chapter.verses_count}", style="bold"))
            elements.append(Text(""))
            
            summary = chapter.summary.get("en", "")
            if summary:
                elements.append(Text("Summary", style="bold magenta"))
                elements.append(Text(summary, style="white"))
                
            return Panel(
                Group(*elements),
                title=f"[bold]📖 Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})[/bold]",
                border_style="green",
                expand=False
            )
        except ImportError:
            return ConsoleFormatter.render_chapter(chapter)
