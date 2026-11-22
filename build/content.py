"""Site content. Edit here, then run `python build/build.py`."""

SITE = "https://affifariza04.github.io/portfolio/"
NAME = "Affif Ariza Adiwijaya"
EMAIL = "affifariza04@gmail.com"
LINKS = {
    "GitHub": "https://github.com/affifariza04",
    "LinkedIn": "https://www.linkedin.com/in/affif-ariza-adiwijaya-75b89027a",
    "Freelancer": "https://www.freelancer.com/u/affifarizaa",
}
STATS = [("50+", "projects delivered"), ("3 yrs", "design & development"), ("6", "contest wins"), ("1.5 yrs", "Odoo / ERP")]

# ------------------------------------------------------------------ Software & AI
FEATURED = [
    {"slug": "docflow", "title": "docflow", "kind": "Document AI · FastAPI + React/TS",
     "text": "Claude reads supplier invoices into a typed schema; one rule set, in Python and TypeScript and tested against shared vectors, "
             "catches mistakes on the document; approval stays blocked until a person resolves them; Odoo gets a vendor bill.",
     "img": "assets/ai/docflow.webp", "live": "https://affifariza04.github.io/docflow/", "code": "https://github.com/affifariza04/docflow",
     "tags": ["Claude vision", "structured outputs", "human-in-the-loop", "Odoo"]},
    {"slug": "evalgate", "title": "evalgate", "kind": "LLM evals · CI gate",
     "text": "Unit tests for prompts: YAML suites, rule + LLM-judge graders, paired McNemar statistics and critical checks, so CI blocks a prompt "
             "that scores the same but breaks policy.",
     "img": "assets/ai/evalgate.webp", "live": "https://affifariza04.github.io/evalgate/", "code": "https://github.com/affifariza04/evalgate",
     "tags": ["evals", "LLM-as-judge", "statistics", "GitHub Actions"]},
    {"slug": "odoo-mcp", "title": "odoo-mcp", "kind": "MCP server · Python",
     "text": "Gives AI agents guarded access to an Odoo ERP: typed business tools, read-only by default, model and field allow-lists, and writes "
             "that a human confirms through the 2026 MCP elicitation flow.",
     "code": "https://github.com/affifariza04/odoo-mcp", "tags": ["MCP SDK 2.x", "agents", "guardrails", "ERP"],
     "snippet": [("$", "uv run python examples/demo.py"), ("›", "overdue_invoices(as_of=\"2026-11-22\")"),
                 ("", "INV/2026/0004  PT Sinar Retail    51 days   12,540,000"), ("?", "Create a draft quotation for Hotel Arunika?"),
                 ("✓", "S00013 · draft · 7,940,000")]},
    {"slug": "lumen", "title": "lumen-configurator", "kind": "three.js · TypeScript",
     "text": "Real-time 3D product configurator: procedural lathe modelling, PBR materials, day/night lighting, shareable configs and PNG export.",
     "img": "assets/3d/lumen-night.webp", "live": "https://affifariza04.github.io/lumen-configurator/",
     "code": "https://github.com/affifariza04/lumen-configurator", "tags": ["three.js", "WebGL", "Vitest", "CI/CD"]},
]
REPOS = [
    ("storefront", "Next.js 16 + PostgreSQL", "E-commerce with oversell-safe checkout and idempotent payment webhooks"),
    ("ragkit", "Python", "Hybrid-search RAG with cited answers and a retrieval eval harness"),
    ("agentloop", "TypeScript", "Provider-agnostic agent runtime with Zod-typed tools"),
    ("llm-gateway", "Python", "OpenAI-compatible gateway: failover, budgets, streaming, metrics"),
    ("pulse", "WebSockets", "Real-time chat with presence and exactly-once storage"),
    ("taskflow", "React + Express + Flutter", "Kanban app with JWT auth and a mobile client"),
    ("bizchat", "JavaScript", "Customer-service bot with human hand-off"),
    ("raft-kv", "TypeScript", "Raft consensus verified with deterministic simulation"),
    ("platform", "Terraform / K8s", "AWS EKS, GitOps with Argo CD, SLO alerts"),
    ("order-analytics", "dbt + DuckDB", "Contracted marts and an incremental pipeline"),
    ("churnlab", "Python", "Calibrated churn model served with FastAPI"),
]
STACK = {"languages": "TypeScript, Python, JavaScript, SQL", "frontend": "React, Next.js, three.js, Vite",
         "backend": "FastAPI, Node/Express, PostgreSQL", "ai": "Claude API, MCP, RAG, evals, structured outputs",
         "erp": "Odoo (1.5 yrs), WooCommerce", "ops": "Docker, GitHub Actions, Terraform"}

# ------------------------------------------------------------------ 3D & game
ROBLOX = {"name": "Revive & Steal a Dino", "url": "https://www.roblox.com/games/108232369899456",
          "text": "A Roblox tycoon I designed and scripted: dig up bones across five habitats, revive dinosaurs in the lab (some come back "
                  "mutated: Golden, Lava, Galaxy, Rainbow), earn coins every second, upgrade your base, then sneak into other bases to "
                  "steal their dinos while keeping yours locked. Trading and daily gifts keep players coming back.",
          "features": ["Bone digging across Desert, Jungle, Glacier, Volcano and Coral Reef", "Revive lab with mutation rarities",
                       "Idle income and base upgrades", "Base stealing and locking (PvP)", "Trading and daily rewards"],
          "shots": ["dino-1", "dino-2", "dino-3"]}
SHOWROOM = [("camera_01", "Camera_01", "Rangefinder camera"), ("vintage_electric_kettle", "vintage_electric_kettle", "Vintage kettle"),
            ("mid_century_lounge_chair", "mid_century_lounge_chair", "Lounge chair"), ("brass_vase_03", "brass_vase_03", "Brass vase"),
            ("coffeecart_01", "CoffeeCart_01", "Coffee cart")]

EXPERIENCE = [
    ("Jul 2026 — now", "UI/UX Designer & Web Developer · Gold Coffee Company",
     "Amazon storefront (home + 6 category pages) and the brand website on one Figma design system.", "design"),
    ("Aug 2025 — Oct 2026", "Product, Web & Video Designer · Techno Global Inc.",
     "WortixEV 3D vehicle models, SWEVEN app redesign (contest win), 33 product videos, corporate site with 7 sector pages.", "design 3d"),
    ("Jun 2025 — now", "Freelance Designer, 3D & Developer · Freelancer.com",
     "30+ projects: three.js configurator, permit drawings, retail interiors (2 wins), identities, product videos (2 wins).", "code 3d design"),
    ("6 months", "Social Media Content Intern · Traveloka",
     "Reels and TikToks end to end: concept, script, shoot direction, edit and captions.", "design"),
    ("1.5 years", "Odoo / ERP", "Configuring and customising Odoo modules and business workflows.", "code"),
    ("2024 — now", "B.Sc. Information Systems & Technology · UHAMKA",
     "Web programming, distributed systems, network security; research on AI-supported learning.", "code"),
]

# ------------------------------------------------------------------ Case studies (independent teardowns)
CASES = [
    {"slug": "attio", "product": "Attio", "url": "https://attio.com/", "category": "CRM · B2B SaaS",
     "title": "Attio: selling an AI-native CRM in one line",
     "lede": "How Attio's homepage reframes a crowded category (CRM) as a new one (agentic revenue), and where that bet costs clarity.",
     "audience": "Revenue and GTM teams at startups and scale-ups", "focus": "Positioning, hero hierarchy, product-as-hero",
     "jobs": ["Tell a sales leader in five seconds that this is a CRM, but a new kind",
              "Make AI feel like part of the daily workflow, not a bolt-on",
              "Offer a self-serve path and a sales path without either competing"],
     "works": [("Product as the hero image", "The visual is the real app, a deal page with an AI thread asking how to win the GreenLeaf deal, "
                "rather than an illustration. It shows the promise instead of describing it."),
               ("A clear two-CTA hierarchy", "“Start for free” is the only filled button; “Talk to sales” sits next to it in outline. "
                "Both buyer types get a path and the product-led one wins visually."),
               ("Freshness signals above the fold", "An announcement bar and a small pill (“GTM lessons from…”) tell returning visitors "
                "something is new without moving the headline."),
               ("Restraint as a trust signal", "A near-monochrome palette, generous whitespace and one soft lavender gradient read as "
                "enterprise-grade and leave all the colour to the product UI.")],
     "friction": [("Category language before category", "“Welcome to agentic revenue” is memorable, but a first-time visitor has to "
                   "read the subcopy to learn it is a CRM. New categories need an anchor in the old one."),
                  ("The proof sits below the fold", "At a 1440 × 900 viewport the product window starts below the fold, so the "
                   "first screen is all words and the strongest asset waits for a scroll.")],
     "tests": [("Anchor the category in the H1", "“The AI-native CRM for agentic revenue” vs the current headline",
                "Start-for-free click-through; scroll depth to the product frame"),
               ("Pull the product frame up", "Start the app window inside the first viewport, overlapping the hero",
                "Time to first interaction; bounce rate on paid traffic")],
     "takeaway": "When you name a new category, keep one foot in the old one. Show the product in the first screen; it argues better than copy."},
    {"slug": "tally", "product": "Tally", "url": "https://tally.so/", "category": "Form builder · PLG",
     "title": "Tally: personality in a commodity category",
     "lede": "Form builders all promise the same thing. Tally competes on feel: doodles, a doc-like editor and a pricing promise in the hero.",
     "audience": "Makers, founders and small teams", "focus": "Differentiation, friction removal, mental model",
     "jobs": ["Stand out against Google Forms and Typeform at first glance",
              "Make building a form feel as easy as typing a document",
              "Remove every reason not to try it now"],
     "works": [("Illustration as differentiation", "Hand-drawn faces, speech bubbles and a scribbled underline under “simplest” give a "
                "commodity product a voice. The line art is light enough not to fight the CTA."),
               ("The preview is the mental model", "The hero shows the editor itself: a “Customer feedback” title, a slash prompt and a "
                "submit button. It reads like a document, which is the whole idea."),
               ("Friction removed in microcopy", "“No signup required” under “Create a free form” answers the main objection exactly "
                "where the decision happens."),
               ("Pricing as a feature", "“Unlimited forms and submissions for free” gets its own highlighted card early, turning the "
                "business model into a selling point. Privacy (hosted in Europe, GDPR) follows for teams that need it.")],
     "friction": [("Long, even rhythm", "Many feature cards share the same weight, so after the hero the page loses a clear story arc "
                   "and scanning visitors may miss the strongest points."),
                  ("Logos without numbers", "“Powering 2,500,000+ teams” is strong; the logo strip under it is small and grey, so "
                   "recognisable brands like Notion get little attention.")],
     "tests": [("Try it in the hero", "Let visitors type a question into the hero editor vs the static preview",
                "Forms created in the first session"),
               ("Group features into three acts", "Build · Share · Analyse sections vs the current flat card list",
                "Scroll depth; sign-up rate from the features area")],
     "takeaway": "In a crowded category, the feel of a product is a feature. Put the objection-killer right under the button."},
    {"slug": "sunsama", "product": "Sunsama", "url": "https://sunsama.com/", "category": "Productivity · daily planner",
     "title": "Sunsama: selling a feeling, not a feature list",
     "lede": "Sunsama positions a task planner around calm instead of productivity. The page is built as a before-and-after story.",
     "audience": "Professionals overwhelmed by tasks, meetings and tools", "focus": "Emotional positioning, narrative structure, voice",
     "jobs": ["Make an overwhelmed professional feel understood",
              "Explain a daily ritual (plan, focus, review) without a manual",
              "Lower the risk of trying a paid tool"],
     "works": [("A headline that is the product", "“Start Calm. Stay Focused. End Confident.” maps one-to-one onto the daily ritual: "
                "plan in the morning, focus during the day, review at night."),
               ("Problem, then solution, side by side", "A card titled “Work is f***ing chaotic” lists pains with red marks; the next "
                "card answers each with a check and a testimonial. The contrast does the persuading."),
               ("A voice people remember", "The censored swear word is a deliberate brand risk. It signals a human company, and it "
                "filters for the audience that will love the product."),
               ("Risk reversal next to the CTA", "“14-day free trial, no credit card” and “Works with Claude, ChatGPT and more” sit "
                "beside the orange button, answering cost and compatibility at once.")],
     "friction": [("Warm gradient vs product clarity", "The peach gradient sets the mood but the product view is small in the first "
                   "screen, so visitors feel the promise before they see the tool."),
                  ("Social proof is quiet", "Press logos are muted and small; one strong numeric proof point would carry more weight "
                   "next to the headline.")],
     "tests": [("Show the daily ritual", "A 3-step animated strip (plan · focus · review) under the headline vs static copy",
                "Trial starts; time on page"),
               ("Lead with a number", "Add one usage or outcome metric beside the CTA",
                "CTA click-through")],
     "takeaway": "When everyone sells features, sell the state your user wants to be in, then prove it with a before-and-after."},
    {"slug": "dovetail", "product": "Dovetail", "url": "https://dovetail.com/", "category": "Customer insight · AI",
     "title": "Dovetail: repositioning a research tool for the agent era",
     "lede": "Dovetail reframes itself from a research repository into a “customer context layer” for AI agents, and leans on bold type and proof to carry it.",
     "audience": "Product, research, CX and revenue leaders", "focus": "Repositioning, trust signals, display typography",
     "jobs": ["Keep research teams while winning new budget from AI initiatives",
              "Prove the product is enterprise-safe and loved",
              "Make an abstract layer feel concrete"],
     "works": [("Repositioned on the AI narrative", "Sales calls, tickets and interviews become “context for agents”, each linked to "
                "evidence and revenue impact. The existing strength (evidence) becomes the answer to AI's weakness (trust)."),
               ("Instant trust in the corner", "G2, Capterra and TrustRadius ratings sit top right, in the eye path, before any scroll."),
               ("Display type with a wink", "“Feed the facts machine” in huge type with a 3D fax machine between the words breaks "
                "enterprise seriousness and makes the abstract idea physical."),
               ("A heavyweight logo wall", "Mercedes-Benz, KPMG, Notion, Salesforce, Dyson, Shopify and Wise close the hero, answering "
                "“who else uses this?” for enterprise buyers.")],
     "friction": [("The value proposition is a paragraph", "The first message is one long sentence in small type on black; the big, "
                   "memorable line appears only further down. Scanners read the logos, not the promise."),
                  ("Low-contrast supporting text", "Grey text on near-black is elegant but harder to read, especially on laptops "
                   "outdoors.")],
     "tests": [("Swap the hierarchy", "Use “Feed the facts machine” as the H1 and the long sentence as subcopy",
                "Demo requests; scroll past the hero"),
               ("Raise contrast", "Lift body text contrast to WCAG AA on the hero",
                "Readability score; CTA click-through on mobile")],
     "takeaway": "A repositioning works best when the old strength becomes the answer to the new market's fear. Say it big, then explain."},
    {"slug": "heptabase", "product": "Heptabase", "url": "https://heptabase.com/", "category": "Knowledge tool · visual thinking",
     "title": "Heptabase: differentiating against AI itself",
     "lede": "Instead of competing on AI features, Heptabase positions against what AI makes too easy, and uses art direction to sell slow, deep thinking.",
     "audience": "Researchers, students and knowledge workers", "focus": "Contrarian positioning, art direction, audience segmentation",
     "jobs": ["Explain why a visual knowledge base matters when AI can just answer",
              "Make a dense, powerful UI feel calm and approachable",
              "Show it works with the sources people already read"],
     "works": [("Contrarian, two-beat headline", "“AI gives you answers. Heptabase builds your worldview.” concedes what AI does well, "
                "then claims the space AI can't own: understanding."),
               ("Painterly art direction", "The product window floats over a sunset landscape. The softness balances a dense UI and "
                "says “thinking”, not “productivity”."),
               ("Segmentation before the headline", "An App / Plugin toggle above the H1 lets two audiences self-select before they "
                "read a word."),
               ("Sources made concrete", "Chips for PDFs, web pages, YouTube, podcasts, Readwise and Zotero turn “import anything” into "
                "a list a reader recognises. Awards and investors (YC, Kleiner Perkins) add proof.")],
     "friction": [("Dense UI at thumbnail size", "Screenshots of whiteboards and tables are hard to read at hero scale; the detail "
                   "that sells the product is too small to see."),
                  ("Toggle with no explanation", "“App” vs “Plugin” is clear to existing users but ambiguous to a newcomer.")],
     "tests": [("Annotated hotspots", "Zoomable hotspots on the hero screenshot explaining 3 key actions",
                "Trial starts; hotspot interaction rate"),
               ("Explain the toggle", "Add a one-line hint (“Use it standalone or inside Claude”) under the toggle",
                "Toggle usage; plugin installs")],
     "takeaway": "You can differentiate against the trend everyone rides. Art direction can make a complex tool feel calm."},
]
