# HI Maven Project - GitHub Deployment Guide

## 📦 Project Package

**Location:** `C:\Users\wwang\Documents\sql-server-connection.zip` (2.11 MB)

**Includes:**
- Complete PowerShell scripts (query, connect, export, deploy)
- Python parser (hi_maven_parser.py)
- CSV exports (FieldMetadata.csv 0.69 MB, ValueMetadata.csv 8.77 MB)
- Complete documentation (DATABASE_DOCUMENTATION.md, PARSER_USAGE.md, README.md)
- Deployment scripts (push-to-github.ps1, deploy-github.ps1)
- .gitignore for version control

---

## 🚀 Deploy to GitHub (3 Simple Steps)

### Step 1: Get Your GitHub Token
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Name:** HI-Maven-Upload
4. **Expiration:** No expiration (or choose your preference)
5. **Scope:** Check **"repo"** (Full control of private repositories)
6. Click **"Generate token"** at bottom
7. **Copy the token** (appears once - save it!)

⚠️ **Keep this token private!** Treat it like a password.

### Step 2: Run PowerShell Deployment Script
```powershell
cd C:\Users\wwang\Documents\sql-server-connection

# Replace YOUR_TOKEN with your actual token from Step 1
.\push-to-github.ps1 -GithubToken "ghp_YOUR_TOKEN_HERE" -Owner "wwinductive" -RepoName "hi-maven-sql-server"
```

**What it does:**
- Creates GitHub repo: `wwinductive/hi-maven-sql-server`
- Uploads all files via GitHub REST API
- No Git installation needed
- Shows progress for each file

### Step 3: Verify
- Visit: https://github.com/wwinductive/hi-maven-sql-server
- All files should be there!

---

## 🔧 Alternative: Using Git Locally

**If you prefer manual git workflow:**

```powershell
# 1. Install Git from https://git-scm.com/download/win (if needed)

# 2. Navigate and initialize
cd C:\Users\wwang\Documents\sql-server-connection
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Create repo on GitHub first:
#    Go to https://github.com/new
#    Owner: wwinductive
#    Repo name: hi-maven-sql-server
#    Click "Create repository"

# 4. Add remote and push
git remote add origin https://github.com/wwinductive/hi-maven-sql-server.git
git branch -M main
git add .
git commit -m "Initial commit: HI Maven SQL Server connection and parser"
git push -u origin main

# When prompted for password: Use your GitHub token as the password
```

---

## 📋 Project Contents Summary

### Documentation (Ready to Read)
- **DATABASE_DOCUMENTATION.md** - Complete schema, 50+ SQL queries, integration patterns
- **PARSER_USAGE.md** - Python parser API with 5+ usage examples
- **README.md** - Quick start guide, module mapping, feature overview

### Data Exports (Ready to Use)
- **FieldMetadata.csv** - 7,692 fields from 10 source tables
- **ValueMetadata.csv** - 171,671 codes across 2,238 value sets

### PowerShell Tools (Ready to Run)
- **query.ps1** - Main reusable SQL query function
- **connect.ps1** - Test database connection
- **metadata-info.ps1** - Inspect table structures
- **export-scope.ps1** - Run all sizing queries
- **export-values.ps1** - Export ValueMetadata to CSV

### Python Tools (Ready After Installation)
- **hi_maven_parser.py** - Parse CSVs into standardized Question objects
- Includes: filtering, exporting to JSON/CSV, schema reference

### Deployment Scripts (Ready to Use)
- **push-to-github.ps1** - Upload to GitHub via REST API ← **Use this one**
- **deploy-github.ps1** - Alternative Git-based deployment

---

## 🎯 What You Get After Deployment

✅ **Public GitHub Repository** at https://github.com/wwinductive/hi-maven-sql-server  
✅ **Full Source Control** - Track changes, collaborate with team  
✅ **Documentation** - Accessible to anyone  
✅ **Data Exports** - Ready for workbench ingestion  
✅ **Tools** - PowerShell scripts, Python parser, deployment guides  

---

## 📊 Project Statistics

- **7,692 fields** from HI Maven database
- **171,671 codes** in value sets
- **2,238 value sets** total
- **10 source tables** (GeneralModel, HepModel, STDModel, LeadModel, ids_* tables)
- **0% gaps** - Complete value sets (unlike ND Pages.xlsx)

---

## ⚡ Quick Reference

| Task | Command |
|------|---------|
| **Deploy to GitHub** | `.\push-to-github.ps1 -GithubToken "YOUR_TOKEN"` |
| **Query Database** | `. .\query.ps1` then `Query-SqlServer -Query "SELECT ..." -Database "ihi-hi"` |
| **Generate JSON** | `python hi_maven_parser.py` |
| **View Help** | `Get-Help Query-SqlServer` |

---

## ✅ Deployment Readiness Checklist

- [x] SQL Server connection established ✓
- [x] Data exported to CSV ✓
- [x] Documentation complete ✓
- [x] Python parser created ✓
- [x] PowerShell scripts tested ✓
- [x] Deployment script ready ✓
- [x] Zip archive created ✓
- [ ] Push to GitHub (use Step 1-3 above)

**You're ready to deploy!** Just get your GitHub token and run the script.

---

## 🆘 Troubleshooting

### "Token invalid" or "401 Unauthorized"
- Double-check your token has "repo" scope
- Make sure you copied the full token (including "ghp_" prefix)
- Regenerate if needed: https://github.com/settings/tokens

### "Repository already exists"
- Script will detect and use existing repo
- Files will be updated if they already exist

### "PowerShell execution policy" error
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try again

### "File not found"
- Make sure you're in the correct directory
- Run from: `C:\Users\wwang\Documents\sql-server-connection`

---

## 📞 Success Indicator

When deployment succeeds, you'll see:
```
========================================
   GitHub Repository Uploader
========================================

[1/3] Creating GitHub Repository...
✓ Repository already exists: wwinductive/hi-maven-sql-server

[2/3] Collecting files...

[3/3] Uploading files...
  ✓ DATABASE_DOCUMENTATION.md (145 KB)
  ✓ FieldMetadata.csv (690 KB)
  ✓ ValueMetadata.csv (8.8 MB)
  ... (more files)

========================================
✓ Upload Complete!
========================================
Repository: https://github.com/wwinductive/hi-maven-sql-server
Files uploaded: 14
```

---

**Ready? Get your GitHub token and run the deployment script!**
