import requests


def scan_url(url):
    results = []
    score = 100

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
    except:
        return ["Unable to connect to website"], 0

    # Security headers
    required = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "X-XSS-Protection",
        "Strict-Transport-Security"
    ]

    for h in required:
        if h not in headers:
            results.append(f"Missing {h} header")
            score -= 10

    # SQLi basic
    try:
        payload = "' OR 1=1--"
        r = requests.get(url, params={"id": payload}, timeout=10, verify=False)
        if any(x in r.text.lower() for x in ["sql", "mysql", "syntax"]):
            results.append("Possible SQL Injection vulnerability")
            score -= 20
    except:
        pass

    # XSS basic
    try:
        payload = "<script>alert(1)</script>"
        r = requests.get(url, params={"q": payload}, timeout=10, verify=False)
        if payload in r.text:
            results.append("Possible XSS vulnerability")
            score -= 20
    except:
        pass

    # robots.txt check
    try:
        r = requests.get(url + "/robots.txt", timeout=10, verify=False)
        if r.status_code == 200:
            results.append("robots.txt exposed")
            score -= 5
    except:
        pass

    # admin page check
    try:
        r = requests.get(url + "/admin", timeout=10, verify=False)
        if r.status_code == 200:
            results.append("Admin panel accessible")
            score -= 10
    except:
        pass

    return results, max(score, 0)