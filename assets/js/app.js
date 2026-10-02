(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const button = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  function closeMenu() { nav.classList.remove('open'); button.setAttribute('aria-expanded', 'false'); button.setAttribute('aria-label', 'Open navigation'); }
  button.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); button.focus(); } });
  document.addEventListener('click', e => { if (!e.target.closest('.nav-shell')) closeMenu(); });
  const mobile = matchMedia('(max-width:760px)');
  const details = document.querySelector('.contents details');
  details.open = !mobile.matches;
  const toc = [...document.querySelectorAll('.contents nav a')];
  const search = document.getElementById('contents-search');
  search.addEventListener('input', () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    toc.forEach(a => { a.hidden = !a.dataset.title.includes(query); if (!a.hidden) count++; });
    document.getElementById('no-sections').hidden = count !== 0;
  });
  toc.forEach(a => a.addEventListener('click', () => { if (mobile.matches) details.open = false; }));
  const article = document.getElementById('source-article');
  const headings = [...article.querySelectorAll('h2')];
  const progress = document.getElementById('reading-progress');
  const label = document.getElementById('reading-label');
  let ticking = false;
  let activeId = '';
  function update() {
    const start = article.getBoundingClientRect().top + window.scrollY;
    const end = start + article.offsetHeight - window.innerHeight;
    const percentage = Math.max(0, Math.min(100, (window.scrollY - start) / Math.max(1, end - start) * 100));
    progress.style.width = `${percentage}%`;
    label.textContent = percentage < 1 ? 'Ready to begin' : `${Math.round(percentage)}% through the guide`;
    let current = headings[0];
    for (const h of headings) { if (h.getBoundingClientRect().top <= 180) current = h; else break; }
    if (current && current.id !== activeId) {
      activeId = current.id;
      toc.forEach(a => { if (a.hash === `#${activeId}`) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
    }
    ticking = false;
  }
  function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  document.getElementById('year').textContent = new Date().getFullYear();
  schedule();
})();
