"""Merge round output files into solo-income/ideas.md.

Usage: python3 merge.py <round> "<lenses>" "<note>" --drop ID,ID -- file1.md file2.md ...
Renumbers kept cards to I-NNN, appends them under a round heading in ## Ideas,
and adds a row to the round log.
"""
import os
import re
import sys

IDEAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ideas.md")

args = sys.argv[1:]
rnd, lenses, note = args[0], args[1], args[2]
drop = set()
if "--drop" in args:
    i = args.index("--drop")
    drop = {d.strip() for d in args[i + 1].split(",") if d.strip()}
files = args[args.index("--") + 1:]

text = open(IDEAS).read()
existing = [int(n) for n in re.findall(r"^### I-(\d{3})", text, re.M)]
next_id = max(existing, default=0) + 1

card_re = re.compile(r"^### (R\d+[A-Z]-\d+) · (.*)$", re.M)
kept, proposed, idmap = [], 0, {}
for path in files:
    body = open(path).read()
    body = body.split("Lens notes:")[0]
    starts = list(card_re.finditer(body))
    for j, m in enumerate(starts):
        proposed += 1
        end = starts[j + 1].start() if j + 1 < len(starts) else len(body)
        card = body[m.start():end].strip()
        if m.group(1) in drop:
            continue
        new_id = f"I-{next_id:03d}"
        next_id += 1
        card = card.replace(f"### {m.group(1)} ·", f"### {new_id} ·", 1)
        idmap[m.group(1)] = new_id
        kept.append(card)

kept = [re.sub(r"\b(R\d+[A-Z]-\d+)\b", lambda x: idmap.get(x.group(1), x.group(1) + " (dropped)"), c) for c in kept]
block = f"\n**Round {rnd[1:]}** ({lenses})\n\n" + "\n\n".join(kept) + "\n"
marker = "\n## Round log"
text = text.replace(marker, block + marker, 1)
text = text.rstrip("\n") + f"\n| {rnd[1:]} | {lenses} | {proposed} | {len(kept)} | {note} |\n"
open(IDEAS, "w").write(text)
print(f"proposed={proposed} kept={len(kept)} next_id={next_id}")
