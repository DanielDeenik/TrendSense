// Trendsense UI Module
class TrendsenseUI {
    // Configuration
    static config = {
        statusCheckInterval: 30000, // 30 seconds
        maxRetries: 3,
        retryDelay: 1000, // 1 second
        endpoints: {
            status: '/api/trendsense/status',
            analyze: '/api/trendsense/analyze',
            upload: '/api/trendsense/upload'
        },
        confidenceClasses: {
            high: 'bg-success',
            medium: 'bg-warning',
            low: 'bg-danger'
        }
    };

    // State
    static state = {
        connected: false,
        processing: false,
        currentAnalysis: null,
    };

    // Initialize the module
    static init() {
        this.bindEvents();
        this.checkStatus();
        this.startPeriodicStatusCheck();
    }

    // Bind event listeners
    static bindEvents() {
        const elements = {
            depthSelect: document.getElementById('trendsense-depth'),
            uploadForm: document.querySelector('form[data-trendsense-upload]'),
            triggers: document.querySelectorAll('.trendsense-trigger')
        };

        elements.depthSelect?.addEventListener('change', ({ target }) => {
            this.handleDepthChange(target.value);
        });

        elements.triggers.forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                this.triggerAnalysis(e.target.dataset);
            });
        });

        elements.uploadForm?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleDocumentUpload(e.target);
        });
    }

    // Check Trendsense connection status
    static async checkStatus() {
        try {
            const { connected } = await this.fetchData(this.config.endpoints.status);
            this.state.connected = connected;
            this.updateStatusIndicator(connected);
            connected && this.hideStatusSpinner();
        } catch (error) {
            console.error('Error checking Trendsense status:', error);
            this.state.connected = false;
            this.updateStatusIndicator(false);
        }
    }

    // Start periodic status check
    static startPeriodicStatusCheck() {
        setInterval(() => this.checkStatus(), this.config.statusCheckInterval);
    }

    // Update status indicator in UI
    static updateStatusIndicator(isConnected) {
        const elements = {
            connectedBadge: document.getElementById('trendsense-connected'),
            disconnectedBadge: document.getElementById('trendsense-disconnected'),
            spinner: document.getElementById('trendsense-status-spinner')
        };

        const { connectedBadge, disconnectedBadge, spinner } = elements;

        if (connectedBadge && disconnectedBadge) {
            connectedBadge.style.display = isConnected ? 'inline-block' : 'none';
            disconnectedBadge.style.display = isConnected ? 'none' : 'inline-block';
        }

        spinner && (spinner.style.display = 'none');
    }

    // Show status spinner
    static showStatusSpinner() {
        const spinner = document.getElementById('trendsense-status-spinner');
        spinner && (spinner.style.display = 'inline-block');
    }

    // Hide status spinner
    static hideStatusSpinner() {
        const spinner = document.getElementById('trendsense-status-spinner');
        spinner && (spinner.style.display = 'none');
    }

    // Handle analysis depth change
    static handleDepthChange(depth) {
        this.state.currentAnalysis && this.triggerAnalysis({ depth });
    }

    // Trigger Trendsense analysis
    static async triggerAnalysis(params = {}) {
        if (!this.validateOperation()) return;

        try {
            this.setProcessingState(true);
            const { success, analysis, insights, error } = await this.fetchData(
                this.config.endpoints.analyze,
                { method: 'POST', body: JSON.stringify(params) }
            );
            
            if (success) {
                this.state.currentAnalysis = analysis;
                this.renderInsights(insights);
                this.showToast('success', 'Analysis completed successfully.');
            } else {
                throw new Error(error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Error triggering analysis:', error);
            this.showToast('error', error.message || 'Failed to complete analysis');
        } finally {
            this.setProcessingState(false);
        }
    }

    // Handle document upload
    static async handleDocumentUpload(form) {
        if (!this.validateOperation()) return;

        try {
            this.setProcessingState(true);
            const formData = new FormData(form);
            const { success, results, error } = await this.fetchData(
                this.config.endpoints.upload,
                { method: 'POST', body: formData }
            );
            
            if (success) {
                this.renderUploadResults(results);
                this.showToast('success', 'Document processed successfully.');
            } else {
                throw new Error(error || 'Upload failed');
            }
        } catch (error) {
            console.error('Error uploading document:', error);
            this.showToast('error', error.message || 'Failed to process document');
        } finally {
            this.setProcessingState(false);
        }
    }

    // Show processing status
    static showProcessingStatus() {
        const status = document.querySelector('.trendsense-processing-status');
        status && (status.style.display = 'block');
    }

    // Hide processing status
    static hideProcessingStatus() {
        const status = document.querySelector('.trendsense-processing-status');
        status && (status.style.display = 'none');
    }

    // Render insights
    static renderInsights(insights) {
        const container = document.getElementById('trendsense-insights-container');
        if (!container) return;

        container.innerHTML = insights.map(insight => `
            <div class="trendsense-insight mb-3">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">${insight.title}</h6>
                        <span class="badge ${this.config.confidenceClasses[insight.confidence] || 'bg-secondary'}">
                            ${insight.confidence} Confidence
                        </span>
                    </div>
                    <div class="card-body">
                        <p class="mb-3">${insight.content}</p>
                        ${insight.recommendations ? `
                            <div class="trendsense-recommendations">
                                <h6 class="mb-2">Recommendations:</h6>
                                <ul class="mb-0">
                                    ${insight.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Show toast notification
    static showToast(type, message) {
        const toast = document.createElement('div');
        Object.assign(toast, {
            className: `toast align-items-center text-white bg-${type} border-0`,
            role: 'alert',
            'aria-live': 'assertive',
            'aria-atomic': 'true',
            innerHTML: `
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `
        });
        
        const container = document.getElementById('toast-container') || (() => {
            const div = document.createElement('div');
            Object.assign(div, {
                id: 'toast-container',
                className: 'toast-container position-fixed bottom-0 end-0 p-3'
            });
            document.body.appendChild(div);
            return div;
        })();
        
        container.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }

    static setProcessingState(isProcessing) {
        this.state.processing = isProcessing;
        const status = document.querySelector('.trendsense-processing-status');
        status && (status.style.display = isProcessing ? 'block' : 'none');
    }

    static validateOperation() {
        if (!this.state.connected) {
            this.showToast('error', 'Trendsense is not connected. Please try again later.');
            return false;
        }

        if (this.state.processing) {
            this.showToast('warning', 'Operation is already in progress.');
            return false;
        }

        return true;
    }

    static async fetchData(endpoint, options = {}) {
        const defaultOptions = {
            headers: { 'Content-Type': 'application/json' }
        };

        const response = await fetch(endpoint, { ...defaultOptions, ...options });
        return response.json();
    }
}

// Initialize the module when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => TrendsenseUI.init()); 