"""Headless smoke run: visit each main page, capture a screenshot,
collect console errors and failed network requests. Run with:

    .venv/bin/python playwright_smoke/smoke.py

The dev server must be running at http://localhost:8003.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
BASE = "http://localhost:8003"
ROUTES = [
    ("/", "homepage"),
    ("/services/", "services"),
    ("/about/", "about"),
    ("/contact/", "contact"),
    ("/portfolio/", "portfolio"),
    ("/team/", "team"),
    ("/blog/", "blog"),
    ("/resume/", "resume"),
    ("/admin/login/", "admin-login"),
    ("/search/", "search-empty"),
    ("/search/?query=test", "search-query"),
]


def visit(page, path: str, name: str) -> dict:
    failed_requests: list[tuple[str, int | str]] = []
    console_messages: list[tuple[str, str]] = []

    page.on("console", lambda msg: console_messages.append((msg.type, msg.text)))
    page.on(
        "requestfailed",
        lambda req: failed_requests.append((req.url, req.failure or "unknown")),
    )
    page.on(
        "response",
        lambda resp: failed_requests.append((resp.url, resp.status))
        if resp.status >= 400
        else None,
    )

    response = page.goto(BASE + path, wait_until="networkidle", timeout=15000)
    page.screenshot(path=OUT / f"{name}.png", full_page=True)

    return {
        "name": name,
        "path": path,
        "status": response.status if response else None,
        "title": page.title(),
        "failed_requests": failed_requests,
        "console_errors": [(t, m) for t, m in console_messages if t == "error"],
    }


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        results = [visit(page, path, name) for path, name in ROUTES]

        browser.close()

    for r in results:
        print(f"\n=== {r['name']}  {r['path']}  HTTP {r['status']}  title={r['title']!r} ===")
        if r["console_errors"]:
            print(f"  CONSOLE ERRORS ({len(r['console_errors'])}):")
            for t, m in r["console_errors"][:10]:
                print(f"    [{t}] {m[:200]}")
        if r["failed_requests"]:
            print(f"  FAILED REQUESTS ({len(r['failed_requests'])}):")
            for url, status in r["failed_requests"][:15]:
                print(f"    {status}  {url}")
        if not r["console_errors"] and not r["failed_requests"]:
            print("  clean")

    print(f"\nScreenshots saved to {OUT}/")


if __name__ == "__main__":
    sys.exit(main() or 0)
