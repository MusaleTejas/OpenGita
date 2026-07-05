class MarkdownFormatter:
    @staticmethod
    def render_verse(verse, language="en", commentary=False, transliteration=True) -> str:
        lines = []
        lines.append(f"### 📖 {verse.reference()}")
        lines.append("")
        lines.append("**Sanskrit**")
        lines.append(f"> {verse.slok}")
        lines.append("")
        if transliteration and verse.transliteration:
            lines.append("**Transliteration**")
            lines.append(f"> {verse.transliteration}")
            lines.append("")
            
        trans = verse.translation(language)
        if trans:
            lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
            lines.append(f"**{lang_label}**")
            lines.append(trans)
            lines.append("")
            
        if commentary:
            comm = verse.commentary(language)
            if comm:
                lang_label = "English Commentary" if language == "en" else ("Hindi Commentary" if language == "hi" else f"{language.capitalize()} Commentary")
                lines.append(f"**{lang_label}**")
                lines.append(comm)
                lines.append("")
                
        return "\n".join(lines).strip()

    @staticmethod
    def render_chapter(chapter, language="en") -> str:
        lines = []
        lines.append(f"## 📖 Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})")
        lines.append("")
        lines.append(f"**Sanskrit Title:** {chapter.name}")
        lines.append("")
        
        meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
        if meaning:
            lines.append(f"**Meaning:** {meaning}")
            lines.append("")
            
        lines.append(f"**Total Verses:** {chapter.verses_count}")
        lines.append("")
        
        summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
        if summary:
            lines.append("**Summary**")
            lines.append(summary)
            lines.append("")
            
        return "\n".join(lines).strip()
