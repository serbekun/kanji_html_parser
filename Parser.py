"""KanjiPageParser parses kanji.me HTML pages and returns structured JSON data."""
import json
import re
from bs4 import BeautifulSoup
from typing import Optional

def parse_kanji_page(html: str) -> dict:
    """Top-level parser that returns a dict of kanji page data."""
    soup = BeautifulSoup(html, "html.parser")
    
    
    # Private helpers
    def _get_kanji() -> Optional[str]:
        """Extracts the kanji symbol from <main data-kanji="...">."""
        main = soup.find("main", {"data-kanji": True})
        if main:
            return main.get("data-kanji")
        # fallback: breadcrumb
        span = soup.select_one("nav span.japanese-text")
        return span.get_text(strip=True) if span else None
    

    def _get_meanings_short() -> Optional[str]:
        """Short meaning text beneath the primary content."""
        section = soup.find("section", {"id": "basic-info"})
        if not section:
            return None
        div = section.select_one("div.text-lg.font-bold")
        return div.get_text(strip=True) if div else None
    

    def _get_basic_info() -> dict:
        """Parses the Basic Information section (radical, stroke count, kanken, grade, categories, JIS level)."""
        result = {}
        section = soup.find("section", {"id": "basic-info"})
        if not section:
            return result
        items = section.select("div.info-item")
        for item in items:
            label_el = item.select_one("span.info-label")
            if not label_el:
                continue
            label = label_el.get_text(strip=True)
            if label == "部首":
                # Radical name(s) + reading in parentheses
                kanji_span = item.select_one("span.japanese-text")
                # The reading span has a parenthesised text like (こころ・...)
                reading_span = item.select_one("div.radical-content span.text-xs")
                result["radical"] = {
                    "kanji": kanji_span.get_text(strip=True) if kanji_span else None,
                    "reading": reading_span.get_text(strip=True) if reading_span else None,
                }
            elif label == "画数":
                a = item.find("a")
                result["stroke_count"] = int(a.get_text(strip=True).replace("画", "")) if a else None
            elif label == "漢検":
                a = item.find("a")
                result["kanken_level"] = a.get_text(strip=True) if a else None
            elif label == "学年":
                a = item.find("a")
                result["grade"] = a.get_text(strip=True) if a else None
            elif label == "種別":
                links = item.select("a")
                result["categories"] = [a.get_text(strip=True) for a in links]
            elif label == "JIS水準":
                # Take the first span that is NOT the info-label
                spans = item.select("span")
                jis_spans = [s for s in spans if "info-label" not in (s.get("class") or [])]
                result["jis_level"] = jis_spans[0].get_text(strip=True) if jis_spans else None
        return result
    

    def _get_readings() -> dict:
        """Processes the Readings section and categorizes on-yomi and kun-yomi."""
        result = {"on_yomi": [], "kun_yomi": []}
        section = soup.find("section", {"id": "readings"})
        if not section:
            return result
        divs = section.select("div.rounded-lg")
        for div in divs:
            label_el = div.select_one("div.text-xs.font-medium")
            if not label_el:
                continue
            label = label_el.get_text(strip=True)
            buttons = div.select("button.reading-sound-btn")
            readings = [btn.select_one("span.reading-text").get_text(strip=True)
                        for btn in buttons
                        if btn.select_one("span.reading-text")]
            if "音読み" in label:
                result["on_yomi"] = readings
            elif "訓読み" in label:
                result["kun_yomi"] = readings
        return result
    

    def _get_meanings() -> list[dict]:
        """Extracts numbered meanings from the Meanings section."""
        meanings = []
        section = soup.find("section", {"id": "meanings"})
        if not section:
            return meanings
        items = section.select("div.meaning-item")
        for item in items:
            num_el = item.select_one("span.meaning-number-inner")
            text_el = item.select_one("p")
            if text_el:
                meanings.append({
                    "number": int(num_el.get_text(strip=True)) if num_el else None,
                    "text": text_el.get_text(strip=True),
                })
        return meanings
    

    def _get_words() -> list[dict]:
        """Extracts word compounds with kanji, reading, and meaning."""
        words = []
        section = soup.find("section", {"id": "words"})
        if not section:
            return words
        cards = section.select("div.word-card")
        for card in cards:
            # Collect the kanji characters for this word
            char_links = card.select("a.kanji-char")
            word = "".join(a.get_text(strip=True) for a in char_links)
            # Reading without brackets 【】
            reading_div = card.select_one("div.word-reading")
            reading = ""
            if reading_div:
                raw = reading_div.get_text(strip=True)
                reading = re.sub(r"[【】]", "", raw).strip()
            # Meaning
            meaning_div = card.select_one("div.word-meaning")
            meaning = meaning_div.get_text(strip=True) if meaning_div else ""
            if word:
                words.append({
                    "word": word,
                    "reading": reading,
                    "meaning": meaning,
                })
        return words
    
    # Assemble the final payload
    return {
        "kanji": _get_kanji(),
        "meanings_short": _get_meanings_short(),
        "basic_info": _get_basic_info(),
        "readings": _get_readings(),
        "meanings": _get_meanings(),
        "words": _get_words(),
    }


def to_kanji_json(html: str, indent: int = 2) -> str:
    """Returns parse_kanji_page() output formatted as JSON."""
    return json.dumps(parse_kanji_page(html), ensure_ascii=False, indent=indent)

# Usage
# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1:
#         # Read HTML from the file provided as an argument
#         with open(sys.argv[1], encoding="utf-8") as f:
#             html = f.read()
#     else:
#         print("Usage: python kanji_parser.py <path_to_html_file>")
#         print("\nDemo: running with a minimal stub to show structure...")
#         html = "<html><main data-kanji='意'></main></html>"
#     print(to_kanji_json(html))
