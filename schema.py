from __future__ import annotations

from pydantic import BaseModel, Field # type: ignore | imported by Anki from vendor_BiblicalReference
from typing import Dict, Tuple, Literal, Optional

from aqt.editor import Editor # type: ignore | imported by Anki from vendor_BiblicalReference
from aqt.utils import tooltip # type: ignore | imported by Anki from vendor_BiblicalReference

import re
from re import Pattern, Match


class Schema_Configuration(BaseModel):
    book: Tuple[str, str, Literal['header', 'body']] = Field(alias='00_book')
    chapter: Tuple[str, str, Literal['header', 'body']] = Field(alias='00_chapter')
    verse: Tuple[str, str, Literal['header', 'body']] = Field(alias='00_verse')
    rewrite_fields: bool = Field(alias='01_rewrite_fields')
    output_fields: Dict[str, str] = Field(alias='02_output_fields')
    book_aliases: Optional[Dict[str, str]] = Field(alias='03_book_aliases', default=None)

    @staticmethod
    def _extract_RegExp(
        field_spec: Tuple[str, str, Literal['header', 'body']],
        card_data: dict, editor: Editor
    ) -> str | None:

        field_name, pattern_str, search = field_spec

        if not field_name in card_data:
            tooltip (
                f'Biblical Reference: Can not extract data from {field_name} field. Field is does not exist.',
                period=3000, parent=editor.parentWindow
            )
            return
        
        if search == 'header':
            field_text: str | None = field_name
        elif search == 'body':
            field_text: str | None = card_data.get(field_name)
        else:
            tooltip (
                f'Biblical Reference: Can not extract data from {field_name} field. Adjust field search parameter in config or Restore Defaults',
                period=3000, parent=editor.parentWindow
            )
            return
        
        if field_text is None:
            tooltip (
                f'Biblical Reference: Can not extract data from {field_name} field. Field is empty.',
                period=3000, parent=editor.parentWindow
            )
            return
        
        try:
            pattern: Pattern = re.compile(pattern_str)
        except re.error:
            tooltip (
                f'❌ ERROR: Biblical Reference - RegExp for {field_name} field is invalid. Adjust RegExp in config or Restore Defaults',
                period=3000, parent=editor.parentWindow
            )
            return
        
        field_text_match: Match[str] | None = re.search(pattern, field_text)
        
        if field_text_match is None:
            tooltip (
                f'Biblical Reference: Can not extract data from {field_name} field. Check spelling or adjust RegExp in config',
                period=3000, parent=editor.parentWindow
            )
            return
        
        try:
            text: str = field_text_match.group(1)
        except IndexError:
            tooltip (
                f'❌ ERROR: Biblical Reference - RegExp for {field_name} field is do not contains group. Adjust RegExp in config or Restore Defaults',
                period=3000, parent=editor.parentWindow
            )
            return
        return text
    
    @staticmethod
    def _isdigit(text_digit: str, editor: Editor) -> bool:
        if text_digit.isdigit():
            return True
        else:
            tooltip (
                f'Biblical Reference: Chapter or Verse are not digits',
                period=3000, parent=editor.parentWindow
            )
            return False


    def extract_RegExp(self, editor: Editor) -> Tuple[str, int, int] | None:
        card_data = dict(editor.note.items())
        
        book: str | None = self._extract_RegExp(self.book, card_data, editor)
        chapter: str | None = self._extract_RegExp(self.chapter, card_data, editor)
        verse: str | None = self._extract_RegExp(self.verse, card_data, editor)
        
        if book is None or chapter is None or verse is None:
            return
        
        if not self._isdigit(chapter, editor) and not self._isdigit(verse, editor):
            return
        
        chapter_no, verse_no = map(int, (chapter, verse))
        
        return book, chapter_no, verse_no

