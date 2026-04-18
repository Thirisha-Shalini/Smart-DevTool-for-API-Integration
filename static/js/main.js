document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('api-form');
    const resultsSection = document.getElementById('results');
    const endpointsField = document.getElementById('endpoints');
    const authMethodsField = document.getElementById('auth-methods');
    const sdksField = document.getElementById('sdks');
    const codeOutput = document.getElementById('generated-code');
    const downloadButton = document.getElementById('download-btn');
    const copyButton = document.getElementById('copy-btn');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const url = document.getElementById('api-url').value.trim();
        const usecase = document.getElementById('usecase').value.trim();
        const lang = document.getElementById('lang').value;

        console.log('Form submitted:', { url, usecase, lang });

        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, usecase, lang })
        });

        console.log('Response status:', response.status);

        const contentType = response.headers.get('Content-Type') || '';
        let data;
        if (contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.error('Unexpected response:', text);
            showError('Unexpected server response. Please try again.');
            return;
        }

        if (!response.ok) {
            console.error('Error response:', data);
            showError(data.error || 'Unable to generate code. Please verify the URL and try again.');
            return;
        }

        console.log('Received data:', data);
        console.log('Received data:', data);
        displayResults(data);
    });

    downloadButton.addEventListener('click', function() {
        const content = codeOutput.textContent;
        const lang = document.getElementById('lang').value;
        const extension = lang === 'python' ? 'py' : 'js';
        downloadFile(content, `api_wrapper.${extension}`);
    });

    copyButton.addEventListener('click', function() {
        navigator.clipboard.writeText(codeOutput.textContent)
            .then(() => alert('Code copied to clipboard.'))
            .catch(() => alert('Copy failed. Try manually selecting the content.'));
    });

    function displayResults(data) {
        clearError();
        console.log('displayResults called with:', data);
        
        // Display endpoints with method badges
        if (data.endpoints.length) {
            endpointsField.innerHTML = '';
            data.endpoints.forEach(endpoint => {
                const match = endpoint.match(/^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(.*)$/);
                if (match) {
                    const method = match[1];
                    const path = match[2];
                    const colors = {
                        'GET': '#3b82f6',
                        'POST': '#10b981',
                        'PUT': '#f59e0b',
                        'DELETE': '#ef4444',
                        'PATCH': '#8b5cf6',
                        'HEAD': '#6b7280',
                        'OPTIONS': '#06b6d4'
                    };
                    const color = colors[method] || '#64748b';
                    const item = document.createElement('div');
                    item.className = 'endpoint-item';
                    item.innerHTML = `<span class="method-badge" style="background-color: ${color};">${method}</span><span class="endpoint-path">${path}</span>`;
                    endpointsField.appendChild(item);
                } else {
                    const item = document.createElement('div');
                    item.className = 'endpoint-item';
                    item.textContent = endpoint;
                    endpointsField.appendChild(item);
                }
            });
        } else {
            endpointsField.textContent = 'No endpoints found';
        }
        
        authMethodsField.textContent = data.auth_methods.length ? data.auth_methods.join(', ') : 'None detected';
        sdksField.textContent = data.sdks.length ? data.sdks.join(', ') : 'None detected';
        codeOutput.textContent = data.generated_code || '';
        
        // Safely highlight with Prism if available
        if (typeof Prism !== 'undefined' && Prism.highlightElement) {
            console.log('Prism available, highlighting code');
            Prism.highlightElement(codeOutput);
        } else {
            console.log('Prism not available, skipping highlight');
        }
        
        console.log('Removing hidden class from resultsSection');
        resultsSection.classList.remove('hidden');
        console.log('Results section now visible:', resultsSection.classList);
    }

    function showError(message) {
        const errorBanner = document.getElementById('error-banner');
        errorBanner.textContent = message;
        errorBanner.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    }

    function clearError() {
        const errorBanner = document.getElementById('error-banner');
        errorBanner.textContent = '';
        errorBanner.classList.add('hidden');
    }

    function createMethodBadge(method) {
        const colors = {
            'GET': '#3b82f6',
            'POST': '#10b981',
            'PUT': '#f59e0b',
            'DELETE': '#ef4444',
            'PATCH': '#8b5cf6',
            'HEAD': '#6b7280',
            'OPTIONS': '#06b6d4'
        };
        const color = colors[method] || '#64748b';
        const badge = document.createElement('span');
        badge.className = 'method-badge';
        badge.style.backgroundColor = color;
        badge.textContent = method;
        return badge;
    }

    function downloadFile(content, filename) {
        const blob = new Blob([content], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }
});