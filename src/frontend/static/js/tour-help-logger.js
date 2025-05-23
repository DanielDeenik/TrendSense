/**
 * TourMode Help Logger
 * 
 * This module provides logging functionality for the TourMode help system.
 * It captures detailed information about the user's environment and tour state
 * to help diagnose and resolve issues.
 */

class TourHelpLogger {
  constructor() {
    this.debugInfo = {};
    this.initialized = false;
    this.issueHistory = [];
    this.maxHistorySize = 10;
  }

  /**
   * Initialize the help logger
   */
  init() {
    if (this.initialized) return;
    
    // Create help button
    this.createHelpButton();
    
    // Load issue history from localStorage
    this.loadIssueHistory();
    
    this.initialized = true;
  }

  /**
   * Create help button
   */
  createHelpButton() {
    // Create button element
    const helpButton = document.createElement('button');
    helpButton.id = 'tour-help-button';
    helpButton.className = 'fixed bottom-6 left-6 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full shadow-lg flex items-center z-50';
    helpButton.innerHTML = `
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Need Help?
    `;
    
    // Add click event listener
    helpButton.addEventListener('click', () => {
      this.collectDebugInfo();
      if (typeof window.openHelpModal === 'function') {
        window.openHelpModal();
      } else {
        console.error('Help modal not found');
      }
    });
    
    // Add to document
    document.body.appendChild(helpButton);
  }

  /**
   * Collect debug information
   */
  collectDebugInfo() {
    this.debugInfo = {
      // Basic information
      url: window.location.href,
      pathname: window.location.pathname,
      timestamp: new Date().toISOString(),
      
      // Browser information
      userAgent: navigator.userAgent,
      screenSize: `${window.innerWidth}x${window.innerHeight}`,
      language: navigator.language,
      cookiesEnabled: navigator.cookieEnabled,
      
      // Tour information
      tourActive: window.tourMode ? window.tourMode.isActive() : false,
      currentStep: window.tourMode ? window.tourMode.currentStep : -1,
      totalSteps: window.tourMode && window.tourMode.tourSteps ? window.tourMode.tourSteps.length : 0,
      tourConfig: window.tourMode && window.tourMode.tourConfig ? window.tourMode.tourConfig.name : 'Unknown',
      
      // Current step information
      currentStepInfo: this.getCurrentStepInfo(),
      
      // DOM information
      visibleElements: this.getVisibleElements(),
      
      // Performance information
      performance: this.getPerformanceInfo(),
      
      // Error information
      recentErrors: this.getRecentErrors(),
      
      // User information (non-identifying)
      userAuthenticated: window.firebase && window.firebase.auth && window.firebase.auth().currentUser ? true : false,
      localStorageAvailable: this.isLocalStorageAvailable(),
      tourCompletedBefore: localStorage.getItem('tourCompleted') === 'true'
    };
    
    // Make debug info available globally
    window.tourDebugInfo = this.debugInfo;
    
    return this.debugInfo;
  }

  /**
   * Get information about the current tour step
   */
  getCurrentStepInfo() {
    if (!window.tourMode || !window.tourMode.tourSteps || !window.tourMode.tourSteps[window.tourMode.currentStep]) {
      return null;
    }
    
    const currentStep = window.tourMode.tourSteps[window.tourMode.currentStep];
    return {
      thinking: currentStep.thinking ? currentStep.thinking.substring(0, 100) + '...' : null,
      highlightSelector: currentStep.highlightSelector,
      elementExists: currentStep.highlightSelector ? !!document.querySelector(currentStep.highlightSelector) : false,
      elementVisible: currentStep.highlightSelector ? this.isElementVisible(document.querySelector(currentStep.highlightSelector)) : false,
      actions: currentStep.actions ? currentStep.actions.length : 0
    };
  }

  /**
   * Get information about visible elements
   */
  getVisibleElements() {
    const visibleElements = [];
    
    // Check tour-related elements
    const tourElements = [
      '#tour-controls',
      '#copilot-cot-tooltip',
      '.tour-navigation',
      '#toggle-tour-btn'
    ];
    
    tourElements.forEach(selector => {
      const element = document.querySelector(selector);
      if (element) {
        visibleElements.push({
          selector,
          visible: !element.classList.contains('hidden'),
          rect: element.getBoundingClientRect()
        });
      }
    });
    
    return visibleElements;
  }

  /**
   * Get performance information
   */
  getPerformanceInfo() {
    if (!window.performance) {
      return null;
    }
    
    return {
      navigation: window.performance.navigation ? {
        type: window.performance.navigation.type,
        redirectCount: window.performance.navigation.redirectCount
      } : null,
      timing: window.performance.timing ? {
        loadTime: window.performance.timing.loadEventEnd - window.performance.timing.navigationStart,
        domReadyTime: window.performance.timing.domComplete - window.performance.timing.domLoading,
        readyStart: window.performance.timing.fetchStart - window.performance.timing.navigationStart,
        redirectTime: window.performance.timing.redirectEnd - window.performance.timing.redirectStart,
        appcacheTime: window.performance.timing.domainLookupStart - window.performance.timing.fetchStart,
        unloadEventTime: window.performance.timing.unloadEventEnd - window.performance.timing.unloadEventStart,
        lookupDomainTime: window.performance.timing.domainLookupEnd - window.performance.timing.domainLookupStart,
        connectTime: window.performance.timing.connectEnd - window.performance.timing.connectStart,
        requestTime: window.performance.timing.responseEnd - window.performance.timing.requestStart,
        initDomTreeTime: window.performance.timing.domInteractive - window.performance.timing.responseEnd,
        loadEventTime: window.performance.timing.loadEventEnd - window.performance.timing.loadEventStart
      } : null
    };
  }

  /**
   * Get recent JavaScript errors
   */
  getRecentErrors() {
    return window.tourErrorLog || [];
  }

  /**
   * Check if localStorage is available
   */
  isLocalStorageAvailable() {
    try {
      const test = 'test';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (e) {
      return false;
    }
  }

  /**
   * Check if an element is visible
   */
  isElementVisible(element) {
    if (!element) return false;
    
    const style = window.getComputedStyle(element);
    if (style.display === 'none') return false;
    if (style.visibility !== 'visible') return false;
    if (style.opacity === '0') return false;
    
    const rect = element.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return false;
    
    return true;
  }

  /**
   * Log an issue
   */
  logIssue(issueData) {
    // Add timestamp and debug info
    const issue = {
      ...issueData,
      timestamp: new Date().toISOString(),
      debugInfo: this.collectDebugInfo()
    };
    
    // Add to issue history
    this.issueHistory.unshift(issue);
    
    // Limit history size
    if (this.issueHistory.length > this.maxHistorySize) {
      this.issueHistory = this.issueHistory.slice(0, this.maxHistorySize);
    }
    
    // Save to localStorage
    this.saveIssueHistory();
    
    // Submit to Firebase if available
    this.submitToFirebase(issue);
    
    return issue;
  }

  /**
   * Load issue history from localStorage
   */
  loadIssueHistory() {
    try {
      const history = localStorage.getItem('tourIssueHistory');
      if (history) {
        this.issueHistory = JSON.parse(history);
      }
    } catch (e) {
      console.error('Error loading issue history:', e);
      this.issueHistory = [];
    }
  }

  /**
   * Save issue history to localStorage
   */
  saveIssueHistory() {
    try {
      localStorage.setItem('tourIssueHistory', JSON.stringify(this.issueHistory));
    } catch (e) {
      console.error('Error saving issue history:', e);
    }
  }

  /**
   * Submit issue to Firebase
   */
  submitToFirebase(issue) {
    if (window.firebase && window.firebase.database) {
      const issuesRef = window.firebase.database().ref('tourIssues');
      issuesRef.push(issue)
        .then(() => {
          console.log('Issue submitted to Firebase');
        })
        .catch(error => {
          console.error('Error submitting issue to Firebase:', error);
        });
    }
  }
}

// Create global error logger
window.tourErrorLog = [];
window.addEventListener('error', function(event) {
  // Add error to log
  window.tourErrorLog.unshift({
    message: event.message,
    source: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    timestamp: new Date().toISOString()
  });
  
  // Limit log size
  if (window.tourErrorLog.length > 10) {
    window.tourErrorLog = window.tourErrorLog.slice(0, 10);
  }
});

// Create and initialize help logger
window.tourHelpLogger = new TourHelpLogger();
document.addEventListener('DOMContentLoaded', function() {
  window.tourHelpLogger.init();
});
