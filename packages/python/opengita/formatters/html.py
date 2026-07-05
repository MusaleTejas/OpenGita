class HTMLFormatter:
    @staticmethod
    def render_verse(verse, language="en", commentary=False, transliteration=True) -> str:
        lines = []
        lines.append('<div class="opengita-verse">')
        lines.append(f'  <h3 class="reference">📖 {verse.reference()}</h3>')
        lines.append(f'  <p class="sanskrit">{verse.slok}</p>')
        if transliteration and verse.transliteration:
            lines.append(f'  <p class="transliteration"><em>{verse.transliteration}</em></p>')
            
        trans = verse.translation(language)
        if trans:
            lang_label = "English" if language == "en" else ("Hindi" if language == "hi" else language.capitalize())
            lines.append('  <div class="translation">')
            lines.append(f'    <strong>{lang_label}:</strong> {trans}')
            lines.append('  </div>')
            
        if commentary:
            comm = verse.commentary(language)
            if comm:
                lang_label = "English Commentary" if language == "en" else ("Hindi Commentary" if language == "hi" else f"{language.capitalize()} Commentary")
                lines.append('  <div class="commentary">')
                lines.append(f'    <strong>{lang_label}:</strong> {comm}')
                lines.append('  </div>')
                
        lines.append('</div>')
        return "\n".join(lines)

    @staticmethod
    def render_chapter(chapter, language="en") -> str:
        lines = []
        lines.append('<div class="opengita-chapter">')
        lines.append(f'  <h2 class="title">📖 Chapter {chapter.number}: {chapter.translation} ({chapter.transliteration})</h2>')
        lines.append(f'  <p class="sanskrit-title"><strong>Sanskrit Title:</strong> {chapter.name}</p>')
        
        meaning = chapter.meaning.get(language) or chapter.meaning.get("en") or ""
        if meaning:
            lines.append(f'  <p class="meaning"><strong>Meaning:</strong> {meaning}</p>')
            
        lines.append(f'  <p class="verses-count"><strong>Total Verses:</strong> {chapter.verses_count}</p>')
        
        summary = chapter.summary.get(language) or chapter.summary.get("en") or ""
        if summary:
            lines.append('  <div class="summary">')
            lines.append(f'    <strong>Summary:</strong> {summary}')
            lines.append('  </div>')
            
        lines.append('</div>')
        return "\n".join(lines)
