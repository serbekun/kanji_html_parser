# Kanji HTML Parser API

## Acknowledgments

This project would not be possible without the excellent website [kanji.me](https://kanji.me), which provides high-quality, detailed information about Japanese kanji.  
We sincerely thank the creators and maintainers of kanji.me for their valuable contribution to Japanese language learning and for making this rich data openly accessible.

## Overview
This server provides an API for parsing information about Japanese kanji characters from the website [kanji.me](https://kanji.me).  
The server acts as a proxy parser: it scrapes structured kanji data and returns it in clean JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd kanji
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

To start the server, run:
```bash
python __main__.py
```

The server will be available at:  
`http://0.0.0.0:8000`

## API Documentation

### Endpoint

**GET** `/kanji/{kanji}`  
Returns structured information about the requested kanji character(s).

**Parameters:**
- `kanji` (string) — one or more kanji characters (maximum 5 characters)

**Example requests:**
```
GET /kanji/山
GET /kanji/愛
GET /kanji/日本
```

**Example response:**
```json
{
  "kanji": "山",
  "meanings_short": "mountain, hill",
  "basic_info": {
    "radical": {
      "kanji": "山",
      "reading": "さん / やま"
    },
    "stroke_count": 3,
    "kanken_level": "10級",
    "grade": "1年生",
    "categories": ["教育漢字", "常用漢字"],
    "jis_level": "第1水準"
  },
  "readings": {
    "on_yomi": ["サン", "セン"],
    "kun_yomi": ["やま"]
  },
  "meanings": [
    {
      "number": "1",
      "text": "A mountain or large hill."
    },
    {
      "number": "2",
      "text": "Something that resembles a mountain in shape."
    }
  ],
  "words": [
    {
      "word": "山",
      "reading": "やま",
      "meaning": "mountain"
    },
    {
      "word": "富士山",
      "reading": "ふじさん",
      "meaning": "Mount Fuji"
    },
    {
      "word": "登山",
      "reading": "とざん",
      "meaning": "mountain climbing"
    }
  ],
  "requested_kanji": "山",
  "fetched_at": "2026-03-14T14:35:22.187Z"
}
```

**Response structure:**
- `kanji` — the requested kanji character(s)
- `meanings_short` — short summary of main meanings (comma-separated)
- `basic_info` — core kanji metadata
  - `radical` — radical character and its reading
  - `stroke_count` — number of strokes
  - `kanken_level` — Kanji Kentei (Kanken) exam level
  - `grade` — Japanese school grade when the kanji is taught
  - `categories` — classification (Kyōiku kanji, Jōyō kanji, etc.)
  - `jis_level` — JIS standard level
- `readings`
  - `on_yomi` — Chinese-derived readings (on-reading)
  - `kun_yomi` — native Japanese readings (kun-reading)
- `meanings` — detailed numbered meaning explanations
- `words` — example vocabulary / compounds using this kanji
  - `word` — the compound word
  - `reading` — reading of the word
  - `meaning` — detailed meaning / explanation
- `requested_kanji` — echo of the requested input (for convenience)
- `fetched_at` — timestamp when the data was scraped (ISO format)

**Error codes:**
- `400` — Invalid request format (expected 1–5 kanji characters)
- `502` — Failed to connect to kanji.me
- `504` — Request to kanji.me timed out
- `500` — Internal server error


## License

This project is released under the **MIT License**.
