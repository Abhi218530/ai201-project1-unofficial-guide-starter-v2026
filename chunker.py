"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

"""
Stage 2 of the pipeline: splitting documents into chunks.

Replaced in Milestone 3: paragraph-aware chunking instead of fixed-size
windows. See split_documents for the reasoning.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.
    Kept for comparison — Milestone 3's stop rule points back at it.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


def _pack_sentences(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Only used when a single paragraph is bigger than chunk_size on its own.
    Packs whole sentences up to chunk_size, carrying trailing sentences
    forward as overlap so a fact split across the boundary still appears
    whole somewhere."""
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    if not sentences:
        return [text]

    pieces, current, current_len = [], [], 0
    for sent in sentences:
        sent_len = len(sent) + 1
        if current and current_len + sent_len > chunk_size:
            pieces.append(" ".join(current))
            carry, carry_len = [], 0
            for s in reversed(current):
                if carry_len + len(s) + 1 > overlap:
                    break
                carry.insert(0, s)
                carry_len += len(s) + 1
            current, current_len = carry, carry_len
        current.append(sent)
        current_len += sent_len
    if current:
        pieces.append(" ".join(current))
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunking, chosen after reading campus_life directly:
    most posts (e.g. admin_dining_dollars) are short enough that the whole
    post is one coherent chunk. Longer posts and multi-reply threads
    (advice_threads) get split at paragraph/reply boundaries, which are
    already natural units — only a single oversized paragraph falls back
    to sentence-packing.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()

        if len(text) <= chunk_size:
            chunks.append(Chunk(text=text, source=doc.source, index=0,
                                 produced_by="chunker.py::split_documents"))
            continue

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        idx = 0
        buffer = ""

        def flush():
            nonlocal buffer, idx
            if buffer:
                chunks.append(Chunk(text=buffer, source=doc.source, index=idx,
                                     produced_by="chunker.py::split_documents"))
                idx += 1
                buffer = ""

        for para in paragraphs:
            candidate = f"{buffer}\n\n{para}".strip() if buffer else para
            if len(candidate) <= chunk_size:
                buffer = candidate
            else:
                flush()
                if len(para) <= chunk_size:
                    buffer = para
                else:
                    for piece in _pack_sentences(para, chunk_size, overlap):
                        chunks.append(Chunk(text=piece, source=doc.source, index=idx,
                                             produced_by="chunker.py::split_documents"))
                        idx += 1
        flush()

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))