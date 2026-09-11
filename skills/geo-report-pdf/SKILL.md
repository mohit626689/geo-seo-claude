---
name: geo-report-pdf
description: Generate a publication-grade, multi-page executive PDF report from a GEO + SEO audit. Includes dual-engine scoring (GEO Citability + Semrush-grade Technical Health), structured client folder storage, standardized naming (GEO-Report-[domain]-[date].pdf), and master audit index registry tracking.
version: 2.1.0
author: geo-seo-antigravity
tags: [geo, pdf, report, client-deliverable, professional, semrush-alternative]
allowed-tools: Read, Grep, Glob, Bash, Write
---

# GEO Executive PDF Report Generator (Dual-Engine Pipeline)

## Overview

The GEO PDF Report pipeline generates high-converting, professional executive audit deliverables. It integrates two powerful engines:
1. **GEO AI Visibility Engine**: AI citability, llms.txt compliance, crawlers access, schema discoverability, and brand authority.
2. **Semrush Alternative Technical Engine (`seo_auditor.py`)**: Crawl health, HTTP status, SSL, security headers (HSTS, CSP, X-Frame), meta tag length/completeness, headings hierarchy, image alt coverage, text-to-HTML ratio, and Core Web Vitals readiness.

## Deliverable Organization & Standardization

Every generated audit is automatically organized:
- **Client Audit Directory**: `Audits/<domain>/`
- **Standardized PDF Name**: `GEO-Report-<domain>-<YYYY-MM-DD>.pdf`
- **Client Markdown & HTML**: `GEO-Audit-<domain>-<date>.md` & `GEO-Report-<domain>-<date>.html`
- **Desktop Instant Access**: Mirrored to `/Users/shivpratap/Desktop/GEO-Report-<domain>-<date>.pdf` for one-click sharing
- **Central Master Registry**: Recorded in `Audits/AUDIT-INDEX.md` and `Audits/audit-index.json`

---

## How To Run

### One-Command Full Audit & PDF Generation
To run the automated audit, generate the multi-page PDF, and register it in the master index:

```bash
/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3 \
  ~/.gemini/config/skills/geo/scripts/audit_orchestrator.py "<target_url>" "<brand_name>"
```

### Standalone Semrush-Alternative Technical Audit
To run just the free technical audit engine:

```bash
/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3 \
  ~/.gemini/config/skills/geo/scripts/seo_auditor.py "<target_url>"
```

---

## 4-Page PDF Document Structure

The generated PDF strictly avoids fragmented styling through explicit A4 page breaks (`page-break-before: always;`):

1. **Page 1: Executive Cover Page**
   - Premium dark navy gradient (`#0b132b` to `#1c2541`)
   - Large Circular Score Gauge & Status Pill
   - Target URL, Client Brand Name, Audit Date, Business Type, and Platform
   - High-trust confidentiality badge and executive summary statement

2. **Page 2: Executive Scorecard & Category Breakdown**
   - Dual KPI Cards: Overall GEO Citability Score vs. Technical Health Score (Semrush Metric)
   - Issue Severity Counter (Critical Errors, Warnings, Notices)
   - Category Breakdown Table with visual colored progress indicators (AI Citability, Crawler Access, Schema, Technical Foundation, Content E-E-A-T)

3. **Page 3: Actionable Findings & Technical Issues**
   - High Priority Callouts (red left-border card)
   - Medium Priority Callouts (amber left-border card)
   - Low Priority & Advisory Notices (blue left-border card)
   - Semrush-comparable technical issues (SSL, missing headers, robots directives, image alts)

4. **Page 4: 30-Day Execution Roadmap & Client Sign-Off**
   - Phase 1 (Days 1–7): Immediate Technical Foundation & Crawler Access
   - Phase 2 (Days 8–14): Knowledge Graph & Structured Data (JSON-LD)
   - Phase 3 (Days 15–21): AI Citability & Content Restructuring
   - Phase 4 (Days 22–30): Brand Mentions & AI Engine Tracking
   - Formal Agency/Client Sign-off Block

---

## Master Index Registry (`AUDIT-INDEX.md`)

Whenever an audit is generated, it automatically registers in:
`/Users/shivpratap/Desktop/Shiv Second Brain/Audits/AUDIT-INDEX.md`
