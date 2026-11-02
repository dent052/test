---
name: grok
description: Grok（xAI）に X（旧Twitter）のリアルタイム検索をさせて情報収集するスキル。「Xで調べて」「ツイッターの反応」「Xの評判」「grokに聞いて」「x_search」などと言われたとき、または /grok で呼ばれたときに使う。用途は話題・評判・炎上・速報・特定アカウントの発言の調査。Claude の WebSearch では X の投稿がほぼ取れないため、X の情報はこちらを使う。
---

# Grok（X 検索）

Claude の WebSearch / WebFetch は X の投稿をほとんど取れない。X の情報は Grok に検索させ、
その結果を Claude がまとめる。経路は 2 つ。使える方を使う。

| 経路 | 料金 | 必要なもの |
| --- | --- | --- |
| A. Grok Build CLI（`grok -p`） | X / SuperGrok のプランに含まれる | `grok` がインストール済みでログイン済み |
| B. xAI API の `x_search` | 従量課金（投稿1000件あたり $5 + トークン代） | 環境変数 `XAI_API_KEY` |

まず `command -v grok` を確認する。あれば A、なければ `XAI_API_KEY` を確認して B。
どちらもなければ、下の「セットアップ」をユーザーに案内して止まる。

## A. Grok Build CLI

```bash
grok --no-auto-update -p "<依頼文>" --sandbox read-only --cwd <作業ディレクトリ> --output-format plain
```

- `--sandbox read-only`: Grok にファイルを書き換えさせない
- `--no-auto-update`: 非対話実行で更新チェックを止める
- 検索には時間がかかるので、Bash ツールの `timeout` を長め（例: 600000）にする

## B. xAI API（x_search）

```bash
curl -sS -m 300 https://api.x.ai/v1/responses \
  -H "Authorization: Bearer $XAI_API_KEY" -H "Content-Type: application/json" \
  -d "$(jq -n --arg q "<依頼文>" '{model:"grok-4.7", input:$q, tools:[{type:"x_search"}]}')" \
  | jq -r '.output[] | select(.type=="message") | .content[] | .text'
```

`tools` の `x_search` には次の絞り込みを足せる（`allowed` と `excluded` は同時に使えない）:

- `"allowed_x_handles": ["SpaceX"]` / `"excluded_x_handles": [...]`（`@` なし、最大20件）
- `"from_date": "2026-10-01", "to_date": "2026-10-08"`（`YYYY-MM-DD`。`to_date` の日は含まない）

課金は取得した投稿の件数で決まる。「上位10件程度で」のように件数を絞る依頼文にする。

## 依頼文のルール

依頼文の末尾に必ず次を付ける:

> X を検索して答えてください。根拠にした投稿は URL（https://x.com/...）と投稿日を必ず付けてください。確認や質問は不要です。

例:
- `Claude Code の新機能について、ここ1週間の X での反応を賛否に分けてまとめてください。`
- `@SuzukuStudio が最近 AI ツールについて投稿した内容を要約してください。`

## 手順

1. 調べたい話題・期間・対象アカウントを把握する
2. 経路を決め、依頼文を組み立てて実行する
3. 結果を日本語で要約して報告する。投稿 URL を出典として残す
4. Grok の要約は鵜呑みにしない。重要な主張は URL を確認したり、WebSearch で裏を取ったりする。
   「X 上の声」であって事実とは限らないことも添える

## セットアップ（未設定のときにユーザーへ案内する）

- A: `curl -fsSL https://x.ai/cli/install.sh | bash` でインストールし、`grok login` でログインする
  （ブラウザがない環境では `grok login --device-auth`）。X のプランに Grok Build が含まれていれば追加料金なし
- B: https://console.x.ai で API キーを作り、`XAI_API_KEY` に設定する
- Claude Code のクラウド環境で使う場合: 環境のネットワーク設定で `x.ai` と `api.x.ai` への通信を許可する
