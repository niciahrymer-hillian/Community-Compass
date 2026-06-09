import { beforeEach, describe, expect, it, vi } from 'vitest';
import { JSDOM } from 'jsdom';
import { setFontSize, calculateRiskPercentage, saveNotes, loadNotes } from '../script.js';

describe('Community Compass script helpers', () => {
  beforeEach(() => {
    const dom = new JSDOM(`<!doctype html><html><body><textarea id="noteText"></textarea><div id="listingDetail"></div><div class="listing-card" data-category="section8"><strong>92%</strong></div></body></html>`, { url: 'http://localhost' });
    global.document = dom.window.document;
    global.window = dom.window;
    global.localStorage = dom.window.localStorage;
    global.alert = vi.fn();
  });

  it('adjusts the root font size by the requested delta', () => {
    document.documentElement.style.fontSize = '16px';
    setFontSize(2);
    expect(document.documentElement.style.fontSize).toBe('18px');
  });

  it('calculates a risk percentage from a score value', () => {
    expect(calculateRiskPercentage(9)).toBeGreaterThanOrEqual(10);
    expect(calculateRiskPercentage(18)).toBe(100);
  });

  it('saves notes to localStorage', () => {
    const noteText = document.getElementById('noteText');
    noteText.value = 'Test note';
    saveNotes();
    expect(localStorage.getItem('community-compass-notes')).toBe('Test note');
  });

  it('loads notes from localStorage', () => {
    localStorage.setItem('community-compass-notes', 'Loaded note');
    const noteText = document.getElementById('noteText');
    noteText.value = '';
    loadNotes();
    expect(noteText.value).toBe('Loaded note');
  });
});
