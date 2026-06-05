import os

walkthrough_path = r"C:\Users\ATSAdmin\.gemini\antigravity-ide\brain\05624b30-c507-4cfd-a9e7-c81b94063ae0\walkthrough.md"

md = ["\n\n## 전체 코드베이스 (Full Codebase)\n\n"]

files_to_read = [
    "docker/docker-compose.yml",
    "run.py",
    "cli.py",
]

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            files_to_read.append(os.path.join(root, file))

for filepath in files_to_read:
    if os.path.exists(filepath):
        md.append(f"### File: `{filepath.replace(chr(92), '/')}`\n")
        ext = "yaml" if filepath.endswith(".yml") else "python"
        md.append(f"```{ext}\n")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                md.append(f.read())
        except Exception as e:
            md.append(f"# Error reading file: {e}")
        md.append("\n```\n\n")

with open(walkthrough_path, "a", encoding="utf-8") as f:
    f.write("".join(md))
