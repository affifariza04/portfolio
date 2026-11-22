// Progressive enhancement only: every page works without JS.
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// reveal on scroll
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.rv').forEach(el => io.observe(el));

// tilt cards (3D page)
if (!reduce && matchMedia('(hover:hover)').matches) {
  document.querySelectorAll('.tilt').forEach(el => {
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = `perspective(900px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg) translateZ(0)`;
    });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });
}

// typed prompt (software page)
const typed = document.querySelector('[data-type]');
if (typed && !reduce) {
  const text = typed.dataset.type; typed.textContent = '';
  let i = 0; const t = setInterval(() => { typed.textContent = text.slice(0, ++i); if (i >= text.length) clearInterval(t); }, 45);
}

// lightbox
const lb = document.createElement('div'); lb.className = 'lb'; lb.innerHTML = '<img alt="">'; document.body.append(lb);
document.addEventListener('click', e => {
  const z = e.target.closest('[data-zoom]');
  if (z) { e.preventDefault(); lb.querySelector('img').src = z.dataset.zoom; lb.querySelector('img').alt = z.querySelector('img')?.alt || ''; lb.classList.add('on'); }
  else if (e.target.closest('.lb')) lb.classList.remove('on');
});
addEventListener('keydown', e => { if (e.key === 'Escape') lb.classList.remove('on'); });

// active tab on the design page
const tabs = document.querySelectorAll('.tabs a');
if (tabs.length) {
  const secs = [...tabs].map(a => document.querySelector(a.getAttribute('href')));
  addEventListener('scroll', () => {
    let k = 0; secs.forEach((s, i) => { if (s && s.getBoundingClientRect().top < 200) k = i; });
    tabs.forEach((a, i) => a.classList.toggle('on', i === k));
  }, { passive: true });
}

// reels: play on hover
document.querySelectorAll('.reel video').forEach(v => {
  v.closest('.phone').addEventListener('pointerenter', () => v.play().catch(() => {}));
  v.closest('.phone').addEventListener('pointerleave', () => v.pause());
});

// home: Kartel-style cylinder reel (auto-spin, drag/swipe with inertia, pauses on hover)
const wrap = document.querySelector('[data-cyl]');
if (wrap) {
  const cyl = wrap.querySelector('.cyl');
  let angle = 0, vel = reduce ? 0 : -0.07, dragging = false, lastX = 0, moved = 0, hover = false;
  const auto = reduce ? 0 : -0.07;
  wrap.addEventListener('pointerenter', () => { hover = true; });
  wrap.addEventListener('pointerleave', () => { hover = false; });
  wrap.addEventListener('pointerdown', ev => { dragging = true; lastX = ev.clientX; moved = 0; });
  wrap.addEventListener('dragstart', ev => ev.preventDefault());
  wrap.addEventListener('pointermove', ev => {
    if (!dragging) return;
    const dx = ev.clientX - lastX; lastX = ev.clientX; moved += Math.abs(dx);
    if (moved > 6 && !wrap.hasPointerCapture(ev.pointerId)) wrap.setPointerCapture(ev.pointerId);
    angle += dx * 0.18; vel = dx * 0.18;
  });
  const end = () => { dragging = false; };
  wrap.addEventListener('pointerup', end); wrap.addEventListener('pointercancel', end);
  wrap.addEventListener('click', ev => { if (moved > 6) { ev.preventDefault(); ev.stopPropagation(); } }, true);
  const n = cyl.children.length;
  (function tick() {
    if (!dragging) {
      const target = hover ? 0 : auto;
      vel += (target - vel) * 0.04;
      angle += vel;
    }
    cyl.style.transform = `translateZ(calc(var(--r) * -1)) rotateY(${angle}deg)`;
    // fade cards that face away so the back of the reel stays readable
    for (let i = 0; i < n; i++) {
      const a = ((i * 360 / n + angle) % 360 + 360) % 360;
      const front = Math.cos(a * Math.PI / 180);
      cyl.children[i].style.opacity = (0.18 + 0.82 * Math.max(0, front) ** 0.8).toFixed(3);
      cyl.children[i].style.pointerEvents = front > 0.2 ? 'auto' : 'none';
    }
    requestAnimationFrame(tick);
  })();
}

// 3D page: Roblox screenshot rotator
document.querySelectorAll('[data-rotate]').forEach(box => {
  const imgs = box.querySelectorAll('img'), dots = box.querySelectorAll('.rbx-dots i');
  let k = 0;
  setInterval(() => {
    imgs[k].classList.remove('on'); dots[k]?.classList.remove('on');
    k = (k + 1) % imgs.length;
    imgs[k].classList.add('on'); dots[k]?.classList.add('on');
  }, 3800);
});

// 3D page: showroom switcher
const mv = document.querySelector('#mv');
if (mv) {
  document.querySelectorAll('.show-list button').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('.show-list button').forEach(x => x.classList.toggle('on', x === b));
    mv.src = b.dataset.src;
  }));
  document.querySelectorAll('[data-env]').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('[data-env]').forEach(x => x.classList.toggle('on', x === b));
    mv.environmentImage = b.dataset.env;
  }));
  const spin = document.querySelector('[data-spin]');
  spin?.addEventListener('click', () => { mv.autoRotate = !mv.autoRotate; spin.classList.toggle('on', mv.autoRotate); });
}

// slices hero: always open at the lead panel on small screens
document.querySelectorAll('.slices').forEach(s => { s.scrollLeft = 0; requestAnimationFrame(() => { s.scrollLeft = 0; }); });
