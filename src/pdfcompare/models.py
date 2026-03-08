from __future__ import annotations

from dataclasses import dataclass

RectTuple = tuple[float, float, float, float]


@dataclass(frozen=True)
class WordBox:
    page_index: int
    line_index: int
    word_index: int
    text: str
    norm: str
    rect: RectTuple


@dataclass(frozen=True)
class LineBox:
    page_index: int
    line_index: int
    text: str
    norm_text: str
    words: list[WordBox]


@dataclass(frozen=True)
class PageBox:
    page_index: int
    lines: list[LineBox]

    @property
    def text(self) -> str:
        return "\n".join(line.text for line in self.lines)

    @property
    def norm_text(self) -> str:
        return "\n".join(line.norm_text for line in self.lines)