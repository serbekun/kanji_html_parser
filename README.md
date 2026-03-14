# 漢字 HTML Parser API

## 謝辞

このプロジェクトは、非常に優れた漢字情報サイト [kanji.me](https://kanji.me) なしには実現できませんでした。  
詳細で質の高い漢字情報を公開し、日本語学習を支えてくださっている kanji.me の開発者・運営者の皆様に心より感謝申し上げます。

## 概要
このサーバーは、kanji.me のサイトから日本語の漢字（かんじ）に関する情報を解析し、構造化されたデータを JSON 形式で提供する API です。  
サーバーはプロキシ・パーサーとして機能し、kanji.me から取得したデータを整理して返します。

## インストール

1. リポジトリをクローンします：
```bash
git clone <repository-url>
cd kanji
```

2. 依存関係をインストールします：
```bash
pip install -r requirements.txt
```

## サーバーの起動

以下のコマンドでサーバーを起動してください：
```bash
python __main__.py
```

サーバーは次のアドレスで利用可能になります：  
`http://0.0.0.0:8000`

## API ドキュメント

### エンドポイント

##### GET /kanji/{kanji}

指定した漢字の構造化された情報を返します。

**パラメータ：**
- `kanji` (string): 漢字1〜5文字（最大5文字）

**リクエスト例：**
```
GET /kanji/山
GET /kanji/愛
GET /kanji/日本
```

**レスポンス例：**
```json
{
  "kanji": "山",
  "meanings_short": "やま、山、峰、など",
  "basic_info": {
    "radical": {
      "kanji": "山",
      "reading": "サン"
    },
    "stroke_count": "3",
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
      "text": "土地が盛り上がったもの。やま。"
    },
    {
      "number": "2",
      "text": "山のような形をしたもの。"
    }
  ],
  "words": [
    {
      "word": "山",
      "reading": "やま",
      "meaning": "盛り上がった土地。自然の高い地形。"
    },
    {
      "word": "富士山",
      "reading": "ふじさん",
      "meaning": "日本で最も有名な火山で、標高3,776m。"
    }
  ],
  "requested_kanji": "山",
  "fetched_at": "2026-03-14T12:34:56Z"
}
```

**レスポンスの構造：**

- `kanji`: 対象の漢字
- `meanings_short`: 意味の短いまとめ（コンマ区切り）
- `basic_info`: 基本情報
  - `radical`: 部首とその読み
  - `stroke_count`: 画数
  - `kanken_level`: 漢検の級
  - `grade`: 小学校の学年
  - `categories`: 分類（教育漢字、常用漢字など）
  - `jis_level`: JIS水準
- `readings`: 読み方
  - `on_yomi`: 音読み
  - `kun_yomi`: 訓読み
- `meanings`: 詳細な意味（番号付き）
- `words`: 漢字を使った単語・熟語の例
  - `word`: 単語
  - `reading`: 読み方
  - `meaning`: 意味・解説
- `requested_kanji`: リクエストされた漢字（重複）
- `fetched_at`: データ取得日時（ISO形式）

**エラーコード：**

- `400` → 不正なリクエスト（1〜5文字の漢字を期待）
- `502` → kanji.me への接続エラー
- `504` → kanji.me へのリクエストがタイムアウト
- `500` → サーバー内部エラー


## ライセンス

MIT License
