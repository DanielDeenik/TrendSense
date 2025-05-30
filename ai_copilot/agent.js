// agent.js - AI-Powered UI Co-Pilot Frontend Agent
// v0.1: DOM Inspector, Labeler, Mutation Tracker, Context Snapshot

(function(global) {
  const AGENT_VERSION = '0.1.0';
  const CONTEXT_EVENT = 'ai-copilot-context';

  // Utility: Get all visible elements with semantic meaning
  function getVisibleUIElements() {
    const elements = [];
    const selectors = [
      'button', 'input', 'select', 'textarea', 'a', '[role="button"]', '[role="tab"]', '[role="checkbox"]', '[role="menuitem"]', '[data-ai-label]'
    ];
    document.querySelectorAll(selectors.join(','))
      .forEach(el => {
        if (!el.offsetParent) return; // skip hidden
        const label = el.getAttribute('data-ai-label') || el.innerText || el.value || el.placeholder || el.getAttribute('aria-label') || '';
        elements.push({
          tag: el.tagName.toLowerCase(),
          label: label.trim(),
          id: el.id || null,
          classes: el.className || null,
          rect: el.getBoundingClientRect(),
          attributes: Array.from(el.attributes).reduce((acc, attr) => { acc[attr.name] = attr.value; return acc; }, {})
        });
      });
    return elements;
  }

  // Utility: Take a context snapshot
  function getContextSnapshot() {
    return {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString(),
      elements: getVisibleUIElements(),
      agentVersion: AGENT_VERSION
    };
  }

  // Mutation Observer: Track UI changes
  function setupMutationObserver(onChange) {
    const observer = new MutationObserver((mutations) => {
      onChange(getContextSnapshot());
    });
    observer.observe(document.body, { childList: true, subtree: true, attributes: true });
    return observer;
  }

  // API: Expose context snapshot and event system
  const CopilotAgent = {
    getContextSnapshot,
    onContextChange(callback) {
      setupMutationObserver(callback);
    },
    sendContextToBackend(endpoint, extra={}) {
      const payload = { ...getContextSnapshot(), ...extra };
      return fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }
  };

  // Auto-fire event on context change
  setupMutationObserver((context) => {
    const event = new CustomEvent(CONTEXT_EVENT, { detail: context });
    window.dispatchEvent(event);
  });

  // Attach to window for global access
  global.CopilotAgent = CopilotAgent;

  // Log agent load
  console.info(`[AI Copilot Agent v${AGENT_VERSION}] Loaded.`);

})(window);
