// API request handler
const API = {
    // Base URL for API requests
    baseUrl: '/api',

    // Default headers for API requests
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },

    // Helper function to handle API responses
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'An error occurred');
        }
        return response.json();
    },

    // GET request
    async get(endpoint, params = {}) {
        const url = new URL(this.baseUrl + endpoint, window.location.origin);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        
        const response = await fetch(url, {
            method: 'GET',
            headers: this.headers
        });
        
        return this.handleResponse(response);
    },

    // POST request
    async post(endpoint, data = {}) {
        const response = await fetch(this.baseUrl + endpoint, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    },

    // PUT request
    async put(endpoint, data = {}) {
        const response = await fetch(this.baseUrl + endpoint, {
            method: 'PUT',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    },

    // DELETE request
    async delete(endpoint) {
        const response = await fetch(this.baseUrl + endpoint, {
            method: 'DELETE',
            headers: this.headers
        });
        
        return this.handleResponse(response);
    },

    // Upload file
    async uploadFile(endpoint, file, onProgress = null) {
        const formData = new FormData();
        formData.append('file', file);

        const xhr = new XMLHttpRequest();
        
        if (onProgress) {
            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    onProgress(percentComplete);
                }
            });
        }

        return new Promise((resolve, reject) => {
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(JSON.parse(xhr.response));
                } else {
                    reject(new Error(xhr.response));
                }
            };
            
            xhr.onerror = () => {
                reject(new Error('Network error'));
            };
            
            xhr.open('POST', this.baseUrl + endpoint);
            xhr.send(formData);
        });
    }
};

// Export the API module
export default API; 