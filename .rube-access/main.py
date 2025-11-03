# Rube Reader: Repo Scanner for make-ops-clean
import os
import json

def scan_repo(root_dir="."):
    file_tree = {
        "files": [],
        "total": 0,
        "copy": [],
        "tests": [],
        "drafts": [],
        "unused": [],
        "other": []
    }

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(root, file)
            if not file.endswith(".py"):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                content = ""

            data = {
                "path": path,
                "lines": len(content.splitlines()),
                "bytes": len(content.encode('utf-8'))
            }

            if "copy_" in file:
                file_tree["copy"].append(data)
            elif "test" in file or "tests" in path:
                file_tree["tests"].append(data)
            elif "draft" in file or "drafts" in path:
                file_tree["drafts"].append(data)
            elif "compose" in file or ".json" in file:
                file_tree["other"].append(data)
            else:
                file_tree["unused"].append(data)

    file_tree["total"] = sum(len(file_tree[k]) for k in ["copy", "tests", "drafts", "unused", "other"])
    return file_tree

output = scan_repo()
with open('.rube-access/repo_tree.json', 'w') as out:
    json.dump(output, out, ensure=True)
