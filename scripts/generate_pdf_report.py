#!/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3
"""
GEO PDF Report Generator using Playwright Chromium.
Renders GEO-AUDIT-REPORT.md into a client-ready styled PDF.
"""
import sys
import os
from pathlib import Path

def main():
    cwd = Path(os.getcwd())
    md_path = cwd / "GEO-AUDIT-REPORT.md"
    html_path = cwd / "GEO-AUDIT-REPORT.html"
    pdf_path = cwd / "GEO-AUDIT-REPORT.pdf"

    if not md_path.exists():
        print(f"Error: {md_path} not found. Run /geo audit <url> first.", file=sys.stderr)
        sys.exit(1)

    try:
        from markdown_it import MarkdownIt
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    md = MarkdownIt()
    body_html = md.render(md_content)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GEO Audit Report</title>
<style>
  @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap");
  
  @page {{
    margin: 15mm;
    size: A4;
  }}

  body {{
    font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background: #ffffff;
  }}
  h1, h2, h3, h4 {{
    font-family: "Space Grotesk", sans-serif;
    color: #0f172a;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
  }}
  h1 {{
    font-size: 24pt;
    border-bottom: 3px solid #6366f1;
    padding-bottom: 8px;
    color: #0f172a;
  }}
  h2 {{
    font-size: 16pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    color: #1e293b;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 13pt;
    color: #334155;
    page-break-after: avoid;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    font-size: 10pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 9px 12px;
    text-align: left;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  blockquote {{
    border-left: 4px solid #6366f1;
    background: #f8fafc;
    margin: 1.2em 0;
    padding: 10px 16px;
    color: #475569;
    border-radius: 0 8px 8px 0;
  }}
  hr {{
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 2em 0;
  }}
  code {{
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    color: #0f172a;
    font-family: monospace;
  }}
  ul, ol {{
    padding-left: 22px;
  }}
  li {{
    margin-bottom: 5px;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle")
        page.pdf(path=str(pdf_path), format="A4", print_background=True, margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"})
        browser.close()

    print(f"Successfully generated PDF report: {pdf_path}")

if __name__ == "__main__":
    main()
