const noteStorageKey = 'community-compass-notes';

// --- Testable helpers (pure-ish, exported for Vitest) ---
// These look up DOM nodes at call time (not import time) so they stay
// import-safe in Node and work against whatever document is current.

export function setFontSize(delta) {
  const root = document.documentElement;
  const current = parseFloat(window.getComputedStyle(root).fontSize);
  root.style.fontSize = `${Math.max(14, Math.min(22, current + delta))}px`;
}

export function calculateRiskPercentage(score) {
  return Math.min(100, Math.max(10, Math.round((score / 18) * 100)));
}

export function saveNotes() {
  const noteText = document.getElementById('noteText');
  localStorage.setItem(noteStorageKey, noteText.value);
}

export function loadNotes() {
  const noteText = document.getElementById('noteText');
  const saved = localStorage.getItem(noteStorageKey);
  if (saved) noteText.value = saved;
}

// --- Browser wiring ---
// All DOM event wiring lives in init() so importing this module in Node
// (for tests) does not execute browser-only code. init() runs only when a
// real document with the dashboard markup is present.

function init() {
  const buttons = {
    decreaseFont: document.getElementById('decrease-font'),
    increaseFont: document.getElementById('increase-font'),
    toggleContrast: document.getElementById('toggle-contrast'),
    saveNote: document.getElementById('saveNote'),
    emailNotes: document.getElementById('emailNotes'),
  };

  const panelTabs = document.querySelectorAll('.panel-tab');
  const panelSections = document.querySelectorAll('[data-panel-content]');
  const pills = document.querySelectorAll('.pill');
  const listingCards = document.querySelectorAll('.listing-card');
  const listingDetail = document.getElementById('listingDetail');
  const options = document.querySelectorAll('.questionnaire-card .option');
  const riskScore = document.getElementById('riskScore');
  const scoreFill = document.getElementById('scoreFill');
  const resourceTabs = document.querySelectorAll('.resource-tabs .tab');

  buttons.decreaseFont.addEventListener('click', () => setFontSize(-1));
  buttons.increaseFont.addEventListener('click', () => setFontSize(1));
  buttons.toggleContrast.addEventListener('click', () => {
    document.documentElement.classList.toggle('high-contrast');
  });

  panelTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      panelTabs.forEach((item) => item.classList.remove('active'));
      panelSections.forEach((section) => section.classList.add('hidden'));
      tab.classList.add('active');
      document.querySelector(`[data-panel-content="${tab.dataset.panel}"]`).classList.remove('hidden');
    });
  });

  pills.forEach((pill) => {
    pill.addEventListener('click', () => {
      pills.forEach((item) => item.classList.remove('active'));
      pill.classList.add('active');
      const filter = pill.dataset.filter;
      listingCards.forEach((card) => {
        card.style.display = (filter === 'all' || card.dataset.category === filter) ? 'flex' : 'none';
      });
    });
  });

  document.querySelectorAll('[data-action="details"]').forEach((button) => {
    button.addEventListener('click', () => {
      const parent = button.closest('.listing-card');
      const title = parent.querySelector('h4').textContent;
      listingDetail.querySelector('h3').textContent = title;
      listingDetail.querySelector('.chip').textContent = `Match score ${parent.querySelector('strong').textContent}`;
    });
  });

  document.querySelectorAll('[data-action="tour"]').forEach((button) => {
    button.addEventListener('click', () => alert('Tour scheduled! We will follow up with the provider details.'));
  });

  document.querySelectorAll('[data-action="email"]').forEach((button) => {
    button.addEventListener('click', () => alert('Email drafted. You can personalize it and send it to yourself.'));
  });

  document.querySelectorAll('[data-action="save"]').forEach((button) => {
    button.addEventListener('click', () => alert('Saved to your My Items list.'));
  });

  function updateRiskScore() {
    const selected = Array.from(options).filter((option) => option.classList.contains('active'));
    const score = selected.reduce((sum, option) => sum + Number(option.dataset.score), 0);
    riskScore.textContent = score;
    scoreFill.style.width = `${calculateRiskPercentage(score)}%`;
  }

  options.forEach((option) => {
    option.addEventListener('click', () => {
      options.forEach((item) => item.classList.remove('active'));
      option.classList.add('active');
      updateRiskScore();
    });
  });

  buttons.saveNote.addEventListener('click', () => {
    saveNotes();
    alert('Notes saved.');
  });

  buttons.emailNotes.addEventListener('click', () => {
    alert('A note email draft is ready for you to send.');
  });

  resourceTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      resourceTabs.forEach((item) => item.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  loadNotes();
  updateRiskScore();

  if (!listingDetail.querySelector('.chip')) {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = 'Match score 92%';
    listingDetail.querySelector('.detail-card-header').appendChild(chip);
  }
}

if (typeof document !== 'undefined' && document.getElementById('decrease-font')) {
  init();
}
