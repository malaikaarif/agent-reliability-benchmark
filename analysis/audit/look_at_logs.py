import os

print("Top of logs folder:", os.listdir("logs")[:20])
paths = []
for root, dirs, files in os.walk("logs"):
    for f in files:
        paths.append(os.path.join(root, f))
print(len(paths), "files total")
print("First 10:", paths[:10])
if paths:
    with open(paths[0], encoding="utf-8", errors="replace") as fh:
        print("\n--- first 800 characters of", paths[0], "---")
        print(fh.read(800))
