"""Static site generator for the portfolio: python build/build.py  (writes HTML at the repo root)."""

import html
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content import (CASES, EMAIL, EXPERIENCE, FEATURED, KITS, LINKS, NAME, REALISTIC, REPOS, SITE, SOCIAL_POSTS, STACK, STATS, UIKITS,
                     WEB)

ROOT = Path(__file__).resolve().parents[1]
e = html.escape
FONTS = {
    "home": "family=Inter+Tight:wght@500;600;700&family=Instrument+Serif:ital@1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500",
    "code": "family=Doto:wght@700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600",
    "3d": "family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500",
    "design": "family=Inter+Tight:wght@500;600;700&family=Instrument+Serif:ital@1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500",
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
<link rel="stylesheet" href="{up}assets/site.css">
{ld}
</head>
<body class="t-{theme}">
<header class="nav"><a class="brand" href="{up}">Affif<span>.</span></a><nav class="menu" aria-label="Main">{menu}</nav><a class="hire" href="mailto:{EMAIL}">Hire me</a></header>
{body.replace("{up}", up)}
<script src="{up}assets/site.js" defer></script>
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
<p>Open to remote roles and freelance projects in software &amp; AI, 3D and product design. Based in Jakarta (GMT+7).</p>
<div class="row"><a class="btn solid" href="mailto:{EMAIL}">{EMAIL}</a>{links}</div>
<div class="foot"><span>© {date.today().year} {NAME}</span><span>Designed and built by hand. No template.</span></div></section>"""


def img(src, alt, w=None, h=None, cls="", lazy=True):
    size = f' width="{w}" height="{h}"' if w else ""
    return f'<img src="{{up}}{src}" alt="{e(alt)}"{size}{" loading=lazy decoding=async" if lazy else ""}{f" class={cls}" if cls else ""}>'


# ------------------------------------------------------------------ home
def home():
    panels = [
        ("code", "software/", "01", "Software &amp; AI", "AI systems built for production: agents, evals, document AI, full-stack apps.",
         ["MCP", "LLM evals", "React", "Python"], "assets/ai/docflow.webp", "docflow review interface"),
        ("3d", "3d/", "02", "3D, Game &amp; Assets", "Real-time 3D on the web, game asset kits, game UI and photoreal renders.",
         ["three.js", "Blender", "Game UI", "PBR"], "assets/3d/kenney-fantasy-town-sample.webp", "Low-poly fantasy town scene"),
        ("design", "design/", "03", "Product Design &amp; UI/UX", "Product teardowns, SaaS and web interfaces, social media and video.",
         ["Figma", "Case studies", "Web", "Social"], "assets/work/vue-dashboard.webp", "VUE dashboard UI design"),
    ]
    cards = "".join(f"""<a class="panel p-{k}" href="{{up}}{href}" aria-label="{t.replace('&amp;', 'and')}">
{img(src, alt, lazy=False, cls='bg')}<span class="num">{n}</span><span class="go" aria-hidden="true">→</span>
<div class="txt"><h2>{t}</h2><p>{d}</p><div class="chips">{''.join(f'<span>{c}</span>' for c in chips)}</div></div><i class="glow"></i></a>"""
                    for k, href, n, t, d, chips, src, alt in panels)
    stats = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in STATS)
    body = f"""<main class="home">
<div class="home-head"><span class="eyebrow"><i></i>Available for remote work · Jakarta</span>
<h1>I build software, shape <em>3D worlds</em> and design products.</h1>
<p class="intro">Hi, I'm Affif: a full-stack &amp; AI engineer, 3D generalist and product designer with 50+ projects shipped for international clients. Pick a world to see the work.</p></div>
<nav class="stage" aria-label="Portfolio categories">{cards}</nav>
<div class="home-foot">{stats}</div>
</main>"""
    return page("index.html", "home", f"{NAME} · Software & AI, 3D and Product Design",
                "Portfolio of Affif Ariza Adiwijaya, a Jakarta-based full-stack and AI engineer, 3D generalist and product designer. "
                "AI agents and evals, three.js and game assets, UI/UX and product case studies.",
                body, "home", [PERSON, {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE}])


# ------------------------------------------------------------------ software
def software():
    feats = []
    for f in FEATURED:
        visual = (f'<div class="shot">{img(f["img"], f["title"] + " screenshot", cls="")}</div>' if f.get("img") else
                  '<div class="shot code">' + "".join(f"<span><b>{e(a)}</b>{e(b)}</span>" for a, b in f["snippet"]) + "</div>")
        links = (f'<a class="live" href="{f["live"]}" target="_blank" rel="noopener">▶ Live demo</a>' if f.get("live") else "") + \
                f'<a href="{f["code"]}" target="_blank" rel="noopener">GitHub ↗</a>'
        feats.append(f"""<article class="feat rv" id="{f['slug']}"><div class="bar"><i></i><i></i><i></i><b>~/{f['title']}</b></div>
{visual}<div class="body"><span class="kind">{e(f['kind'])}</span><h3>{e(f['title'])}</h3><p>{e(f['text'])}</p>
<div class="tags">{''.join(f'<span class="tag">{t}</span>' for t in f['tags'])}</div><div class="links">{links}</div></div></article>""")
    ls = "".join(f'<a href="{LINKS["GitHub"]}/{n}" target="_blank" rel="noopener"><span class="n">{n}/</span><span class="s">{e(s)}</span>'
                 f'<span class="d">{e(d)}</span><span class="ar">↗</span></a>' for n, s, d in REPOS)
    pkg = "{<br>" + ",<br>".join(f'&nbsp;&nbsp;<span class="k">"{k}"</span>: <span class="v">"{e(v)}"</span>' for k, v in STACK.items()) + "<br>}"
    log = "".join(f"<li><time>{t}</time><h4>{e(h)}</h4><p>{e(p)}</p></li>" for t, h, p, tag in EXPERIENCE if "code" in tag)
    body = f"""<main class="wrap">
<section class="term-hero"><p class="prompt">affif@portfolio:~/software$ <span data-type="ls --featured --live"></span><span class="cur"></span></p>
<h1>Software that<br>does real work.</h1>
<p class="lead">AI engineering for production, not demos: agents with guardrails, evaluations that gate CI, document AI with a human in the loop. Plus the full-stack, ERP and infrastructure work underneath.</p>
<div class="row"><a class="btn solid" href="#docflow">See featured builds</a><a class="btn line" href="{LINKS['GitHub']}" target="_blank" rel="noopener">github.com/affifariza04</a></div></section>
<div class="sec-h rv"><h2>featured</h2><p>Each one runs offline in CI, ships with tests and has a live demo or a runnable session.</p></div>
{''.join(feats)}
<div class="sec-h rv"><h2>more_repos</h2><p>Systems, data and infrastructure deep dives on GitHub.</p></div>
<div class="ls rv">{ls}</div>
<div class="sec-h rv"><h2>stack</h2><p>What I reach for, and what I've shipped with.</p></div>
<div class="pkg rv">{pkg}</div>
<div class="sec-h rv"><h2>log</h2><p>Engineering experience.</p></div>
<ol class="log rv">{log}</ol>
</main>{contact()}"""
    return page("software/index.html", "code", f"Software & AI Engineering · {NAME}",
                "AI engineering portfolio: MCP server for Odoo, LLM evaluation CI gate, document AI with human review, three.js configurator, "
                "full-stack and infrastructure projects by Affif Ariza Adiwijaya.", body, "code",
                [{"@context": "https://schema.org", "@type": "ItemList", "name": "Software & AI projects",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f["code"], "name": f["title"]} for i, f in enumerate(FEATURED)]}])


# ------------------------------------------------------------------ 3D
def three_d():
    names = {"camera_01": "Rangefinder camera", "vintage_electric_kettle": "Vintage kettle", "mid_century_lounge_chair": "Lounge chair",
             "brass_vase_03": "Brass vase", "coffeecart_01": "Coffee cart", "tea_set_01": "Tea set", "antique_ceramic_vase_01": "Ceramic vase",
             "armchair_01": "Armchair", "potted_plant_04": "Potted plant", "croissant": "Croissant"}
    real = "".join(f'<a class="r-card tilt{" wide" if r in ("tea_set_01", "croissant") else ""}" href="#" data-zoom="{{up}}assets/3d/{r}.webp">'
                   f'{img(f"assets/3d/{r}.webp", names[r] + ", photoreal 3D render")}</a>' for r in REALISTIC)
    kits = "".join(f'<a href="#" data-zoom="{{up}}assets/3d/{s}.webp" class="tilt">{img(f"assets/3d/{s}.webp", t)}<div><b>{t}</b><span>{d}</span></div></a>'
                   for s, t, d in KITS)
    ui = "".join(f'<a href="#" data-zoom="{{up}}assets/3d/{s}.webp" class="tilt">{img(f"assets/3d/{s}.webp", t + " game UI")}<div><b>{t}</b><span>{d}</span></div></a>'
                 for s, t, d in UIKITS)
    body = f"""<main class="wrap">
<section class="g-hero"><div><span class="eyebrow"><i></i>3D · Game · Real-time</span>
<h1>Worlds you can <span>play with.</span></h1>
<p class="lead">Real-time 3D for the web, game-ready asset kits and game UI, photoreal product renders and CAD for manufacturing.</p>
<div class="row"><a class="btn solid" href="https://affifariza04.github.io/lumen-configurator/" target="_blank" rel="noopener">Open the configurator ↗</a><a class="btn line" href="#renders">Browse renders</a></div></div>
<div class="window"><div class="in"><iframe src="https://affifariza04.github.io/lumen-configurator/" title="Lumen 3D lamp configurator, interactive" loading="lazy"></iframe><span class="hint">drag to orbit · pick finishes</span></div></div></section>
<div class="shelf-h rv" id="renders"><h2>Photoreal renders</h2><p>Product-shot lighting and PBR materials. Tap to enlarge.</p></div>
<div class="r-grid rv">{real}</div>
<div class="shelf-h rv"><h2>Game asset kits</h2><p>Low-poly, modular, game-ready: towns, nature and hex worlds.</p></div>
<div class="lib rv">{kits}</div>
<div class="shelf-h rv"><h2>Game UI</h2><p>HUD panels, menus, shop and settings screens in several styles.</p></div>
<div class="lib rv">{ui}</div>
<div class="shelf-h rv"><h2>CAD for manufacturing</h2><p>A client's Rhino STEP extended by tiling its own lattice cell with OpenCascade (Python), then rendered in Blender Cycles.</p></div>
<div class="cad rv"><a href="#" data-zoom="{{up}}assets/work/knuckle-hero.webp">{img("assets/work/knuckle-hero.webp", "Glove knuckle guard lattice, rendered")}</a>
<div class="stack"><a href="#" data-zoom="{{up}}assets/work/knuckle-sheet.webp">{img("assets/work/knuckle-sheet.webp", "Annotated concept sheet with dimensions")}</a>
<a href="#" data-zoom="{{up}}assets/work/knuckle-detail.webp">{img("assets/work/knuckle-detail.webp", "Lattice detail close-up")}</a></div></div>
</main>{contact()}"""
    return page("3d/index.html", "3d", f"3D, Game Assets & Real-time · {NAME}",
                "3D portfolio: interactive three.js product configurator, photoreal product renders, low-poly game asset kits, game UI "
                "and CAD for manufacturing by Affif Ariza Adiwijaya.", body, "3d")


# ------------------------------------------------------------------ design
def design():
    cases = "".join(f"""<a class="case-c rv" href="{{up}}design/{c['slug']}/"><div class="im">{img(f"assets/case/{c['slug']}-hero.webp", c['product'] + ' homepage')}</div>
<div class="tx"><small>{e(c['category'])} · teardown</small><h3>{e(c['title'])}</h3><p>{e(c['lede'])}</p></div></a>""" for c in CASES)
    web = "".join(f'<a class="w-item {w} rv" href="#" data-zoom="{{up}}assets/work/{s}.webp">{img(f"assets/work/{s}.webp", t)}<div><b>{e(t)}</b><span>{e(d)}</span></div></a>'
                  for s, t, d, w in WEB)
    posts = (SOCIAL_POSTS * 3)[:9]
    grid = "".join(f'<a href="#" data-zoom="{{up}}assets/work/{p}.webp">{img(f"assets/work/{p}.webp", "Social media post design")}</a>' for p in posts)
    xp = "".join(f"<li><time>{t}</time><div><h4>{e(h)}</h4><p>{e(p)}</p></div></li>" for t, h, p, tag in EXPERIENCE if "design" in tag)
    body = f"""<section class="d-hero"><span class="eyebrow"><i></i>Product design · UI/UX · Social</span>
<h1>Product design that <em>earns</em> its place.</h1>
<div class="bottom"><p>I design SaaS interfaces, websites and content systems, and I study how the best products sell themselves.</p>
<div class="row"><a class="btn solid" href="#cases">Read case studies ↘</a><a class="btn line" href="#web">See UI work</a></div></div></section>
<nav class="tabs" aria-label="Sections"><a href="#cases" class="on">Case studies</a><a href="#web">Web &amp; UI</a><a href="#social">Social media</a><a href="#experience">Experience</a></nav>
<main class="wrap">
<section class="d-sec" id="cases"><div class="d-h rv"><div><span class="eyebrow"><i></i>Product teardowns</span><h2>How great SaaS <span>sells complex products.</span></h2></div>
<p>Five independent studies of product homepages: positioning, hierarchy, proof and the experiments I'd run next.</p></div>
<div class="cases">{cases}</div></section>
<section class="d-sec" id="web"><div class="d-h rv"><div><span class="eyebrow"><i></i>Web &amp; UI</span><h2>Interfaces <span>and systems.</span></h2></div>
<p>Platforms, dashboards and brand systems, designed in Figma on shared design systems.</p></div>
<div class="work-grid">{web}</div></section>
<section class="d-sec" id="social"><div class="d-h rv"><div><span class="eyebrow"><i></i>Social media</span><h2>Content people <span>stop scrolling for.</span></h2></div>
<p>Post systems and campaign graphics, plus short-form video: concept, shoot direction, editing and captions.</p></div>
<div class="social rv"><div><div class="phone"><div class="scr"><div class="ig-top"><i></i>campaign.studio</div>
<div class="ig-stats"><div><b>48</b>posts</div><div><b>12 wk</b>campaign</div><div><b>EN/ES</b>bilingual</div></div><div class="ig-grid">{grid}</div></div></div>
<div class="cap"><b>Post systems</b><p>12-week bilingual campaign for a children's nonprofit and travel campaign graphics.</p></div></div>
<div><div class="phone"><div class="scr"><div class="reel">{img("assets/work/travel-reels.webp", "Short-form travel reels")}<div class="ov"><b>Traveloka · reels</b>Concept · shoot direction · edit · captions</div></div></div></div>
<div class="cap"><b>Short-form video</b><p>Hotel tours, destination guides and brand integrations for TikTok and Reels.</p></div></div></div></section>
<section class="d-sec" id="experience"><div class="d-h rv"><div><span class="eyebrow"><i></i>Experience</span><h2>Where I've <span>designed.</span></h2></div></div>
<ol class="xp rv">{xp}</ol></section>
</main>{contact()}"""
    return page("design/index.html", "design", f"Product Design, UI/UX & Social · {NAME}",
                "Product design portfolio: SaaS homepage teardowns (Attio, Tally, Sunsama, Dovetail, Heptabase), UI/UX for platforms and "
                "dashboards, social media design and short-form video by Affif Ariza Adiwijaya.", body, "design")


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
