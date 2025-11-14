# GitHub App Authentication - Cloud Testing Setup

## ✅ Cloud-Ready Migration Complete

הסקריפט והתשתית מוכנים להרצה בענן (GitHub Actions) ללא צורך במחשב מקומי.

---

## 🚀 Quick Start - הוראות הפעלה

### שלב 1: העלאת המפתח הפרטי ל-GitHub Secrets

1. **פתח את Credential Manager על המחשב שלך**
   - לחץ `Win + R` → הקלד `control /name Microsoft.CredentialManager`
   - מצא: `github-app-2251005-private-key`
   - לחץ "Show" → העתק את הערך המלא

2. **העלה ל-GitHub Secrets**
   - עבור ל: https://github.com/edri2or-commits/make-ops-clean/settings/secrets/actions
   - לחץ "New repository secret"
   - **Name**: `GH_APP_PRIVATE_KEY_PEM`
   - **Value**: הדבק את המפתח הפרטי המלא (כולל `-----BEGIN RSA PRIVATE KEY-----` ו-`-----END RSA PRIVATE KEY-----`)
   - לחץ "Add secret"

3. **הוסף את App ID** (אם לא קיים)
   - לחץ "New repository secret"
   - **Name**: `GH_APP_ID`
   - **Value**: `2251005`
   - לחץ "Add secret"

### שלב 2: הרצת הבדיקה (מהענן)

**אופציה א': הפעלה ידנית**
1. עבור ל: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/test-app-auth.yml
2. לחץ "Run workflow"
3. בחר branch: `auth/migration-scaffold`
4. לחץ "Run workflow"

**אופציה ב': טריגר אוטומטי**
- ה-workflow רץ אוטומטית כשיש push לסניף `auth/**`
- או כשמשנים את `auth/test_app_auth.py`

### שלב 3: קבלת תוצאות

1. **צפה בריצה החיה**
   - עבור ל: https://github.com/edri2or-commits/make-ops-clean/actions
   - לחץ על הריצה האחרונה של "Test App Auth (READ-ONLY)"

2. **תוצאות בזמן אמת**
   - לחץ על "test-app-authentication" job
   - צפה בלוג החי של הבדיקה

3. **הורד artifacts**
   - גלול למטה בדף הריצה
   - הורד "app-auth-test-results" (כולל JSON מלא)

---

## 📊 מה הבדיקה בודקת?

### ✅ Step 1: קריאת המפתח הפרטי
- קורא מ-GitHub Secret: `GH_APP_PRIVATE_KEY_PEM`
- מטפל בניו-ליינים מוסתרים (`\n`)
- מאמת שהמפתח בפורמט תקין

### ✅ Step 2: יצירת JWT
- App ID: 2251005
- Algorithm: RS256
- IAT: 60 שניות אחורה (clock skew tolerance)
- EXP: 10 דקות מעכשיו

### ✅ Step 3: יצירת Installation Token
- POST ל-`/app/installations/60358677/access_tokens`
- Lifetime: ~60 דקות
- Permissions: repo-scoped
- Auto-expiry (no manual revocation needed)

### ✅ Step 4: Smoke Tests (READ-ONLY)
- `GET /repos/edri2or-commits/make-ops-clean` - metadata
- `GET /repos/.../issues?state=all&per_page=5` - רשימת issues
- `GET /repos/.../pulls?state=all&per_page=5` - רשימת PRs
- `GET /repos/.../actions/workflows` - רשימת workflows

**⚠️ חשוב**: כל הבדיקות הן READ-ONLY בלבד. אין כתיבה למאגר.

---

## 🔍 פלט צפוי

```
🔐 GitHub App Authentication Test - READ ONLY (Cloud)
============================================================

📋 Configuration:
   App ID: 2251005
   Installation ID: 60358677
   Repository: edri2or-commits/make-ops-clean

📋 Step 1: Reading private key
✅ Reading private key from environment variable (GitHub Secret)
✅ Private key retrieved (length: XXXX chars)

🔑 Step 2: Generating JWT
   Expiry: 10 minutes
✅ JWT generated
   IAT: 2025-11-11T22:10:00 (offset: -60s)
   EXP: 2025-11-11T22:20:00 (10 minutes)

🎫 Step 3: Minting Installation Token
✅ Installation Token minted
   Expires: 2025-11-11T23:10:00Z
   Duration: ~60 minutes
   Permissions: contents, issues, metadata, pull_requests, workflows
   Repositories: make-ops-clean

🧪 Step 4: Smoke Tests (READ-ONLY)

   repo_meta: ✅ ok
      name: make-ops-clean
      private: False
      default_branch: main

   issues: ✅ ok
      count: 5
      sample_titles: [...]

   prs: ✅ ok
      count: 5
      sample_titles: [...]

   workflows: ✅ ok
      count: 65
      sample_names: [...]

============================================================
📊 FINAL REPORT (JSON)
============================================================
{
  "timestamp": "2025-11-11T22:10:00Z",
  "app_id": "2251005",
  "installation_id": "60358677",
  "jwt": {
    "exp_minutes": 10,
    "iat_offset_sec": 60,
    "iat": "2025-11-11T22:09:00",
    "exp": "2025-11-11T22:19:00"
  },
  "installation_token": {
    "expires_in_min": "~60",
    "expires_at": "2025-11-11T23:10:00Z",
    "permissions": ["contents", "issues", "metadata", "pull_requests", "workflows"],
    "repositories": ["make-ops-clean"]
  },
  "smoke": {
    "repo_meta": "✅ ok",
    "issues": "✅ ok",
    "prs": "✅ ok",
    "workflows": "✅ ok"
  },
  "status": "✅ all_tests_passed"
}
```

---

## ⚠️ Troubleshooting

### Error: "Required secrets not configured"
**פתרון**: העלה את ה-secrets (ראה שלב 1 למעלה)

### Error: "JWT generation failed"
**סיבות אפשריות**:
- המפתח לא בפורמט תקין
- יש רווחים מיותרים בתחילת/סוף המפתח
- המפתח לא מתחיל ב-`-----BEGIN RSA PRIVATE KEY-----`

**פתרון**: 
1. העתק שוב את המפתח מ-Credential Manager
2. ודא שאתה מעתיק **הכל** (כולל ה-BEGIN/END headers)
3. עדכן את ה-secret ב-GitHub

### Error: "Installation Token minting failed"
**סיבות אפשריות**:
- App ID לא נכון
- Installation ID לא נכון
- המפתח הפרטי לא תואם ל-App

**פתרון**:
1. ודא App ID = 2251005
2. בדוק שהמפתח הוא של אותו App
3. אמת שה-App מותקן על edri2or-commits/make-ops-clean

---

## 🎯 צעדים הבאים אחרי הצלחה

אם כל הבדיקות עוברות (`status: "✅ all_tests_passed"`):

1. ✅ **Phase 3.1 Complete**: App Auth validation מסומן כהושלם
2. ⏸️ **PAUSE**: ללא כתיבה למאגר עד אישור מפורש
3. 📋 **Or decides**: מאשר מעבר ל-Phase 3.2 (WRITE operations)
4. 🚀 **Next**: MCP cutover + PAT revocation

---

## 🔐 אבטחה

- ✅ המפתח הפרטי מאוחסן רק ב-GitHub Secrets (encrypted)
- ✅ המפתח לא מודפס בלוגים
- ✅ ה-Installation Token פג תוקף אוטומטית ב-~60 דקות
- ✅ כל הבדיקות הן READ-ONLY (no writes)
- ✅ Audit trail מלא ב-GitHub Actions logs

---

## 📚 קבצים רלוונטיים

- `auth/test_app_auth.py` - סקריפט הבדיקה
- `.github/workflows/test-app-auth.yml` - ה-workflow
- `auth/README.md` - תיעוד מלא
- `auth/jwt_wrapper.py` - JWT wrapper (לשימוש עתידי)

---

**Phase**: 3.1 (APP-FLOW - READ-ONLY validation)  
**Status**: Ready for cloud execution  
**Correlation**: PAT-EXPOSURE-20251112  
**Zero-Touch**: Autonomous cloud testing enabled
