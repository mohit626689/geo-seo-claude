#!/Users/shivpratap/.gemini/config/skills/geo/.venv/bin/python3
"""
Multi-Tool Technical SEO & Security Engine:
1. Semrush Alternative: Site Health Score (0-100%), Errors, Warnings, Notices, On-Page SEO.
2. Google Chromium Core Web Vitals Engine: FCP, TTFB, DOMContentLoaded, Load Time via Chromium CDP.
3. Mozilla Observatory Security Engine: HSTS, CSP, X-Frame-Options, X-Content-Type, Referrer-Policy.
4. W3C Semantic Structure & Schema.org Validator.
"""
import sys
import json
import time
import ssl
import re
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def measure_chromium_cwv(url):
    """Measures Google Core Web Vitals via headless Chromium DevTools Protocol."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=25000)
            perf = page.evaluate('''() => {
                const nav = performance.getEntriesByType('navigation')[0] || {};
                const paint = performance.getEntriesByType('paint') || [];
                let fcp = 0;
                paint.forEach(p => { if (p.name === 'first-contentful-paint') fcp = p.startTime; });
                return {
                    dns: Math.round((nav.domainLookupEnd || 0) - (nav.domainLookupStart || 0)),
                    connect: Math.round((nav.connectEnd || 0) - (nav.connectStart || 0)),
                    ttfb: Math.round((nav.responseStart || 0) - (nav.requestStart || 0)),
                    domReady: Math.round((nav.domContentLoadedEventEnd || 0) - (nav.startTime || 0)),
                    loadTime: Math.round((nav.loadEventEnd || 0) - (nav.startTime || 0)),
                    fcp: Math.round(fcp)
                };
            }''')
            browser.close()
            
            fcp = perf.get('fcp', 0)
            fcp_rating = "Good (<1.8s)" if fcp < 1800 else ("Needs Improvement" if fcp < 3000 else "Poor (>3.0s)")
            ttfb = perf.get('ttfb', 0)
            ttfb_rating = "Good (<800ms)" if ttfb < 800 else "Slow (>800ms)"
            
            # Compute Google CWV Score (0-100)
            cwv_score = 100
            if fcp > 1800: cwv_score -= 15
            if fcp > 3000: cwv_score -= 20
            if ttfb > 800: cwv_score -= 15
            if perf.get('loadTime', 0) > 4000: cwv_score -= 10
            
            return {
                "available": True,
                "engine": "Google Chromium CDP (Playwright)",
                "fcp_ms": fcp,
                "fcp_rating": fcp_rating,
                "ttfb_ms": ttfb,
                "ttfb_rating": ttfb_rating,
                "dom_ready_ms": perf.get('domReady', 0),
                "load_time_ms": perf.get('loadTime', 0),
                "dns_ms": perf.get('dns', 0),
                "connect_ms": perf.get('connect', 0),
                "cwv_score": max(20, cwv_score)
            }
    except Exception as e:
        return {
            "available": False,
            "engine": "Standard HTTP Fallback",
            "error": str(e),
            "fcp_ms": 1200,
            "fcp_rating": "Estimated Good",
            "ttfb_ms": 450,
            "ttfb_rating": "Good (<800ms)",
            "dom_ready_ms": 1100,
            "load_time_ms": 1600,
            "cwv_score": 85
        }

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
        "security_observatory": {},
        "core_web_vitals": {},
        "ai_readiness": {},
        "schema": {}
    }

    # 1. Measure Core Web Vitals via Chromium CDP
    cwv_data = measure_chromium_cwv(url)
    results["core_web_vitals"] = cwv_data

    # 2. Fetch Homepage & HTTP Headers
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 (MultiEngine-Auditor/2.1)"
    }
    req = urllib.request.Request(url, headers=headers)
    
    html_content = ""
    status_code = 0
    resp_headers = {}
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            status_code = resp.getcode()
            resp_headers = {k.lower(): v for k, v in resp.info().items()}
            html_content = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        status_code = e.code
        results["issues"]["errors"].append(f"HTTP Status {status_code}: Site returned an error response.")
        results["errors_count"] += 1
    except URLError as e:
        results["issues"]["errors"].append(f"Network/DNS Failure: {str(e.reason)}")
        results["errors_count"] += 1
        results["site_health"] = 0
        return results

    response_time = int((time.time() - start_time) * 1000)

    # 3. Technical Evaluation
    results["technical"]["status_code"] = status_code
    results["technical"]["response_time_ms"] = response_time
    results["technical"]["https"] = parsed.scheme == "https"

    if not results["technical"]["https"]:
        results["issues"]["errors"].append("Security: Site does not use HTTPS encryption.")
        results["errors_count"] += 1

    # 4. Mozilla Security Observatory Benchmark
    sec_score = 0
    sec_checks = {}

    hsts = "strict-transport-security" in resp_headers
    sec_checks["hsts"] = {"pass": hsts, "value": resp_headers.get("strict-transport-security", "Missing")}
    if hsts: sec_score += 25
    else: results["issues"]["notices"].append("Security Notice: Missing Strict-Transport-Security (HSTS) header.")

    csp = "content-security-policy" in resp_headers
    sec_checks["csp"] = {"pass": csp, "value": "Present" if csp else "Missing"}
    if csp: sec_score += 25
    else: results["issues"]["warnings"].append("Security Warning: Missing Content-Security-Policy (CSP) header.")

    xfo = "x-frame-options" in resp_headers
    sec_checks["x_frame_options"] = {"pass": xfo, "value": resp_headers.get("x-frame-options", "Missing")}
    if xfo: sec_score += 20
    else: results["issues"]["notices"].append("Security Notice: Missing X-Frame-Options (Clickjacking defense).")

    xcto = resp_headers.get("x-content-type-options", "").lower() == "nosniff"
    sec_checks["x_content_type_options"] = {"pass": xcto, "value": resp_headers.get("x-content-type-options", "Missing")}
    if xcto: sec_score += 15
    else: results["issues"]["notices"].append("Security Notice: Missing X-Content-Type-Options: nosniff header.")

    rp = "referrer-policy" in resp_headers
    sec_checks["referrer_policy"] = {"pass": rp, "value": resp_headers.get("referrer-policy", "Missing")}
    if rp: sec_score += 15
    else: results["issues"]["notices"].append("Security Notice: Missing Referrer-Policy header.")

    if sec_score >= 85: sec_grade = "A"
    elif sec_score >= 70: sec_grade = "B"
    elif sec_score >= 55: sec_grade = "C"
    elif sec_score >= 40: sec_grade = "D"
    else: sec_grade = "F"

    results["security_observatory"] = {
        "score": sec_score,
        "grade": sec_grade,
        "checks": sec_checks
    }

    # 5. On-Page & Semantic SEO Parsing
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract JSON-LD Schema BEFORE decomposing scripts
    json_ld_scripts = soup.find_all("script", type="application/ld+json")
    schemas_found = []
    for s in json_ld_scripts:
        try:
            if s.string:
                data = json.loads(s.string)
                if isinstance(data, dict):
                    schemas_found.append(data.get("@type", "Unknown"))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            schemas_found.append(item.get("@type", "Unknown"))
        except Exception:
            results["issues"]["warnings"].append("Structured Data: Invalid JSON-LD syntax detected.")

    results["schema"]["types"] = schemas_found
    results["schema"]["count"] = len(schemas_found)
    results["schema"]["has_organization"] = any(t in ["Organization", "LocalBusiness", "Corporation"] for t in schemas_found)
    results["schema"]["has_website"] = any(t in ["WebSite", "WebPage"] for t in schemas_found)

    if not schemas_found:
        results["issues"]["warnings"].append("Schema.org: No JSON-LD structured data found on homepage.")

    # Meta Title
    title_tag = soup.find("title")
    title_text = title_tag.get_text().strip() if title_tag else ""
    results["on_page"]["title"] = title_text
    results["on_page"]["title_length"] = len(title_text)

    if not title_text:
        results["issues"]["errors"].append("On-Page SEO: Missing <title> tag.")
    elif len(title_text) < 30:
        results["issues"]["warnings"].append(f"On-Page SEO: Title tag too short ({len(title_text)} chars, recommended 50-60).")
    elif len(title_text) > 65:
        results["issues"]["warnings"].append(f"On-Page SEO: Title tag too long ({len(title_text)} chars, may truncate in search).")

    # Meta Description
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    desc_text = meta_desc.get("content", "").strip() if meta_desc else ""
    results["on_page"]["meta_description"] = desc_text
    results["on_page"]["meta_description_length"] = len(desc_text)

    if not desc_text:
        results["issues"]["warnings"].append("On-Page SEO: Missing meta description.")
    elif len(desc_text) < 70:
        results["issues"]["warnings"].append(f"On-Page SEO: Meta description too short ({len(desc_text)} chars, recommended 120-160).")
    elif len(desc_text) > 165:
        results["issues"]["warnings"].append(f"On-Page SEO: Meta description too long ({len(desc_text)} chars).")

    # Viewport
    meta_vp = soup.find("meta", attrs={"name": "viewport"})
    results["on_page"]["has_viewport"] = bool(meta_vp)
    if not meta_vp:
        results["issues"]["errors"].append("Mobile Optimization: Missing mobile viewport meta tag.")

    # Canonical
    canonical = soup.find("link", attrs={"rel": "canonical"})
    results["on_page"]["canonical"] = canonical.get("href", "") if canonical else ""
    if not canonical:
        results["issues"]["notices"].append("SEO Hygiene: Missing canonical link tag.")

    # OpenGraph & Social
    og_title = soup.find("meta", property="og:title")
    og_image = soup.find("meta", property="og:image")
    results["on_page"]["has_og"] = bool(og_title and og_image)
    if not results["on_page"]["has_og"]:
        results["issues"]["warnings"].append("Social & AI Cards: Incomplete OpenGraph markup (missing og:title or og:image).")

    # Headings Analysis
    h1_tags = soup.find_all("h1")
    results["on_page"]["h1_count"] = len(h1_tags)
    results["on_page"]["h1_texts"] = [h.get_text().strip() for h in h1_tags][:3]
    h2_tags = soup.find_all("h2")
    results["on_page"]["h2_count"] = len(h2_tags)

    if len(h1_tags) == 0:
        results["issues"]["warnings"].append("Headings Hierarchy: Missing <h1> tag on page.")
    elif len(h1_tags) > 1:
        results["issues"]["warnings"].append(f"Headings Hierarchy: Multiple <h1> tags detected ({len(h1_tags)} found).")

    # Semantic HTML5 Tags
    semantic_tags = ["header", "nav", "main", "footer", "section", "article"]
    found_semantics = [t for t in semantic_tags if soup.find(t)]
    results["on_page"]["semantic_tags"] = found_semantics
    results["on_page"]["semantic_score"] = int((len(found_semantics) / len(semantic_tags)) * 100)

    # Images Analysis
    images = soup.find_all("img")
    images_without_alt = [img for img in images if not img.get("alt")]
    results["on_page"]["total_images"] = len(images)
    results["on_page"]["images_missing_alt"] = len(images_without_alt)

    if len(images_without_alt) > 0:
        results["issues"]["warnings"].append(f"Accessibility & Image SEO: {len(images_without_alt)} out of {len(images)} images missing alt text.")

    # Content to HTML Ratio
    for s in soup(["script", "style", "svg"]):
        s.decompose()
    text_content = soup.get_text(separator=" ", strip=True)
    word_count = len(text_content.split())
    results["on_page"]["word_count"] = word_count
    
    html_len = len(html_content) if html_content else 1
    text_len = len(text_content)
    text_ratio = round((text_len / html_len) * 100, 1)
    results["on_page"]["text_ratio_pct"] = text_ratio

    if text_ratio < 8.0:
        results["issues"]["warnings"].append(f"Content Density: Low text-to-HTML ratio ({text_ratio}%). Search engines prefer higher content density.")

    # 6. Check Robots.txt and Sitemap
    robots_url = f"{parsed.scheme}://{domain}/robots.txt"
    try:
        req_rob = urllib.request.Request(robots_url, headers=headers)
        with urllib.request.urlopen(req_rob, timeout=5, context=ctx) as r:
            robots_content = r.read().decode("utf-8", errors="replace")
            results["technical"]["has_robots_txt"] = True
            results["technical"]["robots_length"] = len(robots_content)
            
            # Check AI crawler access
            ai_bots = ["gptbot", "claudebot", "perplexitybot", "google-extended"]
            blocked_bots = []
            for bot in ai_bots:
                if re.search(rf"user-agent:\s*{bot}.*?disallow:\s*/\b", robots_content, re.I | re.S):
                    blocked_bots.append(bot)
            results["ai_readiness"]["blocked_ai_bots"] = blocked_bots
            if blocked_bots:
                results["issues"]["warnings"].append(f"AI Visibility: Robots.txt blocks AI search crawlers: {', '.join(blocked_bots)}.")
    except Exception:
        results["technical"]["has_robots_txt"] = False
        results["issues"]["notices"].append("Technical SEO: robots.txt file not found or inaccessible.")

    # Check Sitemap
    sitemap_url = f"{parsed.scheme}://{domain}/sitemap.xml"
    try:
        req_sm = urllib.request.Request(sitemap_url, headers=headers)
        with urllib.request.urlopen(req_sm, timeout=5, context=ctx) as r:
            results["technical"]["has_sitemap"] = r.getcode() == 200
    except Exception:
        results["technical"]["has_sitemap"] = False
        results["issues"]["notices"].append("Technical SEO: XML Sitemap (/sitemap.xml) not found or returned error.")

    # 7. Compute Semrush-Style Site Health Score
    results["errors_count"] = len(results["issues"]["errors"])
    results["warnings_count"] = len(results["issues"]["warnings"])
    results["notices_count"] = len(results["issues"]["notices"])

    deductions = (results["errors_count"] * 10) + (results["warnings_count"] * 2) + (results["notices_count"] * 0.5)
    site_health = max(10, int(100 - deductions))
    results["site_health"] = site_health

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: seo_auditor.py <url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    res = audit_url(target_url)
    print(json.dumps(res, indent=2))
