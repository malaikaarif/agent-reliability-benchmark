import os, json, re, collections
pat = re.compile(r"(t\d+)_([a-z]+)_r(\d+)_(\d{8})_(\d{6})")
cnt = collections.Counter(); sample = {}
for root, dirs, files in os.walk("logs"):
    for f in files:
        if not f.endswith(".json"):
            continue
        m = pat.search(f)
        key = (root, m.group(2) if m else "?", m.group(4) if m else "?")
        cnt[key] += 1
        sample.setdefault(root, os.path.join(root, f))
for k, v in sorted(cnt.items()):
    print(k, v)
for root, p in sample.items():
    print("\n=====", p)
    with open(p, encoding="utf-8", errors="replace") as fh:
        print(fh.read(1200))
