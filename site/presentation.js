const shell = document.querySelector('#church-concept');
const slides = [...document.querySelectorAll('.stage')];
const page = document.querySelector('#page');
const chapter = document.querySelector('#chapter');
const read = document.querySelector('#read');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const fullscreen = document.querySelector('#fullscreen');
const continuous = document.querySelector('#continuous');
let index = 0;
let paged = true;
document.querySelectorAll('[data-video]').forEach(button => {
 button.onclick = () => {
  document.querySelectorAll('audio,video').forEach(media => media.pause());
  const frame = document.createElement('iframe');
  frame.src = button.dataset.video;
  frame.title = button.getAttribute('aria-label');
  frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
  frame.allowFullscreen = true;
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  button.hidden = true;
  button.parentElement.prepend(frame);
 };
});
const narration = document.querySelector('#narration');
const recording = document.querySelector('#recording');
const icons = {
 previous: '<path d="m15 5-7 7 7 7"/>', next: '<path d="m9 5 7 7-7 7"/>',
 fullscreen: '<path d="M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6"/>',
 exit: '<path d="M3 9h6V3m6 0v6h6M9 21v-6H3m12 6v-6h6"/>',
 speaker: '<path d="M3 9h4l5-4v14l-5-4H3zM16 8a6 6 0 0 1 0 8M19 5a10 10 0 0 1 0 14"/>'
};
function icon(button, name, label) {
 button.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${icons[name]}</svg>`;
 button.setAttribute('aria-label', label); button.title = label;
}
icon(previous, 'previous', 'Previous slide'); icon(next, 'next', 'Next slide');
icon(narration, 'speaker', 'Play narration');
function currentAudio() { return slides[index].querySelectorAll('audio')[Number(recording.value) || 0]; }
function audioState() {
 const playing = currentAudio() && !currentAudio().paused;
 for (const button of [narration, ...slides[index].querySelectorAll('[data-narration]')]) {
  button.setAttribute('aria-pressed', String(Boolean(playing)));
  const label = (playing ? 'Pause narration' : 'Play narration') + (index === 0 ? ' (AI-generated voice)' : '');
  button.setAttribute('aria-label', label);
  button.title = label;
 }
}
async function toggleAudio() {
 const audio = currentAudio(); if (!audio) return;
 if (!audio.paused) audio.pause();
 else { document.querySelectorAll('audio,video').forEach(other => { if (other !== audio) other.pause(); });
  try { await audio.play(); } catch { document.querySelector('#status').textContent = 'Audio could not play. Please try again.'; }
 }
 audioState();
}
narration.onclick = toggleAudio;
document.querySelectorAll('[data-narration]').forEach(button => button.onclick = toggleAudio);
document.querySelectorAll('audio').forEach(audio => ['play','pause','ended'].forEach(event => audio.addEventListener(event, audioState)));
function transcriptChoice() {
 slides.forEach(slide => slide.querySelectorAll('[data-transcript]').forEach(part => {
  part.hidden = paged && Number(part.dataset.transcript) !== (Number(recording.value) || 0);
 }));
}
recording.onchange = () => { slides[index].querySelectorAll('audio').forEach(audio => audio.pause()); audioState(); transcriptChoice(); };

function render() {
  document.querySelectorAll('.external-video iframe').forEach(frame => frame.remove());
  document.querySelectorAll('[data-video]').forEach(button => button.hidden = false);
  index = Math.max(0, slides.findIndex(slide => '#' + slide.id === location.hash));
  shell.classList.toggle('is-paged', paged);
  for (const [i, slide] of slides.entries()) {
    slide.hidden = paged && i !== index;
    const text = slide.querySelector('.transcript');
    if (text) text.hidden = paged;
    slide.querySelectorAll('audio, video').forEach(media => media.pause());
  }
  const number = index + 1;
  page.value = String(number);
  chapter.value = [...chapter.options].reverse().find(option => Number(option.value) <= number).value;
  previous.disabled = !paged || index === 0;
  next.disabled = !paged || index === slides.length - 1;
  read.disabled = !paged || !slides[index].querySelector('.transcript');
  read.setAttribute('aria-expanded', 'false');
  read.textContent = 'Read article';
  const tracks = [...slides[index].querySelectorAll('audio')];
  recording.replaceChildren(...tracks.map((audio, i) => new Option(audio.dataset.title, String(i))));
  recording.hidden = tracks.length < 2 || !paged;
  narration.disabled = !paged || tracks.length === 0;
  audioState();
  transcriptChoice();
  continuous.setAttribute('aria-pressed', String(!paged));
  document.querySelector('#status').textContent = `Slide ${number} of ${slides.length}`;
}
function go(number) {
  if (number < 1 || number > slides.length) return;
  paged = true;
  history.pushState(null, '', '#slide-' + number);
  render();
}
previous.onclick = () => go(index);
next.onclick = () => go(index + 2);
page.onchange = () => go(Number(page.value));
chapter.onchange = () => go(Number(chapter.value));
continuous.onclick = async () => {
  if (document.fullscreenElement === shell) await document.exitFullscreen();
  shell.classList.remove('expanded');
  paged = !paged;
  render();
};
read.onclick = () => {
  const text = slides[index].querySelector('.transcript');
  text.hidden = !text.hidden;
  read.textContent = text.hidden ? 'Read article' : 'Close article';
  read.setAttribute('aria-expanded', String(!text.hidden));
};
fullscreen.onclick = async () => {
  if (document.fullscreenElement === shell) return document.exitFullscreen();
  if (shell.classList.contains('expanded')) {
    shell.classList.remove('expanded');
  } else {
    paged = true;
    render();
    try { await shell.requestFullscreen(); }
    catch { shell.classList.add('expanded'); }
  }
  updateFullscreenLabel();
};
function updateFullscreenLabel() {
  const expanded = document.fullscreenElement === shell || shell.classList.contains('expanded');
  icon(fullscreen, expanded ? 'exit' : 'fullscreen', expanded ? 'Exit fullscreen' : 'Fullscreen');
}
document.addEventListener('fullscreenchange', updateFullscreenLabel);
window.addEventListener('popstate', render);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    shell.classList.remove('expanded');
    updateFullscreenLabel();
  }
  if (!paged || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('button,select,a,input,audio,video')) return;
  if (event.key === 'ArrowLeft') go(index);
  if (event.key === 'ArrowRight') go(index + 2);
});
render();
updateFullscreenLabel();
shell.querySelector('footer').hidden = false;
