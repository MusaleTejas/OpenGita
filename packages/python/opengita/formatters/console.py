import re
import hashlib

def _get_mode() -> str:
    try:
        import opengita
        return opengita.get_display_mode()
    except (ImportError, AttributeError):
        return "minimal"

class ConsoleFormatter:
    HINTS = [
        "Use verse.commentary() for detailed explanations.",
        "Use verse.to_json() to export the verse as formatted JSON.",
        "Use opengita.search(\"keyword\") to search the entire Gita.",
        "Use opengita.today() to get today's deterministic daily verse.",
        "Use verse.to_markdown() or verse.to_html() for formatted output."
    ]

    @staticmethod
    def get_hint(ref_id: str) -> str:
        idx = int(hashlib.md5(ref_id.encode('utf-8')).hexdigest(), 16) % len(ConsoleFormatter.HINTS)
        return ConsoleFormatter.HINTS[idx]

    @staticmethod
    def _clean_translation(text: str) -> str:
        # Remove duplicate verse numbers like "2.47 ", "18.76 ", "1.1 " at the beginning of the text
        return re.sub(r'^\d+\.\d+\s+', '', text).strip()

    @staticmethod
    def _get_translator_name(verse, language: str) -> str:
        matches = [t for t in verse.translations if t.language.lower() == language.lower()]
        if not matches:
            return "Unknown"
        preferred = {
            "en": ["Swami Sivananda", "A.C. Bhaktivedanta Swami Prabhupada"],
            "hi": ["Swami Ramsukhdas", "Swami Tejomayananda", "Sri Shankaracharya"]
        }
        pref_list = preferred.get(language.lower(), [])
        for p in pref_list:
            for m in matches:
                if p.lower() in m.author.lower():
                    return m.author
        return matches[0].author

    @staticmethod
    def _get_commentator_name(verse, language: str) -> str:
        c_matches = [c for c in verse.commentaries if c.language.lower() == language.lower()]
        if not c_matches:
            return "Unknown"
        preferred_comm = {
            "en": ["Swami Sivananda", "A.C. Bhaktivedanta Swami Prabhupada"],
            "hi": ["Swami Ramsukhdas", "Swami Chinmayananda"],
            "sa": ["Sri Shankaracharya", "Sri Ramanuja"]
        }
        pref_c_list = preferred_comm.get(language.lower(), [])
        for p in pref_c_list:
            for m in c_matches:
                if p.lower() in m.author.lower():
                    return m.author
        return c_matches[0].author

    @staticmethod
    def render_verse(verse, language="en", commentary=False, transliteration=True) -> str:
        mode = _get_mode()
        if mode == "rich":
            try:
                from importlib.util import find_spec
                if find_spec("rich") is None:
                    raise ImportError
                return ConsoleFormatter._render_rich_verse(verse, language, commentary, transliteration)
            except ImportError:
                mode = "minimal"
                
        if mode == "minimal":
            return ConsoleFormatter._render_minimal_verse(verse, language, commentary, transliteration)
        else:
            return ConsoleFormatter._render_plain_verse(verse, language, commentary, transliteration)

    @staticmethod
    def _render_plain_verse(verse, language, commentary, transliteration) -> str:
        lines = []
        lines.append(verse.reference())
        lines.append("------------------------------------")
        
        lines.append("Sanskrit:")
        lines.append(verse.slok)
        lines.append("")
        
        if transliteration and verse.transliteration:
            lines.append("Transliteration:")
            lines.append(verse.transliteration)
            lines.append("")
            
        trans = verse.translation(language)
        if trans:
            translator = ConsoleFormatter._get_translator_name(verse, language)
            cleaned_trans = ConsoleFormatter._clean_translation(trans)
            lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
            lines.append(f"{lang_label} Translation (Translator: {translator}):")
            lines.append(cleaned_trans)
            lines.append("")
            
        if commentary:
            comm = verse.commentary(language)
            if comm:
                commentator = ConsoleFormatter._get_commentator_name(verse, language)
                cleaned_comm = ConsoleFormatter._clean_translation(comm)
                lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
                lines.append(f"{lang_label} Commentary (Commentator: {commentator}):")
                lines.append(cleaned_comm)
                lines.append("")
                
        lines.append("------------------------------------")
        lines.append(f"Tip: {ConsoleFormatter.get_hint(verse.id)}")
        return "\n".join(lines)

    @staticmethod
    def _render_minimal_verse(verse, language, commentary, transliteration) -> str:
        lines = []
        lines.append(f"📖 {verse.reference()}")
        lines.append("────────────────────────────────────")
        
        lines.append("🕉 Sanskrit:")
        lines.append(verse.slok)
        lines.append("")
        
        if transliteration and verse.transliteration:
            lines.append("🔤 Transliteration:")
            lines.append(verse.transliteration)
            lines.append("")
            
        trans = verse.translation(language)
        if trans:
            translator = ConsoleFormatter._get_translator_name(verse, language)
            cleaned_trans = ConsoleFormatter._clean_translation(trans)
            lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
            lines.append(f"🌍 {lang_label} Translation (Translator: {translator}):")
            lines.append(cleaned_trans)
            lines.append("")
            
        if commentary:
            comm = verse.commentary(language)
            if comm:
                commentator = ConsoleFormatter._get_commentator_name(verse, language)
                cleaned_comm = ConsoleFormatter._clean_translation(comm)
                lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
                lines.append(f"💬 {lang_label} Commentary (Commentator: {commentator}):")
                lines.append(cleaned_comm)
                lines.append("")
                
        lines.append("────────────────────────────────────")
        lines.append(f"💡 Tip: {ConsoleFormatter.get_hint(verse.id)}")
        return "\n".join(lines)

    @staticmethod
    def _render_rich_verse(verse, language, commentary, transliteration) -> str:
        from rich.console import Console
        from rich.text import Text
        from rich.rule import Rule
        
        console = Console(force_terminal=True, color_system="truecolor")
        with console.capture() as capture:
            console.print(Rule(Text(f"📖 {verse.reference()}", style="bold cyan"), style="cyan"))
            
            console.print(Text("🕉 Sanskrit:", style="bold yellow"))
            console.print(verse.slok, style="italic green")
            console.print("")
            
            if transliteration and verse.transliteration:
                console.print(Text("🔤 Transliteration:", style="bold magenta"))
                console.print(verse.transliteration, style="dim white")
                console.print("")
                
            trans = verse.translation(language)
            if trans:
                translator = ConsoleFormatter._get_translator_name(verse, language)
                cleaned_trans = ConsoleFormatter._clean_translation(trans)
                lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
                console.print(Text(f"🌍 {lang_label} Translation (Translator: {translator}):", style="bold green"))
                console.print(cleaned_trans, style="white")
                console.print("")
                
            if commentary:
                comm = verse.commentary(language)
                if comm:
                    commentator = ConsoleFormatter._get_commentator_name(verse, language)
                    cleaned_comm = ConsoleFormatter._clean_translation(comm)
                    lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
                    console.print(Text(f"💬 {lang_label} Commentary (Commentator: {commentator}):", style="bold blue"))
                    console.print(cleaned_comm, style="white")
                    console.print("")
                    
            console.print(Rule(style="cyan"))
            console.print(Text(f"💡 Tip: {ConsoleFormatter.get_hint(verse.id)}", style="dim blue"))
            
        return capture.get()

    @staticmethod
    def render_chapter(chapter, language="en") -> str:
        mode = _get_mode()
        if mode == "rich":
            try:
                from importlib.util import find_spec
                if find_spec("rich") is None:
                    raise ImportError
                return ConsoleFormatter._render_rich_chapter(chapter, language)
            except ImportError:
                mode = "minimal"
                
        if mode == "minimal":
            return ConsoleFormatter._render_minimal_chapter(chapter, language)
        else:
            return ConsoleFormatter._render_plain_chapter(chapter, language)

    @staticmethod
    def _render_plain_chapter(chapter, language) -> str:
        import re
        lines = []
        lines.append(f"Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})")
        lines.append("------------------------------------")
        lines.append(f"Sanskrit Title: {chapter.name}")
        
        meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
        if meaning:
            lines.append(f"Meaning: {meaning}")
            
        lines.append(f"Total Verses: {chapter.verses_count}")
        lines.append("")
        
        summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
        if summary:
            lines.append("Summary:")
            sentences = re.split(r'\s+(?=\d+\.\s)', summary)
            for s in sentences:
                s_clean = s.strip()
                if s_clean:
                    bullet_item = re.sub(r'^\d+\.\s+', '• ', s_clean)
                    lines.append(f"  {bullet_item}")
            lines.append("")
            
        lines.append("------------------------------------")
        lines.append(f"Tip: {ConsoleFormatter.get_hint(f'CH{chapter.number}')}")
        return "\n".join(lines)

    @staticmethod
    def _render_minimal_chapter(chapter, language) -> str:
        import re
        lines = []
        lines.append(f"📖 Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})")
        lines.append("────────────────────────────────────")
        lines.append(f"🕉 Sanskrit Title: {chapter.name}")
        
        meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
        if meaning:
            lines.append(f"🌍 Meaning: {meaning}")
            
        lines.append(f"Total Verses: {chapter.verses_count}")
        lines.append("")
        
        summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
        if summary:
            lines.append("Summary:")
            sentences = re.split(r'\s+(?=\d+\.\s)', summary)
            for s in sentences:
                s_clean = s.strip()
                if s_clean:
                    bullet_item = re.sub(r'^\d+\.\s+', '• ', s_clean)
                    lines.append(f"  {bullet_item}")
            lines.append("")
            
        lines.append("────────────────────────────────────")
        lines.append(f"💡 Tip: {ConsoleFormatter.get_hint(f'CH{chapter.number}')}")
        return "\n".join(lines)

    @staticmethod
    def _render_rich_chapter(chapter, language) -> str:
        from rich.console import Console
        from rich.text import Text
        from rich.rule import Rule
        import re
        
        console = Console(force_terminal=True, color_system="truecolor")
        with console.capture() as capture:
            console.print(Rule(Text(f"📖 Chapter {chapter.number}: {chapter.translation}", style="bold cyan"), style="cyan"))
            
            console.print(Text("🕉 Sanskrit Title:", style="bold yellow"), end=" ")
            console.print(chapter.name, style="italic green")
            
            meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
            if meaning:
                console.print(Text("🌍 Meaning:", style="bold cyan"), end=" ")
                console.print(meaning, style="white")
                
            console.print(Text("Total Verses:", style="bold magenta"), end=" ")
            console.print(str(chapter.verses_count), style="white")
            console.print("")
            
            summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
            if summary:
                console.print(Text("Summary:", style="bold green"))
                sentences = re.split(r'\s+(?=\d+\.\s)', summary)
                for s in sentences:
                    s_clean = s.strip()
                    if s_clean:
                        bullet_item = re.sub(r'^\d+\.\s+', '• ', s_clean)
                        console.print(Text(f"  {bullet_item}", style="white"))
                console.print("")
                
            console.print(Rule(style="cyan"))
            console.print(Text(f"💡 Tip: {ConsoleFormatter.get_hint(f'CH{chapter.number}')}", style="dim blue"))
            
        return capture.get()

    @staticmethod
    def render_search(results, keyword: str) -> str:
        mode = _get_mode()
        if mode == "rich":
            try:
                from importlib.util import find_spec
                if find_spec("rich") is None:
                    raise ImportError
                return ConsoleFormatter._render_rich_search(results, keyword)
            except ImportError:
                mode = "minimal"
                
        if mode == "minimal":
            return ConsoleFormatter._render_minimal_search(results, keyword)
        else:
            return ConsoleFormatter._render_plain_search(results, keyword)

    @staticmethod
    def _render_plain_search(results, keyword: str) -> str:
        lines = []
        lines.append(f"Search Results for '{keyword}'")
        lines.append(f"Found: {len(results)} verses")
        lines.append("------------------------------------")
        
        preview_limit = 10
        for idx, v in enumerate(results[:preview_limit], 1):
            lines.append(f"{idx}. {v.reference()}")
            slok_snippet = v.slok[:60] + "..."
            trans_snippet = ConsoleFormatter._clean_translation(v.translation())[:100] + "..."
            lines.append(f"   {slok_snippet}")
            lines.append(f"   {trans_snippet}")
            lines.append("")
            
        if len(results) > preview_limit:
            lines.append(f"... and {len(results) - preview_limit} more matches.")
            lines.append("")
            
        lines.append("------------------------------------")
        lines.append(f"Tip: {ConsoleFormatter.get_hint(keyword)}")
        return "\n".join(lines).strip()

    @staticmethod
    def _render_minimal_search(results, keyword: str) -> str:
        lines = []
        lines.append(f"🔍 Search Results for '{keyword}'")
        lines.append(f"Found: {len(results)} verses")
        lines.append("────────────────────────────────────")
        
        preview_limit = 10
        for idx, v in enumerate(results[:preview_limit], 1):
            lines.append(f"{idx}. {v.reference()}")
            slok_snippet = v.slok[:60] + "..."
            trans_snippet = ConsoleFormatter._clean_translation(v.translation())[:100] + "..."
            lines.append(f"   {slok_snippet}")
            lines.append(f"   {trans_snippet}")
            lines.append("")
            
        if len(results) > preview_limit:
            lines.append(f"... and {len(results) - preview_limit} more matches.")
            lines.append("")
            
        lines.append("────────────────────────────────────")
        lines.append(f"💡 Tip: {ConsoleFormatter.get_hint(keyword)}")
        return "\n".join(lines).strip()

    @staticmethod
    def _render_rich_search(results, keyword: str) -> str:
        from rich.console import Console
        from rich.text import Text
        from rich.rule import Rule
        
        console = Console(force_terminal=True, color_system="truecolor")
        with console.capture() as capture:
            console.print(Rule(Text(f"🔍 Search results for '{keyword}'", style="bold cyan"), style="cyan"))
            console.print(Text(f"Found {len(results)} verses", style="bold green"))
            console.print("")
            
            preview_limit = 10
            for idx, v in enumerate(results[:preview_limit], 1):
                console.print(Text(f"{idx}. {v.reference()}", style="bold yellow"))
                
                slok_snippet = v.slok[:60] + "..."
                trans_snippet = ConsoleFormatter._clean_translation(v.translation())[:100] + "..."
                
                def highlight_text(text, kw):
                    t = Text(text, style="dim white")
                    t.highlight_regex(re.escape(kw), "bold reverse yellow", case_sensitive=False)
                    return t
                    
                console.print(highlight_text(f"   {slok_snippet}", keyword))
                console.print(highlight_text(f"   {trans_snippet}", keyword))
                console.print("")
                
            if len(results) > preview_limit:
                console.print(Text(f"... and {len(results) - preview_limit} more matches.", style="italic dim white"))
                console.print("")
                
            console.print(Rule(style="cyan"))
            console.print(Text(f"💡 Tip: {ConsoleFormatter.get_hint(keyword)}", style="dim blue"))
            
        return capture.get()

    @staticmethod
    def render_rich_verse(verse):
        try:
            from importlib.util import find_spec
            if find_spec("rich") is None:
                raise ImportError
            return ConsoleFormatter._render_rich_verse(verse, "en", False, True)
        except ImportError:
            return ConsoleFormatter._render_minimal_verse(verse, "en", False, True)

    @staticmethod
    def render_rich_chapter(chapter):
        try:
            from importlib.util import find_spec
            if find_spec("rich") is None:
                raise ImportError
            return ConsoleFormatter._render_rich_chapter(chapter, "en")
        except ImportError:
            return ConsoleFormatter._render_minimal_chapter(chapter, "en")
