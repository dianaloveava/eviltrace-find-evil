const $ = (id) => document.getElementById(id);
const status = $('status');

$('runButton').addEventListener('click', async () => {
  status.textContent = 'Running bounded read-only investigation...';
  try {
    const run = await request('/api/runs', { method: 'POST' });
    render(run);
    status.textContent = `Completed ${run.id}. Report export is ready.`;
  } catch (error) {
    status.textContent = `Run failed: ${error.message}`;
  }
});

$('loadButton').addEventListener('click', loadLatest);
window.addEventListener('DOMContentLoaded', loadLatest);

async function loadLatest() {
  status.textContent = 'Loading latest run...';
  try {
    const run = await request('/api/runs/latest');
    render(run);
    status.textContent = `Loaded ${run.id}.`;
  } catch {
    status.textContent = 'No run yet. Click Run demo investigation.';
  }
}

async function request(url, options) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || response.statusText);
  return payload;
}

function render(run) {
  $('metricFindings').textContent = String(run.metrics.total_findings);
  $('metricCorrections').textContent = String(run.metrics.total_corrections);
  $('metricEvidence').textContent = String(run.metrics.evidence_refs);
  $('metricPaid').textContent = run.metrics.paid_api_required ? 'Yes' : 'No';
  renderFindings(run.findings);
  renderTimeline(run.steps);
  renderCorrections(run.corrections);
  renderEvidence(run.evidence);
}

function renderFindings(findings) {
  const root = $('findingsList');
  root.className = 'cards';
  root.replaceChildren(...findings.map((finding) => {
    const card = el('article', 'card');
    card.append(
      el('h3', '', finding.title),
      badges([finding.severity, `confidence: ${finding.confidence}`]),
      el('p', '', finding.summary),
      refs(finding.evidence_refs)
    );
    if (finding.caveats?.length) {
      const caveats = el('p', 'step-meta', `Caveats: ${finding.caveats.join(' ')}`);
      card.append(caveats);
    }
    return card;
  }));
}

function renderTimeline(steps) {
  const root = $('timelineList');
  root.className = 'timeline';
  root.replaceChildren(...steps.map((step) => {
    const item = el('li');
    item.append(el('span', 'step-index', String(step.index)));
    const body = el('div');
    body.append(el('strong', '', step.action), el('div', 'step-meta', `${step.phase}${step.tool ? ` · ${step.tool}` : ''}`), el('p', '', step.rationale));
    if (step.result_summary) body.append(el('p', 'step-meta', step.result_summary));
    if (step.evidence_refs?.length) body.append(refs(step.evidence_refs.slice(0, 5)));
    item.append(body);
    return item;
  }));
}

function renderCorrections(corrections) {
  const root = $('correctionsList');
  root.className = 'corrections';
  if (!corrections.length) {
    root.className = 'corrections empty';
    root.textContent = 'No corrections recorded.';
    return;
  }
  root.replaceChildren(...corrections.map((correction) => {
    const card = el('article', 'correction');
    card.append(
      el('strong', '', correction.finding_id),
      el('p', '', `${correction.before_confidence} → ${correction.after_confidence}`),
      el('p', '', correction.reason),
      refs(correction.evidence_refs)
    );
    return card;
  }));
}

function renderEvidence(evidence) {
  const root = $('evidenceList');
  root.className = 'evidence-grid';
  root.replaceChildren(...evidence.map((record) => {
    const card = el('article', 'evidence-card');
    card.append(el('strong', '', record.id), el('p', '', record.description), el('p', 'step-meta', `${record.kind} · ${record.size} bytes`), el('code', '', `${record.path}\n${record.sha256}`));
    return card;
  }));
}

function badges(values) {
  const wrap = el('div', 'badges');
  values.forEach((value) => wrap.append(el('span', `badge ${String(value).split(':')[0]}`, String(value))));
  return wrap;
}

function refs(values) {
  const list = el('ul', 'refs');
  values.forEach((value) => list.append(el('li', '', value)));
  return list;
}

function el(tag, className = '', text = '') {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}
