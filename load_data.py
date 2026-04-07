import fitz  # PyMuPDF
import re
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Extract full text and page count from PDF.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with fitz.open(pdf_path) as doc:
        full_text_parts = []

        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                full_text_parts.append(page_text)

        full_text = "\n".join(full_text_parts)
        page_count = len(doc)

    return full_text, page_count


def preview_pdf_pages(pdf_path, chars_per_page=1000):
    """
    Print preview of each page.
    """
    pdf_path = Path(pdf_path)

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")

            # print("=" * 80)
            # print(f"PAGE {page_num}")
            # print("=" * 80)
            # print(page_text[:chars_per_page] if page_text else "[NO TEXT FOUND]")
            # print("\n")


def clean_text_for_llm(text: str) -> str:
    """
    Clean PDF text while preserving basic structure.
    """

    if not text:
        return ""

    # Убираем мусорные символы
    text = text.replace('\x00', '')

    # Сохраняем абзацы: сначала нормализуем переносы
    text = re.sub(r'\r\n', '\n', text)

    # Убираем множественные переносы строк (оставляем максимум 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Убираем лишние пробелы внутри строк
    text = re.sub(r'[ \t]+', ' ', text)

    # Убираем пробелы в начале/конце строк
    text = "\n".join(line.strip() for line in text.splitlines())

    # Убираем пустые строки по краям
    text = text.strip()

    return text


def truncate_text(text: str, max_chars: int = 12000) -> str:
    """
    Limit text size for LLM input.
    """
    if not text:
        return ""

    return text[:max_chars]


def prepare_pdf_for_llm(pdf_path, max_chars: int = 12000):
    """
    Full pipeline:
    PDF → raw text → cleaned → truncated

    Returns:
        dict with useful info
    """
    raw_text, page_count = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text_for_llm(raw_text)
    truncated = truncate_text(cleaned_text, max_chars=max_chars)

    return {
        "page_count": page_count,
        "raw_length": len(raw_text),
        "cleaned_length": len(cleaned_text),
        "final_length": len(truncated),
        "text": truncated,
    }

import re


import re


def remove_image_captions(text: str) -> str:
    """
    Remove image captions, photo descriptions, and media-credit-like lines
    before sending text to the LLM.
    """

    if not text:
        return ""

    lines = text.split("\n")
    cleaned_lines = []

    caption_keywords = [
        "photo", "image", "caption", "credit", "getty", "reuters",
        "afp", "ap", "associated press", "file photo"
    ]

    scene_verbs = [
        "shown", "seen", "pictured", "stands", "sits", "walks", "looks",
        "holds", "rests", "plays", "waits", "shelters", "sleeps"
    ]

    scene_nouns = [
        "child", "children", "man", "woman", "people", "family", "families",
        "building", "street", "shelter", "camp", "tent", "home", "house"
    ]

    date_prefix_pattern = re.compile(
        r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b',
        re.IGNORECASE
    )

    for line in lines:
        l = line.strip()
        if not l:
            continue

        lower = l.lower()

        # 1. Explicit media/caption markers
        if any(k in lower for k in caption_keywords):
            continue

        # 2. Date-prefixed visual description lines
        # Example: "March 16, 2026 A child sits in..."
        if date_prefix_pattern.match(l):
            if any(noun in lower for noun in scene_nouns) and any(verb in lower for verb in scene_verbs):
                continue

        # 3. Scene-description lines even without explicit caption markers
        if any(noun in lower for noun in scene_nouns) and any(verb in lower for verb in scene_verbs):
            if len(l) < 220:
                continue

        # 4. Very short descriptive lines that often come from captions
        if len(l) < 80 and any(noun in lower for noun in scene_nouns):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)