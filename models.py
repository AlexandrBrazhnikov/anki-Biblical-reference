from typing import Optional

from sqlalchemy import CHAR, Column, ForeignKey, Index, Integer, String, Table, Text # type: ignore | imported by Anki from vendor_BiblicalReference
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship # type: ignore | imported by Anki from vendor_BiblicalReference

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    testement: Mapped[Optional[str]] = mapped_column(String(15))
    group: Mapped[Optional[str]] = mapped_column(String(255))

    structure: Mapped[list['Structure']] = relationship('Structure', back_populates='book')
    title: Mapped[list['Title']] = relationship('Title', back_populates='book')


class Translation(Base):
    __tablename__ = 'translation'
    __table_args__ = (
        Index('idx_translation_code', 'code'),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    code: Mapped[Optional[str]] = mapped_column(String(7))
    lang_iso: Mapped[Optional[str]] = mapped_column(CHAR(3))

    pericope: Mapped[list['Pericope']] = relationship('Pericope', back_populates='translation')
    verse: Mapped[list['Verse']] = relationship('Verse', back_populates='translation')


class Pericope(Base):
    __tablename__ = 'pericope'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    id_translation: Mapped[Optional[int]] = mapped_column(ForeignKey('translation.id'))
    pericope_text: Mapped[Optional[str]] = mapped_column(String(255))

    translation: Mapped[Optional['Translation']] = relationship('Translation', back_populates='pericope')
    structure: Mapped[list['Structure']] = relationship('Structure', secondary='pericope_structure', back_populates='pericope')


class Structure(Base):
    __tablename__ = 'structure'
    __table_args__ = (
        Index('idx_structure_main', 'id_book', 'chapter_no', 'verse_no'),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    id_book: Mapped[Optional[int]] = mapped_column(ForeignKey('book.id'))
    chapter_no: Mapped[Optional[int]] = mapped_column(Integer)
    verse_no: Mapped[Optional[int]] = mapped_column(Integer)

    pericope: Mapped[list['Pericope']] = relationship('Pericope', secondary='pericope_structure', back_populates='structure')
    book: Mapped[Optional['Book']] = relationship('Book', back_populates='structure')
    verse: Mapped[list['Verse']] = relationship('Verse', back_populates='structure')


class Title(Base):
    __tablename__ = 'title'
    __table_args__ = (
        Index('idx_title', 'title_text'),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    id_book: Mapped[Optional[int]] = mapped_column(ForeignKey('book.id'))
    lang_iso: Mapped[Optional[str]] = mapped_column(CHAR(3))
    title_text: Mapped[Optional[str]] = mapped_column(String(255))

    book: Mapped[Optional['Book']] = relationship('Book', back_populates='title')


t_pericope_structure = Table(
    'pericope_structure', Base.metadata,
    Column('id_structure', ForeignKey('structure.id'), primary_key=True, nullable=True),
    Column('id_pericope', ForeignKey('pericope.id'), primary_key=True, nullable=True)
)


class Verse(Base):
    __tablename__ = 'verse'

    id_translation: Mapped[Optional[int]] = mapped_column(ForeignKey('translation.id'), primary_key=True, nullable=True)
    id_structure: Mapped[Optional[int]] = mapped_column(ForeignKey('structure.id'), primary_key=True, nullable=True)
    verse_text: Mapped[Optional[str]] = mapped_column(Text)

    structure: Mapped[Optional['Structure']] = relationship('Structure', back_populates='verse')
    translation: Mapped[Optional['Translation']] = relationship('Translation', back_populates='verse')
