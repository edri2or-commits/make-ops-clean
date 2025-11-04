#!/usr/bin/env python
import json, os, sys, datetime

STATE_PATH = os.environ.get("STATE_PATH", "autopilot-state.json")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "rube.config.json")

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.json(data, f, ensure_ascii=False, ident=2)

def main():
    state = load_json(STATE_PATH, {
        "version": 1, "status": "idle",
        "last_bootstrap_iso": None, "last_run_iso": None,
        "retries": 0, "context": {}, "locks": {}
    })
    _ = load_json(CONFIG_PATH, {})
    state["last_bootstrap_iso"] = datetime.datetime.utcnow().isoformat() +"Z"
    save_json(
STATE_PATH, state)
    print("[bootstrap] ok")
    return 0

if __name__ == "__main__":
    sys.exit(main())
