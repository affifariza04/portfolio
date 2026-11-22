"""Static site generator for the portfolio: python build/build.py  (writes HTML at the repo root)."""

import html
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content import CASES, EMAIL, EXPERIENCE, FEATURED, LANGUAGES, LINKS, NAME, SITE
from pages import design_body, game_body, home_body, software_body

ROOT = Path(__file__).resolve().parents[1]
import time
VER = time.strftime("%Y%m%d%H%M")
e = html.escape
FONTS = {
    "home": "family=Unbounded:wght@600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600",
    "code": "family=Unbounded:wght@600;700&family=Doto:wght@700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600",
    "3d": "family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500",
    "design": "family=Unbounded:wght@600;700&family=Inter+Tight:wght@500;600;700&family=Instrument+Serif:ital@1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500",
}
PERSON = {"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": SITE, "email": f"mailto:{EMAIL}",
          "jobTitle": "Full-stack & AI Engineer, 3D Generalist, Product Designer",
          "address": {"@type": "PostalAddress", "addressLocality": "Jakarta", "addressCountry": "ID"},
          "sameAs": list(LINKS.values()),
          "knowsAbout": ["AI engineering", "Model Context Protocol", "LLM evaluation", "React", "Python", "three.js", "Blender",
                         "Product design", "UI/UX", "Figma", "Odoo"]}


def page(path, theme, title, desc, body, nav_on=None, jsonld=None, image="assets/og.png"):
    depth = path.count("/")
    up = "../" * depth
    url = SITE + (path[:-len("index.html")] if path.endswith("index.html") else path)
    menu = "".join(f'<a href="{up}{href}"{" aria-current=page" if key == nav_on else ""}>{label}</a>'
                   for key, href, label in [("home", "", "Home"), ("code", "software/", "Software & AI"), ("3d", "3d/", "3D & Game"),
                                            ("design", "design/", "Product Design")])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    doc = f"""<!doctype html>
<html lang="en" class="t-{theme}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="author" content="{NAME}"><meta name="theme-color" content="#07070A">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE}{image}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS[theme if theme in FONTS else 'design']}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css?v={VER}">
{ld}
</head>
<body class="t-{theme}">
<header class="nav"><a class="brand" href="{up}">Affif<span>.</span></a><nav class="menu" aria-label="Main">{menu}</nav><a class="hire" href="mailto:{EMAIL}">Hire me</a></header>
{body.replace("{up}", up).replace(".js\"></script>", f".js?v={VER}\"></script>")}
<script src="{up}assets/site.js?v={VER}" defer></script>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return url


def contact(dark=True):
    links = "".join(f'<a class="btn line" href="{u}" target="_blank" rel="noopener">{k}</a>' for k, u in LINKS.items())
    return f"""<section class="contact wrap rv" id="contact"><h2>Let's build something worth showing.</h2>
<p>Open to remote roles and freelance projects in software &amp; AI, 3D and product design. Based in Jakarta (GMT+7). Languages: {LANGUAGES}.</p>
<div class="row"><a class="btn solid" href="mailto:{EMAIL}">{EMAIL}</a>{links}</div>
<div class="foot"><span>© {date.today().year} {NAME}</span><span>Designed and built by hand. No template.</span></div></section>"""


def img(src, alt, w=None, h=None, cls="", lazy=True):
    size = f' width="{w}" height="{h}"' if w else ""
    return f'<img src="{{up}}{src}" alt="{e(alt)}"{size}{" loading=lazy decoding=async" if lazy else ""}{f" class={cls}" if cls else ""}>'


# ------------------------------------------------------------------ home
def home():
    return page("index.html", "home", f"{NAME} · Software & AI, 3D & Game, Product Design",
                "Portfolio of Affif Ariza Adiwijaya, a Jakarta-based full-stack and AI engineer, game and 3D creator and product designer: "
                "AI agents and evals, a Roblox game, playable 3D, and SaaS product case studies.",
                home_body(), "home", [PERSON, {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE}])


# ------------------------------------------------------------------ software
def software():
    return page("software/index.html", "code", f"Software & AI Engineering · {NAME}",
                "AI engineering portfolio: MCP server for Odoo, LLM evaluation CI gate, document AI with human review, three.js configurator "
                "and full-stack projects by Affif Ariza Adiwijaya.", software_body(contact()), "code",
                [{"@context": "https://schema.org", "@type": "ItemList", "name": "Software & AI projects",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f["code"], "name": f["title"]} for i, f in enumerate(FEATURED)]}])


# ------------------------------------------------------------------ 3D
def three_d():
    return page("3d/index.html", "3d", f"3D & Game: playable 3D, Roblox game, 3D showroom · {NAME}",
                "Interactive 3D and game portfolio: a playable three.js character playground, the Roblox game Revive & Steal a Dino, "
                "a rotatable photoreal 3D model showroom and a product configurator by Affif Ariza Adiwijaya.", game_body(contact()), "3d",
                [{"@context": "https://schema.org", "@type": "VideoGame", "name": "Revive & Steal a Dino", "url": "https://www.roblox.com/games/108232369899456",
                  "gamePlatform": "Roblox", "author": {"@type": "Person", "name": NAME}}])


# ------------------------------------------------------------------ design
def design():
    return page("design/index.html", "design", f"Product Design & UX Case Studies · {NAME}",
                "Product design portfolio: SaaS homepage teardowns of Attio, Tally, Sunsama, Dovetail and Heptabase, with positioning, "
                "hierarchy and experiment design, by Affif Ariza Adiwijaya.", design_body(contact()), "design")


def case_page(i, c):
    nxt = CASES[(i + 1) % len(CASES)]
    jobs = "".join(f"<li><b>0{k + 1}</b>{e(j)}</li>" for k, j in enumerate(c["jobs"]))
    works = "".join(f"<div><b><i>0{k + 1}</i>{e(t)}</b><p>{e(p)}</p></div>" for k, (t, p) in enumerate(c["works"]))
    fr = "".join(f"<div><b><i>!</i>{e(t)}</b><p>{e(p)}</p></div>" for t, p in c["friction"])
    tests = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(m)}</td></tr>" for a, b, m in c["tests"])
    host = c["url"].split("//")[1].strip("/")
    body = f"""<main class="wrap cs"><p class="crumb"><a href="{{up}}design/">Product Design</a> / <a href="{{up}}design/#cases">Case studies</a> / {e(c['product'])}</p>
<div class="cs-head"><h1>{e(c['title'])}</h1><div><p class="lede">{e(c['lede'])}</p><span class="note">Independent teardown of the public homepage · not affiliated with {e(c['product'])}</span></div></div>
<div class="meta"><div><small>Product</small><span>{e(c['product'])}</span></div><div><small>Category</small><span>{e(c['category'])}</span></div>
<div><small>Audience</small><span>{e(c['audience'])}</span></div><div><small>Focus</small><span>{e(c['focus'])}</span></div></div>
<div class="browser"><div class="bar"><i></i><i></i><i></i><span>{host}</span></div><a href="#" data-zoom="{{up}}assets/case/{c['slug']}-hero.webp">{img(f"assets/case/{c['slug']}-hero.webp", c['product'] + ' homepage hero', 1440, 900, lazy=False)}</a></div>
<div class="cs-body"><aside><a href="#jobs">The job of the page</a><a href="#works">What works</a><a href="#friction">Friction</a><a href="#tests">What I'd test</a><a href="#takeaway">Takeaway</a></aside>
<div><section id="jobs"><h2>The job of the page</h2><ul class="jobs">{jobs}</ul></section>
<section id="works"><h2>What works</h2><div class="obs">{works}</div></section>
<section><div class="browser"><div class="bar"><i></i><i></i><i></i><span>{host} · further down</span></div><a href="#" data-zoom="{{up}}assets/case/{c['slug']}-scroll.webp">{img(f"assets/case/{c['slug']}-scroll.webp", c['product'] + ' homepage sections below the hero', 1200, 1417)}</a></div></section>
<section id="friction"><h2>Friction &amp; opportunities</h2><div class="obs warn">{fr}</div></section>
<section id="tests"><h2>What I'd test next</h2><table class="tests"><tr><th>Experiment</th><th>Variant</th><th>Success metric</th></tr>{tests}</table></section>
<section id="takeaway"><h2>Takeaway for my own work</h2><p class="take">{e(c['takeaway'])}</p>
<a class="next" href="{{up}}design/{nxt['slug']}/"><div><small>Next case study</small><b>{e(nxt['title'])}</b></div><span class="btn solid">Read →</span></a></section></div></div>
</main>{contact()}"""
    url = SITE + f"design/{c['slug']}/"
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["lede"],
           "author": {"@type": "Person", "name": NAME, "url": SITE}, "image": SITE + f"assets/case/{c['slug']}-hero.webp", "url": url},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
              {"@type": "ListItem", "position": 2, "name": "Product Design", "item": SITE + "design/"},
              {"@type": "ListItem", "position": 3, "name": c["product"], "item": url}]}]
    return page(f"design/{c['slug']}/index.html", "design", f"{c['title']} · UX case study · {NAME}", c["lede"], body, "design", ld,
                image=f"assets/case/{c['slug']}-hero.webp")


def main():
    urls = [home(), software(), three_d(), design()] + [case_page(i, c) for i, c in enumerate(CASES)]
    today = date.today().isoformat()
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n",
                                      encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
    print("\n".join(urls))


if __name__ == "__main__":
    main()
