#!/usr/bin/env bash
# Colab MCP 疎通チェック: 自分のアカウントでMCPが使えるか / 何のGPUが選べるか を確認する
# 使い方: PROJECT_ID=my-project ./check.sh
set -euo pipefail
: "${PROJECT_ID:?PROJECT_ID を指定してください (例: PROJECT_ID=my-colab-test ./check.sh)}"
EP=https://colaboratory.googleapis.com/mcp
TOKEN=$(gcloud auth application-default print-access-token)

call() { # $1=tool名
  curl -sS -X POST "$EP" \
    -H "Authorization: Bearer $TOKEN" \
    -H "x-goog-user-project: $PROJECT_ID" \
    -H 'content-type: application/json' \
    -H 'accept: application/json, text/event-stream' \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":{}}}"
}

echo "== get_subscription (Colab上のプラン扱い) =="
call get_subscription | python3 -m json.tool
echo
echo "== list_runtime_specs (選べるGPU / eligible かどうか) =="
call list_runtime_specs | python3 -m json.tool
