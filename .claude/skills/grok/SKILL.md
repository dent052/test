---
name: grok
description: Grok（xAI）に X（旧Twitter）のリアルタイム検索をさせて情報収集するスキル。「Xで調べて」「ツイッターの反応」「Xの評判」「grokに聞いて」「x_search」などと言われたとき、または /grok で呼ばれたときに使う。用途は話題・評判・炎上・速報・特定アカウントの発言の調査。Claude の WebSearch では X の投稿がほぼ取れないため、X の情報はこちらを使う。
---

# Grok（X 検索）

Claude の WebSearch / WebFetch は X の投稿をほとんど取れない。X の情報は Grok Build CLI に検索させ、
その結果を Claude がまとめる。料金は X / SuperGrok のプランに含まれる分だけで済ませる。

**従量課金（xAI API キー、`XAI_API_KEY`）は絶対に使わない。** API キー経由だと課金されるため、
必ずプランのログイン（`grok login`）で動かす。`XAI_API_KEY` が設定されていても `env -u` で外して実行する。
`api.x.ai` を curl で直接呼ぶのも禁止。

まず `command -v grok` を確認する。なければ下の「セットアップ」をユーザーに案内して止まる。

## 実行コマンド

```bash
env -u XAI_API_KEY -u GROK_CODE_XAI_API_KEY grok --no-auto-update -p "<依頼文>" --sandbox read-only --cwd <作業ディレクトリ> --output-format plain
```

- `--sandbox read-only`: Grok にファイルを書き換えさせない
- `--no-auto-update`: 非対話実行で更新チェックを止める
- 検索には時間がかかるので、Bash ツールの `timeout` を長め（例: 600000）にする
- ログインが切れていたら、API キーで代用せず、ユーザーに `grok login` をやり直してもらう

## 依頼文のルール

依頼文の末尾に必ず次を付ける:

> X を検索して答えてください。根拠にした投稿は URL（https://x.com/...）と投稿日を必ず付けてください。確認や質問は不要です。

例:
- `Claude Code の新機能について、ここ1週間の X での反応を賛否に分けてまとめてください。`
- `@SuzukuStudio が最近 AI ツールについて投稿した内容を要約してください。`

## 手順

1. 調べたい話題・期間・対象アカウントを把握する
2. 依頼文を組み立てて実行する
3. 結果を日本語で要約して報告する。投稿 URL を出典として残す
4. Grok の要約は鵜呑みにしない。重要な主張は URL を確認したり、WebSearch で裏を取ったりする。
   「X 上の声」であって事実とは限らないことも添える

## セットアップ（未設定のときにユーザーへ案内する）

- `curl -fsSL https://x.ai/cli/install.sh | bash` でインストールし、`grok login` でログインする
  （ブラウザがない環境では `grok login --device-auth`）。X のプランに Grok Build が含まれていれば追加料金なし
- API キー（console.x.ai）は従量課金なので作らない・使わない
- Claude Code のクラウド環境で使う場合: 環境のネットワーク設定で `x.ai` と `api.x.ai` への通信を許可する
