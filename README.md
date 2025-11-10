# Ops Status

[![Append Index (UTC hourly)](https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append.yml/badge.svg?branch=main)](https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append.yml)

## OPS QUICK ACTIONS
- Manual Run: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append-manual.yml
- Scheduled Runs: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append.yml?query=event%3Aschedule
- Evidence Index – Index: https://docs.google.com/spreadsheets/d/1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0/edit#gid=0
- Evidence Index – L2: https://docs.google.com/spreadsheets/d/1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0/edit#gid=301368480

---

**E2E smoke test** — Testing L1.2 Zero-Touch Telegram approval flow

---

<details><summary>OPS CHAT BLOCK (copy/paste)</summary>

```md
# OPS CHAT BLOCK — Pin me

## ▶️ Run ידני
https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append-manual.yml
(לחץ/י "Run workflow", Branch: main)

## ⏱️ ריצות (שעתי)
https://github.com/edri2or-commits/make-ops-clean/actions/workflows/index-append.yml

## 📄 גיליון Index
https://docs.google.com/spreadsheets/d/1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0/edit

## ✅ אימות מהיר (אחרי Run)
1) פתח/י את הריצה האחרונה → "Artifacts" → הורד/י sheet-append-response.zip → פתח/י resp.json  
   בדוק/י: "updatedRange", "updatedRows".
2) או גלול/י ל-Run Summary וחפש/י שורה בסגנון:  
   `updatedRange=Index!A?:D? updatedRows=1 updatedColumns=4 updatedCells=4`

## ℹ️ טיפ
- Schedule רץ לפי UTC.
- אפשר גם בצ'אט: "ops run index-append" / "ops artifacts last".
