// filters
const buttons = document.querySelectorAll('.filters button');
const cases = document.querySelectorAll('.case');
function setFilter(f) {
  buttons.forEach(b => b.classList.toggle('on', b.dataset.f === f));
  cases.forEach(c => c.classList.toggle('hide', f !== 'all' && !c.dataset.c.split(' ').includes(f)));
}
buttons.forEach(b => b.addEventListener('click', () => setFilter(b.dataset.f)));
document.querySelectorAll('.track').forEach(t => t.addEventListener('click', () => {
  setFilter(t.dataset.t);
  document.getElementById('work').scrollIntoView({ behavior: 'smooth' });
}));

// nav border on scroll
const nav = document.querySelector('.nav');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 8), { passive: true });

// reveal on scroll
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
document.querySelectorAll('.track, .case, .exp li, .stats li').forEach(el => { el.classList.add('reveal'); io.observe(el); });
