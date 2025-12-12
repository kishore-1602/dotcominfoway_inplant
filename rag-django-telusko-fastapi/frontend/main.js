const askBtn = document.getElementById('ask');
const qEl = document.getElementById('q');
const answerEl = document.getElementById('answer');
const sourcesEl = document.getElementById('sources');


askBtn.onclick = async () => {
const q = qEl.value;
answerEl.textContent = 'Thinking...';
sourcesEl.innerHTML = '';
try {
const res = await fetch('/query', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ q, top_k: 5 })
});
const data = await res.json();
answerEl.textContent = data.answer;
data.sources.forEach(s => {
const li = document.createElement('li');
li.innerHTML = `<a href="${s.video_url}" target="_blank">${s.video_title}</a> - snippet: ${s.text_snippet}`;
sourcesEl.appendChild(li);
});
} catch (err) {
answerEl.textContent = 'Error: ' + err.message;
}
}