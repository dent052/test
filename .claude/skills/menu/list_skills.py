import glob
import os
import re
import sys

home = os.path.expanduser("~")
cwd = os.getcwd()

# (表示名, 検索パターン)
SOURCES = [
    ("プロジェクト", os.path.join(cwd, ".claude/skills/*/SKILL.md")),
    ("個人用", os.path.join(home, ".claude/skills/*/SKILL.md")),
    ("個人用(同期)", os.path.join(home, ".claude/skills/synced/*/*/SKILL.md")),
    ("プラグイン", os.path.join(home, ".claude/plugins/cache/**/skills/*/SKILL.md")),
]


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    front = m.group(1)
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    if not name:
        return None
    desc = desc.group(1).strip().strip("\"'") if desc else ""
    return name.group(1).strip().strip("\"'"), desc


def short(desc, limit=60):
    desc = desc.replace("\n", " ")
    return desc if len(desc) <= limit else desc[:limit] + "…"


seen = set()
rows = []
for label, pattern in SOURCES:
    for path in sorted(glob.glob(pattern, recursive=True)):
        if os.path.basename(os.path.dirname(path)) == "menu":
            continue
        parsed = parse(path)
        if not parsed or parsed[0] in seen:
            continue
        seen.add(parsed[0])
        rows.append((label, parsed[0], short(parsed[1])))

if not rows:
    sys.exit("スキルが見つかりませんでした")

current = None
n = 0
for label, name, desc in rows:
    if label != current:
        print(f"\n【{label}】")
        current = label
    n += 1
    print(f"{n:>2}. /{name} — {desc}")
