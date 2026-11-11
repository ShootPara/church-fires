const articles = [...document.querySelectorAll('article')];
const controls = document.querySelector('#controls');
const pages = document.querySelector('#pages');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const reading = document.querySelector('#reading');
let current = 0;
let continuous = false;
for (const article of articles) {
  pages.add(new Option(article.querySelector('h2').textContent, article.id));
}
function render() {
  const index = articles.findIndex(article => '#' + article.id === location.hash);
  current = Math.max(index, 0);
  for (const [i, article] of articles.entries()) {
    article.hidden = !continuous && i !== current;
    if (i !== current) article.querySelectorAll('audio,video').forEach(media => media.pause());
  }
  pages.selectedIndex = current;
  previous.disabled = current === 0;
  next.disabled = current === articles.length - 1;
  document.querySelector('#position').textContent = continuous ? '' : `Page ${current + 1} of ${articles.length}`;
}
function go(index) {
  if (index >= 0 && index < articles.length) location.hash = articles[index].id;
}
previous.onclick = () => go(current - 1);
next.onclick = () => go(current + 1);
pages.onchange = () => go(pages.selectedIndex);
reading.onclick = () => {
  continuous = !continuous;
  reading.setAttribute('aria-pressed', String(continuous));
  render();
};
window.addEventListener('hashchange', render);
document.addEventListener('keydown', event => {
  if (continuous || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('button,select,input,textarea,a,summary,audio,video,[contenteditable]')) return;
  if (event.key === 'ArrowLeft') go(current - 1);
  if (event.key === 'ArrowRight') go(current + 1);
});
render();
controls.hidden = false;
