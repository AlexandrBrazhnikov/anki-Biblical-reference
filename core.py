from sqlalchemy import Engine, create_engine, select # type: ignore | imported by Anki from vendor_BiblicalReference
from sqlalchemy.orm import Session # type: ignore | imported by Anki from vendor_BiblicalReference

from aqt import mw # type: ignore | imported by Anki from vendor_BiblicalReference
from aqt.editor import Editor # type: ignore | imported by Anki from vendor_BiblicalReference
from aqt.utils import tooltip # type: ignore | imported by Anki from vendor_BiblicalReference

from pydantic import ValidationError # type: ignore | imported by Anki from vendor_BiblicalReference

import os

from typing import Dict, Tuple, Any

from .schema import Schema_Configuration
from .models import Title, Translation, Structure, Verse


def validate_ConfigurationFile(config: Dict[str, Any] | None, editor: Editor) -> Schema_Configuration | None:
    if config is None:
        tooltip(
            '❌ ERROR: Biblical Reference - Configuration file do not exists. Create it manualy, reinstal add-on or Restore Defaults',
            period=3000, parent=editor.parentWindow
        )
        return
    try:
        config_obj: Schema_Configuration = Schema_Configuration(**config)
    except ValidationError:
        tooltip(
            '❌ ERROR: Biblical Reference - Configuration file has invalid structure. Adjust it manualy or Restore Defaults',
            period=3000, parent=editor.parentWindow
        )
        return
    return config_obj


def create_EngineDB(editor: Editor, db_name: str = 'BiblicalReference.db') -> Engine | None:
    addon_dir: str = os.path.abspath(__file__)
    addon_dir = os.path.dirname(addon_dir)

    db_path: str = os.path.join(addon_dir, db_name)
    if not os.path.exists(db_path):
        tooltip(
            f'❌ ERROR: Biblical Reference - Can not find database file at {db_path}. Reinstal the add-on',
            period=3000, parent=editor.parentWindow
        )
        return

    engine: Engine = create_engine(f'sqlite:///{db_path}?mode=ro', connect_args={'uri': True})
    return engine


def fetch_Database(
        session: Session,
        translation_code: str,
        title_text: str,
        chapter_no: int,
        verse_no: int
) -> str | None:
    query = (
        select(Verse.verse_text)
            .join(Translation, Verse.id_translation == Translation.id)
            .join(Structure, Verse.id_structure == Structure.id)
            .join(Title, Structure.id_book == Title.id_book)
            .where(
                Translation.code == translation_code,
                Title.title_text == title_text,
                Structure.chapter_no == chapter_no,
                Structure.verse_no == verse_no
            )
    )
    response = session.execute(query)
    verse: str | None = response.scalar()
    return verse


def main(editor: Editor):
    config = mw.addonManager.getConfig(__name__)
    note = editor.note
    card_data = dict(note.items())

    config_obj: Schema_Configuration = validate_ConfigurationFile(config, editor)
    if config_obj is None:
        return
    
    if not set(config_obj.output_fields) & set(card_data.keys()):
        tooltip(
            'Biblical Reference: Output field was not found. Set it in addon configuration file',
            period=3000, parent=editor.parentWindow
        )
        return

    query_data: Tuple[str, int, int] | None = config_obj.extract_RegExp(editor)
    if query_data is None:
        return
    book, chapter_no, verse_no = query_data

    if config_obj.book_aliases and book in config_obj.book_aliases:
        book = config_obj.book_aliases.get(book)

    engine: Engine | None = create_EngineDB(editor)
    if engine is None:
        return
    
    with Session(engine) as session:
        for field in note.model()['flds']:
            
            if not config.get('01_rewrite_fields') and card_data[field['name']]:
                continue

            if field['name'] in config_obj.output_fields:
                translation_code: str = config_obj.output_fields.get(field['name']) # type: ignore | Can't be None - line 107
                verse: str | None = fetch_Database(session, translation_code, book, chapter_no, verse_no) # type: ignore | 'book' can't be None - schema.py, line 101
                if verse is None:
                    tooltip(
                        f'Biblical Reference: Verse for {book} - {translation_code}, {chapter_no}:{verse_no} was not found in database',
                        period=3000, parent=editor.parentWindow
                    )
                    return
                
                note[field['name']] = verse
    
    editor.set_note(editor.note)
    # editor.loadNoteKeepingFocus()
    return


def add_button_BiblicalReference(buttons, editor):
    btn = editor.addButton(
        icon=None,
        cmd='Biblical Reference', 
        func=main,
        tip='Загрузить Стихи из базы данных (Ctrl+Shift+B)',
        keys='Ctrl+Shift+B'
    )
    buttons.append(btn)
    return buttons