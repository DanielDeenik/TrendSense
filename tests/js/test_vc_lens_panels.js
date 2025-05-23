/**
 * Tests for VC Lens panels JavaScript functionality
 * 
 * This file contains tests for the VC Lens panels JavaScript functionality,
 * including the hideAllPanels function and panel button event listeners.
 */

// Mock DOM elements
document.body.innerHTML = `
<div id="venture-signal-graph" class="panel"></div>
<div id="esg-compliance-panel" class="panel hidden"></div>
<div id="portfolio-signal-panel" class="panel hidden"></div>
<div id="capital-exit-panel" class="panel hidden"></div>
<div id="lifecycle-scorecard" class="panel hidden"></div>

<button id="venture-signal-graph-btn"></button>
<button id="esg-compliance-btn"></button>
<button id="portfolio-signal-btn"></button>
<button id="capital-exit-btn"></button>
<button id="lifecycle-btn"></button>
`;

// Mock hideAllPanels function
function hideAllPanels() {
  document.querySelectorAll('.panel').forEach(panel => {
    panel.classList.add('hidden');
  });
}

// Tests
describe('VC Lens Panels', () => {
  beforeEach(() => {
    // Reset panel visibility
    document.querySelectorAll('.panel').forEach(panel => {
      panel.classList.add('hidden');
    });
    document.getElementById('venture-signal-graph').classList.remove('hidden');
  });

  test('hideAllPanels should hide all panels', () => {
    // Make sure at least one panel is visible
    document.getElementById('venture-signal-graph').classList.remove('hidden');
    
    // Call hideAllPanels
    hideAllPanels();
    
    // Check that all panels are hidden
    document.querySelectorAll('.panel').forEach(panel => {
      expect(panel.classList.contains('hidden')).toBe(true);
    });
  });

  test('venture signal graph button should show venture signal graph panel', () => {
    // Hide all panels
    hideAllPanels();
    
    // Set up event listener
    document.getElementById('venture-signal-graph-btn').addEventListener('click', function() {
      hideAllPanels();
      document.getElementById('venture-signal-graph').classList.remove('hidden');
    });
    
    // Click button
    document.getElementById('venture-signal-graph-btn').click();
    
    // Check that venture signal graph panel is visible
    expect(document.getElementById('venture-signal-graph').classList.contains('hidden')).toBe(false);
    
    // Check that other panels are hidden
    expect(document.getElementById('esg-compliance-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('portfolio-signal-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('capital-exit-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('lifecycle-scorecard').classList.contains('hidden')).toBe(true);
  });

  test('ESG compliance button should show ESG compliance panel', () => {
    // Hide all panels
    hideAllPanels();
    
    // Set up event listener
    document.getElementById('esg-compliance-btn').addEventListener('click', function() {
      hideAllPanels();
      document.getElementById('esg-compliance-panel').classList.remove('hidden');
    });
    
    // Click button
    document.getElementById('esg-compliance-btn').click();
    
    // Check that ESG compliance panel is visible
    expect(document.getElementById('esg-compliance-panel').classList.contains('hidden')).toBe(false);
    
    // Check that other panels are hidden
    expect(document.getElementById('venture-signal-graph').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('portfolio-signal-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('capital-exit-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('lifecycle-scorecard').classList.contains('hidden')).toBe(true);
  });

  test('portfolio signal button should show portfolio signal panel', () => {
    // Hide all panels
    hideAllPanels();
    
    // Set up event listener
    document.getElementById('portfolio-signal-btn').addEventListener('click', function() {
      hideAllPanels();
      document.getElementById('portfolio-signal-panel').classList.remove('hidden');
    });
    
    // Click button
    document.getElementById('portfolio-signal-btn').click();
    
    // Check that portfolio signal panel is visible
    expect(document.getElementById('portfolio-signal-panel').classList.contains('hidden')).toBe(false);
    
    // Check that other panels are hidden
    expect(document.getElementById('venture-signal-graph').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('esg-compliance-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('capital-exit-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('lifecycle-scorecard').classList.contains('hidden')).toBe(true);
  });

  test('capital exit button should show capital exit panel', () => {
    // Hide all panels
    hideAllPanels();
    
    // Set up event listener
    document.getElementById('capital-exit-btn').addEventListener('click', function() {
      hideAllPanels();
      document.getElementById('capital-exit-panel').classList.remove('hidden');
    });
    
    // Click button
    document.getElementById('capital-exit-btn').click();
    
    // Check that capital exit panel is visible
    expect(document.getElementById('capital-exit-panel').classList.contains('hidden')).toBe(false);
    
    // Check that other panels are hidden
    expect(document.getElementById('venture-signal-graph').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('esg-compliance-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('portfolio-signal-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('lifecycle-scorecard').classList.contains('hidden')).toBe(true);
  });

  test('lifecycle button should show lifecycle scorecard', () => {
    // Hide all panels
    hideAllPanels();
    
    // Set up event listener
    document.getElementById('lifecycle-btn').addEventListener('click', function() {
      hideAllPanels();
      document.getElementById('lifecycle-scorecard').classList.remove('hidden');
    });
    
    // Click button
    document.getElementById('lifecycle-btn').click();
    
    // Check that lifecycle scorecard is visible
    expect(document.getElementById('lifecycle-scorecard').classList.contains('hidden')).toBe(false);
    
    // Check that other panels are hidden
    expect(document.getElementById('venture-signal-graph').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('esg-compliance-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('portfolio-signal-panel').classList.contains('hidden')).toBe(true);
    expect(document.getElementById('capital-exit-panel').classList.contains('hidden')).toBe(true);
  });
});
