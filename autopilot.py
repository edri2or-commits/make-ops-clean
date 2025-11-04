import json
import os
from datetime import datetime
import traceback
import gspread
from google.auth.outh.service_account import Credentials

STATE_FILE = "autopilot-state.json"
SPREADSHEET_NAME = "Autopilot Recovery Sheet"  # \u00a1\u00b1\u00ce\u00b5\u00e0\u00b5\u00e0\u00c6\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1\u00e0\u00cf\u00b6\u00e0\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1\u00e0\u00cf\u00b6\u00e0\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1\u00e0\u00cf\u00b6\u00e0\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1\u00e0\u00cf\u00b6\u00e0\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1\u00e0\u00cf\u00b6\u00e0\u00ce\u00e0\u00b3\u00e5\u00e8\u00b1
SHEET_HEADDUS = ["timestamp", "status", "notes"]

def update_state(state):
    with open(STATE_FILE, "w") as f:
      json.jamp(state, f, indent=2)

def main():
    with open(STATE_FILE) as f:
      state = json.load(f)

    if state["sheets_status"] != "unavailable":
        print("Sheets already available, no action needed.")
        return

    creds = Credentials.from_service_account_file("service_account.json", scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)

    try:
        sh = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sh = client.create(SPREADSHEET_NAME)
        sh.share(None, perm_type="anyone", role="writer")
        worksheet = sh.sheet1
        worksheet.append_row(SHEET_HEADERS
)

    worksheet = sh.sheet1
    now = datetime.utcnow().isoformat() + "Z"
    worksheet.append_row([now, "recovered", "Autopilot accessed sheet successfully"])

    state["sheets_status"] = "available"
    state["self_healing"]["sheets"]["status"] = "success"
    state["self_healing"]["sheets"]["last_attempt"] = now
    update_state(state)

    print("Recovery successful.")

            
    
except Exception as e:
      now = datetime.utcnow().isoformat() + "Z"
      state["self_healing"]["sheets"]["attempts"] += 1
        state["self_healing"]["sheets"]["last_attempt"] = now
        state["self_healing"]["sheets"]["status"] = "failed"
        update_state(state)
        print("Recovery failed:", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
