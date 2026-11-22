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
