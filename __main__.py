from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime
from typing import Dict, Any

from config import Config

# Parser entry point
from Parser import parse_kanji_page

KANJI_SERVER_BASE_URL = "https://kanji.me/"

app = FastAPI(
    title="Kanji HTML Parser API",
    description="Proxy parser for kanji.me pages",
    version="0.1.0"
)


# Endpoints
@app.get("/kanji/{kanji}")
async def get_kanji(kanji: str) -> Dict[str, Any]:
    """
    Retrieve structured information for a kanji character.

    Examples:
      GET /kanji/山
      GET /kanji/愛
    """
    if not kanji.strip() or len(kanji.strip()) > 5:
        raise HTTPException(400, detail="Expected 1-5 kanji characters")

    try:
        resp = requests.get(
            f"{KANJI_SERVER_BASE_URL}{kanji}",
            timeout=12,
            headers={"User-Agent": "Kanji-API/0.1 (compatible; +your-contact-email)"}
        )
        resp.raise_for_status()

        data = parse_kanji_page(resp.text)
        data["requested_kanji"] = kanji
        data["fetched_at"] = datetime.utcnow().isoformat()

        return data

    except requests.Timeout:
        raise HTTPException(504, "kanji.me request timed out")
    except requests.HTTPError as e:
        raise HTTPException(502, f"kanji.me returned error {e.response.status_code}")
    except requests.RequestException as e:
        raise HTTPException(502, f"Unable to connect to kanji.me: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {str(e)}")


# Startup
def main():
    import uvicorn

    now = datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Starting FastAPI server...")
    print(f" → http://{Config.HOST}:{Config.PORT}")
    print(" → Docs:     http://github.com/serbekun/docs")

    uvicorn.run(
        "__main__:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=False,
        log_level="info",
        # workers=2,              # enable for production
    )


if __name__ == "__main__":
    main()
