#!/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3
"""
Free Semrush Alternative: Technical & On-Page SEO Auditor.
Performs comprehensive technical, on-page, and AI readiness auditing.
Computes Semrush-style Site Health (0-100%), Errors, Warnings, and Notices.
"""
import sys
import json
import time
import ssl
import socket
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def audit_url(url):
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urllib.parse.urlparse(url)

    domain = parsed.netloc
    results = {
        "url": url,
        "domain": domain,
        "audit_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "site_health": 100,
        "errors_count": 0,
        "warnings_count": 0,
        "notices_count": 0,
        "issues": {
            "errors": [],
            "warnings": [],
            "notices": []
        },
        "technical": {},
        "on_page": {},
        "ai_readiness": {},
        "schema": {}
    }

    # 1. Fetch Homepage & Measure Performance
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (Antigravity-SEOBot/2.0)"
    }
    req = urllib.request.Request(url, headers=headers)
    
    html_content = ""
    status_code = 0
    resp_headers = {}
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            status_code = resp.getcode()
            resp_headers = dict(resp.info())
            html_content = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        status_code = e.code
        results["issues"]["errors"].append(f"Server returned HTTP error status: {e.code}")
    except URLError as e:
        results["issues"]["errors"].append(f"Connection failed: {e.reason}")
    except Exception as e:
        results["issues"]["errors"].append(f"Fetch failed: {str(e)}")

    response_time_ms = round((time.time() - start_time) * 1000)
    results["technical"]["status_code"] = status_code
    results["technical"]["response_time_ms"] = response_time_ms

    if response_time_ms > 1500:
        results["issues"]["warnings"].append(f"Slow response time: {response_time_ms}ms (Target: < 800ms)")
    elif response_time_ms > 2500:
        results["issues"]["errors"].append(f"Very slow server response time: {response_time_ms}ms")

    # 2. SSL & Security Headers Audit
    is_https = parsed.scheme == "https"
    results["technical"]["https"] = is_https
    if not is_https:
        results["issues"]["errors"].append("Website does not enforce HTTPS")

    sec_headers = {
        "Strict-Transport-Security": resp_headers.get("strict-transport-security") or resp_headers.get("Strict-Transport-Security"),
        "Content-Security-Policy": resp_headers.get("content-security-policy") or resp_headers.get("Content-Security-Policy"),
        "X-Frame-Options": resp_headers.get("x-frame-options") or resp_headers.get("X-Frame-Options"),
        "X-Content-Type-Options": resp_headers.get("x-content-type-options") or resp_headers.get("X-Content-Type-Options"),
        "Referrer-Policy": resp_headers.get("referrer-policy") or resp_headers.get("Referrer-Policy"),
    }
    results["technical"]["security_headers"] = sec_headers

    if not sec_headers["Strict-Transport-Security"]:
        results["issues"]["warnings"].append("Missing HSTS (Strict-Transport-Security) header")
    if not sec_headers["X-Content-Type-Options"]:
        results["issues"]["notices"].append("Missing X-Content-Type-Options: nosniff header")
    if not sec_headers["X-Frame-Options"] and not sec_headers["Content-Security-Policy"]:
        results["issues"]["warnings"].append("Missing clickjacking protection (X-Frame-Options or CSP)")

    # 3. Subdomain Check
    if ".lovable.app" in domain or ".vercel.app" in domain or ".netlify.app" in domain or ".webflow.io" in domain:
        results["technical"]["is_subdomain"] = True
        results["issues"]["warnings"].append(f"Hosted on platform subdomain ({domain}). Missing custom root domain (e.g. yourbrand.com)")
    else:
        results["technical"]["is_subdomain"] = False

    # 4. Robots.txt & AI Crawlers Audit
    robots_url = f"{parsed.scheme}://{domain}/robots.txt"
    robots_content = ""
    try:
        r_req = urllib.request.Request(robots_url, headers=headers)
        with urllib.request.urlopen(r_req, timeout=10) as r_resp:
            if r_resp.getcode() == 200:
                robots_content = r_resp.read().decode("utf-8", errors="replace")
    except Exception:
        pass

    results["technical"]["robots_txt_exists"] = bool(robots_content)
    if not robots_content:
        results["issues"]["warnings"].append("Missing robots.txt file")
    else:
        # Check AI bots
        ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
        blocked_bots = []
        allowed_bots = []
        for bot in ai_bots:
            if f"User-agent: {bot}" in robots_content and "Disallow: /" in robots_content:
                blocked_bots.append(bot)
            elif f"User-agent: {bot}" in robots_content and "Allow: /" in robots_content:
                allowed_bots.append(bot)

        results["ai_readiness"]["blocked_ai_bots"] = blocked_bots
        results["ai_readiness"]["explicit_allowed_ai_bots"] = allowed_bots
        if blocked_bots:
            results["issues"]["errors"].append(f"AI crawlers explicitly blocked in robots.txt: {', '.join(blocked_bots)}")
        elif not allowed_bots:
            results["issues"]["notices"].append("robots.txt uses generic wildcard rules; missing explicit AI bot allow directives")

    # 5. Sitemap & LLMS.txt Audit
    sitemap_url = f"{parsed.scheme}://{domain}/sitemap.xml"
    sitemap_exists = False
    try:
        sm_req = urllib.request.Request(sitemap_url, headers=headers)
        with urllib.request.urlopen(sm_req, timeout=10) as sm_resp:
            if sm_resp.getcode() == 200:
                sitemap_exists = True
    except Exception:
        pass
    results["technical"]["sitemap_exists"] = sitemap_exists
    if not sitemap_exists:
        results["issues"]["warnings"].append("Missing or inaccessible sitemap.xml")

    llmstxt_url = f"{parsed.scheme}://{domain}/llms.txt"
    llmstxt_exists = False
    try:
        llm_req = urllib.request.Request(llmstxt_url, headers=headers)
        with urllib.request.urlopen(llm_req, timeout=10) as llm_resp:
            if llm_resp.getcode() == 200:
                llmstxt_exists = True
    except Exception:
        pass
    results["ai_readiness"]["llms_txt_exists"] = llmstxt_exists
    if not llmstxt_exists:
        results["issues"]["warnings"].append("Missing llms.txt standard file for AI answer engines")

    # 6. On-Page HTML Analysis
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")

        # Title
        title_tag = soup.title.string if soup.title else ""
        title_len = len(title_tag) if title_tag else 0
        results["on_page"]["title"] = title_tag
        results["on_page"]["title_length"] = title_len

        if not title_tag:
            results["issues"]["errors"].append("Missing <title> tag on page")
        elif title_len < 30:
            results["issues"]["warnings"].append(f"Title tag is too short ({title_len} characters, optimal: 50-60)")
        elif title_len > 65:
            results["issues"]["notices"].append(f"Title tag may be truncated in search results ({title_len} characters)")

        # Meta Description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc_content = meta_desc.get("content", "") if meta_desc else ""
        desc_len = len(desc_content) if desc_content else 0
        results["on_page"]["meta_description"] = desc_content
        results["on_page"]["description_length"] = desc_len

        if not desc_content:
            results["issues"]["errors"].append("Missing meta description tag")
        elif desc_len < 70:
            results["issues"]["warnings"].append(f"Meta description is too short ({desc_len} characters, optimal: 120-160)")
        elif desc_len > 170:
            results["issues"]["notices"].append(f"Meta description is long ({desc_len} characters, may truncate)")

        # Headings
        h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]
        results["on_page"]["h1_count"] = len(h1_tags)
        results["on_page"]["h1_list"] = h1_tags
        if len(h1_tags) == 0:
            results["issues"]["errors"].append("Page is missing an <h1> heading tag")
        elif len(h1_tags) > 1:
            results["issues"]["warnings"].append(f"Multiple <h1> tags detected ({len(h1_tags)} found, best practice: exactly 1)")

        # Canonical Tag
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical_href = canonical_tag.get("href", "") if canonical_tag else ""
        results["on_page"]["canonical"] = canonical_href
        if not canonical_href:
            results["issues"]["warnings"].append("Missing canonical tag (<link rel='canonical'>)")

        # Images & Alt Attributes
        images = soup.find_all("img")
        missing_alt = [img.get("src") for img in images if not img.get("alt")]
        results["on_page"]["total_images"] = len(images)
        results["on_page"]["images_missing_alt"] = len(missing_alt)
        if missing_alt:
            results["issues"]["warnings"].append(f"{len(missing_alt)} image(s) missing alt text")

        # Schema.org Structured Data (extract BEFORE decomposing scripts)
        schemas = []
        for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
            try:
                data = json.loads(s.string)
                if isinstance(data, list):
                    schemas.extend(data)
                elif isinstance(data, dict):
                    schemas.append(data)
            except Exception:
                pass

        schema_types = [s.get("@type") for s in schemas if isinstance(s, dict) and "@type" in s]
        results["schema"]["types_detected"] = schema_types
        if not schemas:
            results["issues"]["errors"].append("Missing Schema.org structured data (JSON-LD)")

        # Word Count & Text-to-HTML Ratio
        for script in soup(["script", "style", "svg", "noscript"]):
            script.decompose()
        text = soup.get_text(separator=" ", strip=True)
        words = text.split()
        word_count = len(words)
        results["on_page"]["word_count"] = word_count

        text_bytes = len(text.encode("utf-8"))
        html_bytes = len(html_content.encode("utf-8"))
        ratio = round((text_bytes / max(html_bytes, 1)) * 100, 1)
        results["on_page"]["text_to_html_ratio"] = f"{ratio}%"

        if word_count < 250:
            results["issues"]["warnings"].append(f"Thin content: Page has only {word_count} words (minimum recommended: 350+)")
        if ratio < 10:
            results["issues"]["notices"].append(f"Low text-to-HTML ratio ({ratio}%). Heavy code/scripts relative to content.")

    # Compute Site Health Score (Semrush scale 0-100%)
    # Errors deduct 6 points, Warnings deduct 2 points, Notices deduct 0.5 points
    err_count = len(results["issues"]["errors"])
    warn_count = len(results["issues"]["warnings"])
    not_count = len(results["issues"]["notices"])

    results["errors_count"] = err_count
    results["warnings_count"] = warn_count
    results["notices_count"] = not_count

    penalty = (err_count * 6) + (warn_count * 2) + (not_count * 0.5)
    health = max(round(100 - penalty), 10)
    results["site_health"] = health

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 seo_auditor.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    data = audit_url(url)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
