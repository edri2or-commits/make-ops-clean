
import json
import os
from datetime import datetime

file_path = "RUBE.live.json"

def load_current():
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def update_data(data):
    now = datetime.utcnow().isoformat() + "Z"
    data["generated_at"] = now
    executions = data.get("executions", [])
    executions.append({"timestamp": now, "event": "auto-sync", "source": "GitHub Action"})
    data["executions"] = executions[-100:]
    history = data.get("history", [])
    history.append({"timestamp": now, "summary": "Updated by GitHub Action"})
    data["history"] = history[-100:]
    return data

def save_updated(data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

current = load_current()
updated = update_data(current)
save_updated(updated)