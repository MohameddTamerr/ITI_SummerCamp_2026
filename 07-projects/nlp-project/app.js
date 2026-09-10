// ── Helpers ───────────────────────────────────────────────────────────────────

function getApiUrl() {
  return document.getElementById('api-url').value.trim().replace(/\/$/, '');
}

function showError(msg) {
  const bar = document.getElementById('error-bar');
  bar.textContent = '⚠️ ' + msg;
  bar.classList.remove('hidden');
}

function clearError() {
  document.getElementById('error-bar').classList.add('hidden');
}

function setLoading(on) {
  const btn = document.getElementById('predict-btn');
  document.getElementById('btn-text').textContent = on ? 'Analyzing…' : 'Analyze Text';
  btn.disabled = on;
}

function setDot(state) {            // 'idle' | 'ok' | 'error'
  const dot = document.getElementById('health-dot');
  dot.className = `dot dot--${state}`;
}


// ── Character counter ─────────────────────────────────────────────────────────

document.getElementById('text-input').addEventListener('input', function () {
  document.getElementById('char-count').textContent = this.value.length + ' chars';
});


// ── Health check ──────────────────────────────────────────────────────────────

async function checkHealth() {
  clearError();
  setDot('idle');
  const url = getApiUrl();
  if (!url) { showError('Enter the API URL first.'); return; }

  try {
    const res = await fetch(`${url}/health`);
    setDot(res.ok ? 'ok' : 'error');
    if (!res.ok) showError(`Server replied with status ${res.status}`);
  } catch {
    setDot('error');
    showError('Could not reach the server. Is uvicorn running?');
  }
}


// ── Predict ───────────────────────────────────────────────────────────────────

async function predict() {
  clearError();
  const url = getApiUrl();
  const text = document.getElementById('text-input').value.trim();

  if (!url) { showError('Enter the API URL first.'); return; }
  if (!text) { showError('Please enter some text to analyze.'); return; }
  if (text.length < 10) { showError('Text is too short — enter at least 10 characters.'); return; }

  setLoading(true);

  try {
    const res = await fetch(`${url}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Server error (${res.status})`);
    }

    showResult(await res.json());

  } catch (err) {
    showError(err.message || 'Something went wrong. Check the server and try again.');
  } finally {
    setLoading(false);
  }
}


// ── Render result ─────────────────────────────────────────────────────────────

function showResult(data) {
  // data = { label: "AI-generated" | "Human-written", confidence: 0–1 }
  const isAI = data.label === 'AI-generated';

  // AI likelihood: if AI → confidence is P(AI); if Human → AI% = 1 - confidence
  const aiPct = isAI ? data.confidence * 100 : (1 - data.confidence) * 100;

  // Hide placeholder, show result
  document.getElementById('placeholder').classList.add('hidden');
  const resultEl = document.getElementById('result-section');
  resultEl.classList.remove('hidden');

  // Badge
  const badge = document.getElementById('result-badge');
  badge.textContent = isAI ? '🤖 AI-Generated' : '✍️ Human-Written';
  badge.className = 'result-badge ' + (isAI ? 'ai' : 'human');

  // Big percentage
  document.getElementById('result-pct').textContent = aiPct.toFixed(1) + '%';

  // Re-trigger animation
  resultEl.style.animation = 'none';
  resultEl.offsetHeight;            // reflow
  resultEl.style.animation = '';
}


// ── Ctrl + Enter shortcut ─────────────────────────────────────────────────────

document.getElementById('text-input').addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && e.ctrlKey) predict();
});
