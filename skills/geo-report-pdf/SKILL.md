---
name: geo-report-pdf
description: Generate a publication-grade, multi-page executive PDF report from a GEO + SEO audit. Automatically executes dual-engine audit orchestrator, organizes client folder, and registers in AUDIT-INDEX.md.
version: 2.1.0
author: geo-seo-antigravity
tags: [geo, pdf, report, client-deliverable, professional, semrush-alternative]
allowed-tools: Read, Grep, Glob, Bash, Write
---

# GEO Executive PDF Report Generator

## ⚡ Execution Rule for AI Assistant (CRITICAL)

When the user invokes `/geo report-pdf <url> [client_name]` or `/geo-report-pdf <url>`:
**NEVER** ask the user to run raw Python or bash commands in the chat.
YOU MUST automatically execute the Dual-Engine Audit Orchestrator:

```bash
/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3 /Users/shivpratap/.gemini/config/skills/geo/scripts/audit_orchestrator.py "<url>" "<client_name>"
```

### What This Produces Automatically:
1. **Client Directory**: `Audits/<domain>/`
2. **Standardized PDF**: `GEO-Report-<domain>-<YYYY-MM-DD>.pdf` (500-600 KB, 4-page executive A4 layout)
3. **Instant Desktop Mirror**: `/Users/shivpratap/Desktop/GEO-Report-<domain>-<date>.pdf`
4. **Master Registry Entry**: Updated in `Audits/AUDIT-INDEX.md` and `Audits/audit-index.json`

### 4-Page PDF Document Structure:
- **Page 1 (Cover Page)**: Dark navy full-bleed cover with score gauge, metadata table, URL, and executive statement.
- **Page 2 (Executive Scorecard)**: Dual KPI comparison (GEO AI Visibility vs. Technical Health), error/warning counters, and category progress bars.
- **Page 3 (Actionable Findings & Technical Issues)**: Severity-coded cards (High, Medium, Low) highlighting specific code and content improvements.
- **Page 4 (30-Day Execution Roadmap & Sign-Off)**: Four structured phases (Foundation, Knowledge Graph, Citability, Authority) with an agency/client sign-off box.
