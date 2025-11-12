# MCP Remote Setup Guide

## 🎯 מטרה

חיבור **Claude Web** (דפדפן) למערכת ה-MCP שלך, במקביל ל-**Claude Desktop** שכבר עובד.

## 📊 ארכיטקטורה

```
┌─────────────────────────────────────────────────────────┐
│                    קלוד דסקטופ (Local)                    │
│  Claude Desktop → Docker → GitHub MCP → GitHub API      │
│                                       → Google API       │
└─────────────────────────────────────────────────────────┘
                            ✅ פועל!

┌─────────────────────────────────────────────────────────┐
│                    קלוד Web (Remote)                     │
│  Claude Web → Custom Connector → Cloudflare Worker     │
│                                  → GitHub API            │
│                                  → Google API            │
└─────────────────────────────────────────────────────────┘
                      🚧 נבנה עכשיו
```

## 🚀 התקנה מהירה

### דרישות מקדימות

1. **Node.js** (v18+)
2. **Git Bash** (עבור Windows)
3. **Cloudflare Account** עם API Token
4. **GitHub App** מוגדר (יש לך את זה!)

### שלב 1: הכנת הסביבה

```bash
# הגדר את ה-Cloudflare API Token
export CLOUDFLARE_API_TOKEN="your_token_here"
export CF_ACCOUNT_ID="your_account_id"

# Windows CMD:
set CLOUDFLARE_API_TOKEN=your_token_here
set CF_ACCOUNT_ID=your_account_id

# Windows PowerShell:
$env:CLOUDFLARE_API_TOKEN="your_token_here"
$env:CF_ACCOUNT_ID="your_account_id"
```

**איפה למצוא את ה-Cloudflare Account ID?**
1. היכנס ל-[Cloudflare Dashboard](https://dash.cloudflare.com/)
2. בצד ימין תראה את ה-Account ID

### שלב 2: הרצת ההתקנה

**Linux/Mac:**
```bash
cd /path/to/make-ops-clean
chmod +x scripts/setup-mcp-remote.sh
./scripts/setup-mcp-remote.sh
```

**Windows:**
```cmd
cd C:\Users\edri2\Desktop\AI\Ops\claude\MCP\make-ops-clean
scripts\setup-mcp-remote.bat
```

### שלב 3: חיבור ל-Claude Web

אחרי שהסקריפט מסיים, פתח את:
[https://claude.ai](https://claude.ai)

1. לחץ על **Profile** → **Settings**
2. עבור ל-**Integrations** → **Custom Connectors**
3. לחץ **Add custom connector**
4. מלא:
   - **Name**: `GitHub MCP`
   - **URL**: (הסקריפט ישמור את זה ב-`mcp/server/WORKER_URL.txt`)
   - **Type**: MCP Server
   - **Auth**: None

## 🔧 מה הסקריפט עושה?

1. **✅ בדיקת תקינות** - מוודא שכל התלויות מותקנות
2. **🔐 הגדרת Secrets** - מזין את ה-GitHub App credentials ל-Cloudflare
3. **🚀 Deploy** - מעלה את ה-Worker ל-Cloudflare
4. **🔍 בדיקות** - מריץ health checks ו-tool listing
5. **📋 הוראות** - מייצר קובץ הוראות מפורט

## 📁 מבנה קבצים

```
make-ops-clean/
├── mcp/
│   ├── server/
│   │   ├── worker/
│   │   │   ├── src/
│   │   │   │   └── index.ts         # Worker code
│   │   │   └── wrangler.toml        # Cloudflare config
│   │   ├── WORKER_URL.txt           # 🆕 נוצר אוטומטית
│   │   └── CONNECTION_INSTRUCTIONS.md # 🆕 הוראות חיבור
│   └── README.md
└── scripts/
    ├── setup-mcp-remote.sh          # 🆕 Linux/Mac
    └── setup-mcp-remote.bat         # 🆕 Windows
```

## 🛠️ Tools זמינים

אחרי החיבור, תוכל להשתמש ב-5 tools:

1. **github.create_ref** - יצירת branch
2. **github.create_or_update_file** - עריכת קבצים
3. **github.create_pr** - פתיחת Pull Request
4. **github.merge_pr** - מיזוג PR
5. **github.delete_branch** - מחיקת branch

## 🔍 בדיקת תקינות

### בדיקה ידנית:

```bash
# Health check
curl https://your-worker.workers.dev/health

# רשימת tools
curl https://your-worker.workers.dev/tools/list
```

### בדיקה ב-Claude Web:

```
שלום! האם אתה יכול להציג לי את ה-tools הזמינים דרך ה-MCP?
```

התגובה צריכה לכלול 5 tools.

## 🐛 Troubleshooting

### בעיה: "CLOUDFLARE_API_TOKEN not set"
**פתרון**: ודא שהגדרת את המשתנה לפני הרצת הסקריפט.

### בעיה: "wrangler not found"
**פתרון**: הסקריפט יתקין אוטומטית, אבל אפשר להתקין ידנית:
```bash
npm install -g wrangler@3
```

### בעיה: "Private key missing"
**פתרון**: הסקריפט יבקש ממך להזין את ה-private key. תוכל למצוא אותו ב:
```
Windows Credential Manager → github-app-2251005-privatekey
```

או ב:
```
C:\Users\edri2\Desktop\AI\Ops\claude\_audit\purged_2025-11-11\key.pem
```

### בעיה: Worker לא מגיב
**פתרון**: בדוק logs:
```bash
cd mcp/server/worker
wrangler tail
```

## 🔄 עדכון

כדי לעדכן את ה-worker:

```bash
cd mcp/server/worker
wrangler deploy
```

או הרץ שוב את הסקריפט:
```bash
scripts/setup-mcp-remote.sh
```

## 🔐 אבטחה

- ✅ Secrets מאוחסנים ב-Cloudflare Workers (לא ב-repo)
- ✅ GitHub App authentication (not PAT)
- ✅ Least-privilege scopes
- ✅ Private key ב-Windows Credential Manager

## 📚 מידע נוסף

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [GitHub Apps Authentication](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app)
- [MCP Protocol](https://modelcontextprotocol.com/)

## 💡 טיפים

1. **Desktop vs Web**: שני הסביבות מחוברות לאותו GitHub App, אז שינויים שאתה עושה ב-Desktop ייראו גם ב-Web.

2. **Secrets Rotation**: אם תרצה להחליף את ה-Private Key:
   ```bash
   cd mcp/server/worker
   wrangler secret put PRIVATE_KEY
   ```

3. **Multiple Environments**: אפשר ליצור workers נפרדים ל-dev/staging/prod ע"י שינוי `wrangler.toml`.

## 🎯 הבא

אחרי שהכל עובד:
- [ ] הוסף Google API support
- [ ] הוסף Telegram notifications
- [ ] הוסף monitoring dashboard
- [ ] הוסף rate limiting

---

**נוצר ע"י**: Claude + Or Edri  
**עדכון אחרון**: 2025-11-12  
**סטטוס**: ✅ Ready for deployment
