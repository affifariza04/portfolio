"""Page bodies for the redesigned site (home cylinder, slice heroes, interactive 3D lab)."""

from html import escape as e

from content import CASES, EMAIL, EXPERIENCE, FEATURED, LANGUAGES, LINKS, REPOS, ROBLOX, SHOWROOM, STACK, STATS


def img(src, alt, cls="", lazy=True, w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ""
    return f'<img src="{{up}}{src}" alt="{e(alt)}"{size}{" loading=lazy decoding=async" if lazy else ""}{f" class={cls}" if cls else ""}>'


def slices(lead_html, items):
    """Disney+-style hero: a lead panel then curved vertical slices. items: (href, img, alt, tag, title, text, pos)."""
    out = [f'<div class="slice lead" style="--i:0">{lead_html}</div>']
    for i, (href, src, alt, tag, title, text, pos) in enumerate(items, start=1):
        out.append(f'<a class="slice" href="{href}" style="--i:{i};--pos:{pos}">{img(src, alt, lazy=False)}'
                   f'<div class="cap"><em>{e(tag)}</em><b>{e(title)}</b><span>{e(text)}</span></div></a>')
    return f'<section class="slices" aria-label="Featured">{"".join(out)}</section>'


# ------------------------------------------------------------------ home
HOME_CARDS = [
    ("code", "software/#docflow", "assets/covers/docflow.webp", "Document AI"),
    ("game", "3d/#play", "assets/covers/robot.webp", "Playable 3D"),
    ("design", "design/attio/", "assets/covers/attio.webp", "Product teardown"),
    ("code", "software/#evalgate", "assets/covers/evalgate.webp", "LLM evals"),
    ("game", "3d/#roblox", "assets/roblox/dino-1.webp", "Roblox game"),
    ("design", "design/tally/", "assets/covers/tally.webp", "UX case study"),
    ("code", "software/#odoo-mcp", "assets/covers/odoo-mcp.webp", "AI agents · MCP"),
    ("game", "3d/#showroom", "assets/covers/showroom.webp", "Interactive 3D"),
    ("design", "design/heptabase/", "assets/covers/heptabase.webp", "Product teardown"),
]


def home_body():
    n = len(HOME_CARDS)
    cards = "".join(
        f'<a class="card" data-c="{c}" href="{{up}}{href}" style="transform:rotateY({i * 360 / n:.3f}deg) translateZ(var(--r))">'
        f'<span class="face">{img(src, cat + " project cover", lazy=i > 4)}</span><span class="cat">{cat}</span></a>'
        for i, (c, href, src, cat) in enumerate(HOME_CARDS))
    stats = " · ".join(f"{a} {b}" for a, b in STATS)
    return f"""<main class="home">
<div class="aura" aria-hidden="true"></div><div class="rings" aria-hidden="true"><i></i><i></i><i></i></div>
<img class="me in-up" src="{{up}}assets/me.webp" alt="Affif Ariza Adiwijaya" width="76" height="76">
<h1 class="in-up" style="animation-delay:.06s">Welcome to <span>Affif's world.</span></h1>
<p class="intro in-up" style="animation-delay:.12s">Full-stack &amp; AI engineer, game &amp; 3D creator and product designer from Jakarta. {stats}.</p>
<p class="lang in-up" style="animation-delay:.18s">{LANGUAGES}</p>
<div class="cyl-wrap in-up" style="animation-delay:.25s" data-cyl><div class="cyl">{cards}</div></div>
</main>"""


# ------------------------------------------------------------------ software
def software_body(contact):
    lead = """<span class="eyebrow"><i></i>affif@portfolio:~/software</span><h1>Software that does real work.</h1>
<p>AI engineering for production: agents with guardrails, evals that gate CI, document AI with a human in the loop.</p>
<div class="row"><a class="btn solid" href="#featured">Explore builds</a><a class="btn line" href="https://github.com/affifariza04" target="_blank" rel="noopener">GitHub ↗</a></div>"""
    items = [("#docflow", "assets/ai/docflow.webp", "docflow", "Document AI", "docflow", "Claude extracts invoices, rules flag mistakes, people approve.", "top left"),
             ("#evalgate", "assets/ai/evalgate.webp", "evalgate", "LLM evals", "evalgate", "A CI gate that blocks prompts that break policy.", "top"),
             ("#odoo-mcp", "assets/ai/odoo-mcp.webp", "odoo-mcp", "MCP · agents", "odoo-mcp", "Safe, typed AI access to an Odoo ERP.", "center"),
             ("#lens", "assets/ai/lens.webp", "lens", "On-device AI", "lens", "Search photos by meaning with CLIP, in the browser.", "top"),
             ("#whisper-web", "assets/ai/whisper-web.webp", "whisper-web", "Speech AI", "whisper-web", "Private speech-to-text with Whisper, on-device.", "top")]
    feats = []
    for f in FEATURED:
        visual = (f'<div class="shot">{img(f["img"], f["title"] + " screenshot")}</div>' if f.get("img") else
                  '<div class="shot code">' + "".join(f"<span><b>{e(a)}</b>{e(b)}</span>" for a, b in f["snippet"]) + "</div>")
        links = (f'<a class="live" href="{f["live"]}" target="_blank" rel="noopener">▶ Live demo</a>' if f.get("live") else "") + \
                f'<a href="{f["code"]}" target="_blank" rel="noopener">GitHub ↗</a>'
        feats.append(f"""<article class="feat rv" id="{f['slug']}"><div class="bar"><i></i><i></i><i></i><b>~/{f['title']}</b></div>
{visual}<div class="body"><span class="kind">{e(f['kind'])}</span><h3>{e(f['title'])}</h3><p>{e(f['text'])}</p>
<div class="tags">{''.join(f'<span class="tag">{t}</span>' for t in f['tags'])}</div><div class="links">{links}</div></div></article>""")
    ls = "".join(f'<a href="{LINKS["GitHub"]}/{n}" target="_blank" rel="noopener"><span class="n">{n}/</span><span class="s">{e(s)}</span>'
                 f'<span class="d">{e(d)}</span><span class="ar">↗</span></a>' for n, s, d in REPOS)
    pkg = "{<br>" + ",<br>".join(f'&nbsp;&nbsp;<span class="k">"{k}"</span>: <span class="v">"{e(v)}"</span>' for k, v in STACK.items()) + "<br>}"
    log = "".join(f"<li><time>{t}</time><h4>{e(h)}</h4><p>{e(p)}</p></li>" for t, h, p, tag in EXPERIENCE)
    return f"""{slices(lead, items)}<main class="wrap">
<div class="sec-h rv" id="featured"><h2>featured</h2><p>Each one runs offline in CI, ships with tests and has a live demo or a runnable session.</p></div>
{''.join(feats)}
<div class="sec-h rv"><h2>more_repos</h2><p>Systems, data and infrastructure deep dives on GitHub.</p></div><div class="ls rv">{ls}</div>
<div class="sec-h rv"><h2>stack</h2><p>What I reach for, and what I've shipped with.</p></div><div class="pkg rv">{pkg}</div>
<div class="sec-h rv"><h2>log</h2><p>3 years of experience across software, 3D and design.</p></div><ol class="log rv">{log}</ol>
</main>{contact}"""


# ------------------------------------------------------------------ 3D & game
def game_body(contact):
    lead = """<span class="eyebrow"><i></i>3D · Game · Real-time</span><h1>Worlds you can play with.</h1>
<p>A Roblox game I built, a playable browser prototype of its core loop, and 3D models you can spin, zoom and inspect.</p>
<div class="row"><a class="btn solid" href="#play">Play now ↓</a><a class="btn line" href="#roblox">My Roblox game</a></div>"""
    items = [("#play", "assets/covers/robot.webp", "Character playground", "Playable", "Character playground", "Drive, dance and emote a 3D robot right here.", "center"),
             ("#roblox", "assets/roblox/dino-2.webp", ROBLOX["name"], "Roblox", ROBLOX["name"], "Dig bones, revive dinos, steal bases.", "center"),
             ("#roblox", "assets/roblox/dino-3.webp", "Dino base", "Game design", "Base building & mutations", "Idle income, upgrades and rare mutations.", "center"),
             ("#showroom", "assets/covers/showroom.webp", "3D showroom", "Interactive", "3D showroom", "Spin, zoom and inspect photoreal models.", "center"),
             ("#particles-h", "assets/covers/particles.webp", "Particle morph lab", "Real-time", "Particle morph lab", "14k particles morphing between 3D shapes.", "center")]
    shots = "".join(img(f"assets/roblox/{s}.webp", f"{ROBLOX['name']} screenshot", cls="on" if i == 0 else "", lazy=i > 0)
                    for i, s in enumerate(ROBLOX["shots"]))
    dots = "".join(f'<i{" class=on" if i == 0 else ""}></i>' for i in range(len(ROBLOX["shots"])))
    feats = "".join(f"<li>{e(f)}</li>" for f in ROBLOX["features"])
    first = SHOWROOM[0]
    show_btns = "".join(f'<button data-src="{{up}}assets/models/{d}/model.gltf"{" class=on" if i == 0 else ""}>{img(f"assets/3d/{d}.webp", n)}'
                        f'<span><b>{e(n)}</b><small>glTF · PBR</small></span></button>' for i, (d, _, n) in enumerate(SHOWROOM))
    return f"""{slices(lead, items)}<main class="wrap">
<div class="lab-h rv" id="play"><h2>Character <span>playground</span></h2><p>Drag to orbit, pick an animation, play with facial expressions, then drive with <b>W A S D</b> or the arrow keys and collect the orbs.</p></div>
<div id="playground" class="rv" tabindex="0" data-model="{{up}}assets/models/RobotExpressive.glb" aria-label="Interactive 3D character playground">
<canvas></canvas><div class="loading">loading 3D…</div>
<div class="pg-panel"><small>Animations</small><div data-anims></div><small style="margin-top:12px">Expressions</small><div data-faces></div></div>
<div class="pg-score">orbs <b data-score>0</b></div><div class="pg-hint" data-hint>hover here · W A S D to drive</div>
<div class="pad"><button data-pad="f" aria-label="forward">▲</button><button data-pad="l" aria-label="left">◀</button><button data-pad="b" aria-label="back">▼</button><button data-pad="r" aria-label="right">▶</button></div>
</div>
<div class="lab-h rv" id="roblox"><h2>My <span>Roblox game</span></h2><p>Designed, built and scripted in Roblox Studio: economy, progression and PvP loops.</p></div>
<div class="rbx rv"><div class="rbx-shots" data-rotate>{shots}<div class="rbx-dots">{dots}</div></div>
<div class="rbx-info"><div class="top">{img("assets/roblox/dino-icon.webp", "Game icon")}<div><h3>{e(ROBLOX['name'])}</h3><small>Roblox · Tycoon / PvP · up to 50 players</small></div></div>
<p>{e(ROBLOX['text'])}</p><ul>{feats}</ul><a class="btn solid" href="{ROBLOX['url']}" target="_blank" rel="noopener">Play on Roblox ↗</a></div></div>
<div class="lab-h rv" id="showroom"><h2>3D <span>showroom</span></h2><p>Photoreal, game-ready glTF models with PBR materials. Drag to rotate, scroll to zoom, switch lighting.</p></div>
<div class="show rv"><div><model-viewer id="mv" src="{{up}}assets/models/{first[0]}/model.gltf" camera-controls auto-rotate auto-rotate-delay="0" rotation-per-second="18deg"
 shadow-intensity="1.1" shadow-softness=".8" exposure="1" environment-image="neutral" interaction-prompt="auto" touch-action="pan-y" alt="Interactive 3D model"></model-viewer>
<div class="show-ctl"><button data-env="neutral" class="on">Studio light</button><button data-env="legacy">Soft light</button><button data-spin class="on">Auto-rotate</button></div></div>
<div class="show-list">{show_btns}</div></div>
<div class="lab-h rv" id="particles-h"><h2>Particle <span>morph lab</span></h2><p>14,000 particles sampled from real 3D meshes, morphing between shapes on a custom shader. Move the pointer through them, click to morph.</p></div>
<div id="particles" class="rv" data-robot="{{up}}assets/models/RobotExpressive.glb" data-dino="{{up}}assets/models/dino.glb" aria-label="Interactive particle morph">
<canvas></canvas><div class="pt-shapes" data-shapes></div><span class="pt-hint">move the pointer · click to morph</span></div>
</main>{contact}
<script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}}}</script>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
<script type="module" src="{{up}}assets/playground.js"></script>
<script type="module" src="{{up}}assets/particles.js"></script>"""


# ------------------------------------------------------------------ design
def design_body(contact):
    lead = """<span class="eyebrow"><i></i>Product design · UI/UX</span><h1>Product design that earns its place.</h1>
<p>I study how the best SaaS products sell themselves, and design interfaces and content that do the same.</p>
<div class="row"><a class="btn solid" href="#cases">Read case studies</a><a class="btn line" href="#experience">Experience</a></div>"""
    items = [(f"{{up}}design/{c['slug']}/", f"assets/case/{c['slug']}-hero.webp", c["product"], c["category"].split(" · ")[0], c["product"],
              c["lede"][:110] + ("…" if len(c["lede"]) > 110 else ""), "top") for c in CASES]
    cases = "".join(f"""<a class="case-c rv" href="{{up}}design/{c['slug']}/"><div class="im">{img(f"assets/case/{c['slug']}-hero.webp", c['product'] + ' homepage')}</div>
<div class="tx"><small>{e(c['category'])} · teardown</small><h3>{e(c['title'])}</h3><p>{e(c['lede'])}</p></div></a>""" for c in CASES)
    xp = "".join(f"<li><time>{t}</time><div><h4>{e(h)}</h4><p>{e(p)}</p></div></li>" for t, h, p, tag in EXPERIENCE)
    return f"""{slices(lead, items)}
<nav class="tabs" aria-label="Sections"><a href="#cases" class="on">Case studies</a><a href="#experience">Experience</a></nav>
<main class="wrap">
<section class="d-sec" id="cases"><div class="d-h rv"><div><span class="eyebrow"><i></i>Product teardowns</span><h2>How great SaaS <span>sells complex products.</span></h2></div>
<p>Five independent studies of product homepages: positioning, hierarchy, proof and the experiments I'd run next.</p></div>
<div class="cases">{cases}</div></section>
<section class="d-sec" id="experience"><div class="d-h rv"><div><span class="eyebrow"><i></i>Experience</span><h2>3 years of <span>experience.</span></h2></div></div>
<ol class="xp rv">{xp}</ol></section>
</main>{contact}"""
