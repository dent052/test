---
name: menu
description: 入っているスキルの一覧を表示するメニュー。/menu で手動実行したときだけ使う。
disable-model-invocation: true
---

# スキルメニュー

1. `python3 .claude/skills/menu/list_skills.py` を実行する。
2. 出力を加工・要約せず、そのまま番号付きで表示する。
3. 「番号か名前を選んでください」と案内して止まる。
4. ユーザーが選ぶまで、どのスキルも実行しない。自分でスキルを選ばない。
5. 選ばれたら、そのスキルを Skill ツールでそのまま呼び出す。
