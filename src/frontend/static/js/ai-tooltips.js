/**
 * AI Tooltips and Popups
 * 
 * This utility provides generative AI-powered tooltips and popups
 * to help users understand complex features and concepts.
 */

class AITooltips {
    constructor() {
        this.tooltipContainer = null;
        this.popupContainer = null;
        this.activePopup = null;
        this.tooltipDelay = 300;
        this.tooltipTimer = null;
        this.initialized = false;
    }

    /**
     * Initialize the AI tooltips system
     */
    init() {
        if (this.initialized) return;

        // Create tooltip container
        this.tooltipContainer = document.createElement('div');
        this.tooltipContainer.className = 'ai-tooltip-container';
        this.tooltipContainer.style.position = 'absolute';
        this.tooltipContainer.style.zIndex = '1000';
        this.tooltipContainer.style.display = 'none';
        document.body.appendChild(this.tooltipContainer);

        // Create popup container
        this.popupContainer = document.createElement('div');
        this.popupContainer.className = 'ai-popup-container';
        this.popupContainer.style.position = 'fixed';
        this.popupContainer.style.zIndex = '1001';
        this.popupContainer.style.display = 'none';
        this.popupContainer.style.top = '0';
        this.popupContainer.style.left = '0';
        this.popupContainer.style.width = '100%';
        this.popupContainer.style.height = '100%';
        this.popupContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        this.popupContainer.style.justifyContent = 'center';
        this.popupContainer.style.alignItems = 'center';
        document.body.appendChild(this.popupContainer);

        // Add click event to close popup when clicking outside
        this.popupContainer.addEventListener('click', (e) => {
            if (e.target === this.popupContainer) {
                this.hidePopup();
            }
        });

        // Initialize tooltips
        this.initTooltips();

        // Initialize popups
        this.initPopups();

        this.initialized = true;
    }

    /**
     * Initialize tooltips on elements with data-ai-tooltip attribute
     */
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-ai-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                clearTimeout(this.tooltipTimer);
                this.tooltipTimer = setTimeout(() => {
                    this.showTooltip(element, element.getAttribute('data-ai-tooltip'));
                }, this.tooltipDelay);
            });
            
            element.addEventListener('mouseleave', () => {
                clearTimeout(this.tooltipTimer);
                this.hideTooltip();
            });
        });
    }

    /**
     * Initialize popups on elements with data-ai-popup attribute
     */
    initPopups() {
        const popupElements = document.querySelectorAll('[data-ai-popup]');
        
        popupElements.forEach(element => {
            element.addEventListener('click', () => {
                const popupId = element.getAttribute('data-ai-popup');
                const popupTitle = element.getAttribute('data-ai-popup-title') || 'AI Insight';
                const popupContent = element.getAttribute('data-ai-popup-content') || '';
                
                this.showPopup(popupId, popupTitle, popupContent);
            });
        });
    }

    /**
     * Show a tooltip at the specified element
     */
    showTooltip(element, content) {
        const rect = element.getBoundingClientRect();
        
        this.tooltipContainer.innerHTML = `
            <div class="ai-tooltip bg-gray-800 text-white p-2 rounded shadow-lg border border-gray-700 max-w-xs">
                <div class="flex items-center mb-1">
                    <i class="fas fa-robot text-blue-400 mr-1"></i>
                    <span class="text-xs font-semibold text-blue-400">AI Tip</span>
                </div>
                <div class="text-sm">${content}</div>
            </div>
        `;
        
        this.tooltipContainer.style.display = 'block';
        
        // Position the tooltip
        const tooltipRect = this.tooltipContainer.getBoundingClientRect();
        let top = rect.bottom + window.scrollY + 5;
        let left = rect.left + window.scrollX + (rect.width / 2) - (tooltipRect.width / 2);
        
        // Ensure tooltip stays within viewport
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        
        this.tooltipContainer.style.top = `${top}px`;
        this.tooltipContainer.style.left = `${left}px`;
    }

    /**
     * Hide the current tooltip
     */
    hideTooltip() {
        this.tooltipContainer.style.display = 'none';
    }

    /**
     * Show a popup with the specified content
     */
    showPopup(id, title, content) {
        // Create popup content
        const popupContent = `
            <div class="ai-popup bg-gray-900 rounded-lg shadow-xl border border-gray-700 max-w-2xl w-full mx-4">
                <div class="flex items-center justify-between border-b border-gray-700 p-4">
                    <div class="flex items-center">
                        <i class="fas fa-robot text-blue-500 mr-2 text-xl"></i>
                        <h3 class="text-lg font-semibold text-white">${title}</h3>
                    </div>
                    <button class="ai-popup-close text-gray-400 hover:text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="p-4 text-gray-300">
                    ${content}
                </div>
                <div class="border-t border-gray-700 p-4 flex justify-end">
                    <button class="ai-popup-close bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                        Got it
                    </button>
                </div>
            </div>
        `;
        
        this.popupContainer.innerHTML = popupContent;
        this.popupContainer.style.display = 'flex';
        this.activePopup = id;
        
        // Add event listeners to close buttons
        const closeButtons = this.popupContainer.querySelectorAll('.ai-popup-close');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.hidePopup();
            });
        });
        
        // Prevent scrolling on body
        document.body.style.overflow = 'hidden';
    }

    /**
     * Hide the current popup
     */
    hidePopup() {
        this.popupContainer.style.display = 'none';
        this.activePopup = null;
        
        // Restore scrolling on body
        document.body.style.overflow = '';
    }
}

// Create global instance
const aiTooltips = new AITooltips();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    aiTooltips.init();
});
