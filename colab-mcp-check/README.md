# Colab MCP 使えるかチェック

ゴール: **(1) 自分のアカウントでColab MCPが通るか (2) PlusでどのGPUが選べるか** を確定させる。
所要 15分くらい。手元のPCで実行（Googleログインが要るため）。GPUは起動しないのでCUは減らない。

## 0. 前提
- `gcloud` CLI が入っている（無ければ https://cloud.google.com/sdk/docs/install ）
- Google AI Plus を契約しているGoogleアカウント

## 1. GCPプロジェクトを作ってAPIを有効化
```bash
gcloud auth login                        # Plus契約のアカウントで
gcloud projects create my-colab-test-$RANDOM   # 既存プロジェクトがあればそれでOK
gcloud config set project <作ったPROJECT_ID>
gcloud services enable colaboratory.googleapis.com
```
※ 課金アカウントの紐付けは基本不要のはず。エラーで求められたら教えてください。

### ハマりどころ（実測）
- Google Cloud初利用のアカウントは、先に https://console.cloud.google.com/ で利用規約に同意しないとプロジェクト作成が `Callers must accept Terms of Service` で失敗する
- 新規プロジェクトでは `serviceusage.googleapis.com` も有効化が必要。有効化するまでは `x-goog-user-project` ヘッダーを付けると403になる

## 2. 認証（ADC）
```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/colaboratory
```
**「このアプリはブロックされています」と出たら** → gcloud標準クライアントではColabスコープが許可されていない。
自前のOAuthクライアントを作る:
1. Cloud Console → 「Google Auth Platform」→ 同意画面を作成（外部 / テストユーザーに自分を追加）
2. 「クライアント」→ 作成 → 種類 **デスクトップアプリ** → JSONをダウンロード
3. ```bash
   gcloud auth application-default login --client-id-file=client_secret_xxx.json \
     --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/colaboratory
   ```

## 3. チェック実行
```bash
PROJECT_ID=<PROJECT_ID> ./check.sh
```

## 4. 結果の読み方
| 出力 | 意味 |
|---|---|
| `get_subscription` がプラン名を返す | **MCPは使える**。Plusが Colab上で free / Pro 等どう扱われてるかもここで分かる |
| `list_runtime_specs` で A100 / G4 が eligible | **Plusでも大容量GPUが選べる** → 前回話した「本当に新しいこと」ができる |
| T4 / L4 しか eligible でない | Plusは「Colabがちょっと快適になる」止まり |
| 401 | 認証失敗。手順2をやり直し（スコープ漏れが多い） |
| 403 `PERMISSION_DENIED` / `SERVICE_DISABLED` | 手順1のAPI有効化漏れ、またはプロジェクトIDの指定ミス |
| 403 で allowlist 的なメッセージ | アカウントがまだ対象外 |

## 5. （通ったら）Claude Code に繋ぐ
```bash
claude mcp add --transport http colab https://colaboratory.googleapis.com/mcp \
  --header "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  --header "x-goog-user-project: <PROJECT_ID>"
```
トークンは約1時間で切れるので、お試し用。切れたら `claude mcp remove colab` → 再登録。
繋いだら Claude Code に「Colabの get_subscription と list_runtime_specs を叩いて」と頼めば同じ確認ができる。

## 実測結果（2026-11-25, Google AI Plus契約アカウント）
- gcloud標準クライアントでColabスコープはブロックされなかった
- `get_subscription` → `SUBSCRIPTION_TIER_PRO`（PlusでもColab上はPro扱い）
- `list_runtime_specs` で eligible: T4 / L4 / A100 / G4 / TPU v5e-1・v6e-1 / CPU。H100 は対象外
