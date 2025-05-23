/**
 * Trend Radar Visualization Component
 * 
 * This component creates visualizations for the Trend Radar:
 * - Polar Area Chart: Trends by category and stage
 * - Trend List: Filterable list of trends
 */

// Initialize the Trend Radar
function initTrendRadar() {
    // Fetch data from API
    fetch('/api/trend-radar/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Initialize radar chart with data from API
            renderTrendRadarChart(data.trends, data.categories, data.stages);
            
            // Initialize trend list with data from API
            populateTrendList(data.trends);
            
            // Initialize filters
            initFilters(data.categories, data.stages);
        })
        .catch(error => {
            console.error('Error fetching Trend Radar data:', error);
            // Fall back to empty data
            renderTrendRadarChart([], [], []);
            populateTrendList([]);
            initFilters([], []);
        });
}

// Render the Trend Radar Chart
function renderTrendRadarChart(trends, categories, stages) {
    const ctx = document.getElementById('trendRadarChart');
    if (!ctx) return;
    
    // Process data for radar chart
    const radarData = processDataForRadarChart(trends, categories, stages);
    
    // Create radar chart
    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: categories,
            datasets: [
                {
                    label: 'Watch',
                    data: radarData.watch,
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1
                },
                {
                    label: 'Prepare',
                    data: radarData.prepare,
                    backgroundColor: 'rgba(245, 158, 11, 0.5)',
                    borderColor: 'rgb(245, 158, 11)',
                    borderWidth: 1
                },
                {
                    label: 'Act',
                    data: radarData.act,
                    backgroundColor: 'rgba(16, 185, 129, 0.5)',
                    borderColor: 'rgb(16, 185, 129)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#e5e7eb',
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Trends by Category and Stage',
                    color: '#ffffff',
                    font: {
                        family: 'Inter, sans-serif',
                        size: 16
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#e5e7eb',
                    borderColor: 'rgba(75, 85, 99, 0.5)',
                    borderWidth: 1,
                    padding: 10,
                    bodyFont: {
                        family: 'Inter, sans-serif'
                    },
                    titleFont: {
                        family: 'Inter, sans-serif',
                        weight: 'bold'
                    }
                }
            },
            scales: {
                r: {
                    grid: {
                        color: 'rgba(75, 85, 99, 0.2)'
                    },
                    ticks: {
                        color: '#9ca3af',
                        backdropColor: 'transparent',
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    pointLabels: {
                        color: '#e5e7eb',
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    }
                }
            }
        }
    });
}

// Process data for radar chart
function processDataForRadarChart(trends, categories, stages) {
    const result = {
        watch: Array(categories.length).fill(0),
        prepare: Array(categories.length).fill(0),
        act: Array(categories.length).fill(0)
    };
    
    trends.forEach(trend => {
        const categoryIndex = categories.indexOf(trend.category);
        if (categoryIndex !== -1) {
            if (trend.stage === 'Watch' || trend.stage === 'Emerging') {
                result.watch[categoryIndex]++;
            } else if (trend.stage === 'Prepare' || trend.stage === 'Growing') {
                result.prepare[categoryIndex]++;
            } else if (trend.stage === 'Act' || trend.stage === 'Mature') {
                result.act[categoryIndex]++;
            }
        }
    });
    
    return result;
}

// Populate the trend list
function populateTrendList(trends) {
    const container = document.getElementById('trendList');
    if (!container) return;
    
    // Clear the container
    container.innerHTML = '';
    
    if (trends.length === 0) {
        container.innerHTML = '<div class="p-4 text-gray-400">No trends available</div>';
        return;
    }
    
    // Create a card for each trend
    trends.forEach(trend => {
        const card = document.createElement('div');
        card.className = 'trend-item bg-gray-800 border border-gray-700 rounded-lg p-4 mb-4';
        card.dataset.category = trend.category || '';
        card.dataset.stage = trend.stage || '';
        
        // Determine badge color based on stage
        let badgeColor = 'bg-blue-500';
        if (trend.stage === 'Prepare' || trend.stage === 'Growing') {
            badgeColor = 'bg-yellow-500';
        } else if (trend.stage === 'Act' || trend.stage === 'Mature') {
            badgeColor = 'bg-green-500';
        }
        
        // Create card content
        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-medium text-white">${trend.name}</h3>
                <span class="text-xs font-medium ${badgeColor} text-white px-2 py-1 rounded">${trend.stage}</span>
            </div>
            <div class="text-sm text-gray-400 mb-3">${trend.category}</div>
            <p class="text-gray-300 mb-3">${trend.description || 'No description available'}</p>
            <div class="flex justify-between items-center">
                <div class="flex items-center">
                    <span class="text-sm font-medium text-white mr-1">Score:</span>
                    <span class="text-sm text-gray-300">${trend.score || 'N/A'}</span>
                </div>
                <div class="flex items-center">
                    <span class="text-sm font-medium text-white mr-1">Momentum:</span>
                    <span class="text-sm ${trend.momentum > 0 ? 'text-green-400' : 'text-red-400'}">
                        ${trend.momentum > 0 ? '+' : ''}${trend.momentum || '0'}
                    </span>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Initialize filters
function initFilters(categories, stages) {
    const categoryFilter = document.getElementById('categoryFilter');
    const stageFilter = document.getElementById('stageFilter');
    const searchInput = document.getElementById('searchInput');
    
    if (!categoryFilter || !stageFilter || !searchInput) return;
    
    // Clear existing options
    categoryFilter.innerHTML = '<option value="">All Categories</option>';
    stageFilter.innerHTML = '<option value="">All Stages</option>';
    
    // Add category options
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });
    
    // Add stage options
    stages.forEach(stage => {
        const option = document.createElement('option');
        option.value = stage;
        option.textContent = stage;
        stageFilter.appendChild(option);
    });
    
    // Add event listeners
    categoryFilter.addEventListener('change', applyFilters);
    stageFilter.addEventListener('change', applyFilters);
    searchInput.addEventListener('input', applyFilters);
    
    // Initial filter application
    applyFilters();
}

// Apply filters to trend list
function applyFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const stageFilter = document.getElementById('stageFilter');
    const searchInput = document.getElementById('searchInput');
    const trendItems = document.querySelectorAll('.trend-item');
    
    if (!categoryFilter || !stageFilter || !searchInput || !trendItems.length) return;
    
    const categoryValue = categoryFilter.value;
    const stageValue = stageFilter.value;
    const searchValue = searchInput.value.toLowerCase();
    
    trendItems.forEach(item => {
        const category = item.dataset.category;
        const stage = item.dataset.stage;
        const text = item.textContent.toLowerCase();
        
        const matchesCategory = !categoryValue || category === categoryValue;
        const matchesStage = !stageValue || stage === stageValue;
        const matchesSearch = !searchValue || text.includes(searchValue);
        
        if (matchesCategory && matchesStage && matchesSearch) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
}

// Initialize when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        // Load Chart.js dynamically
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = initTrendRadar;
        document.head.appendChild(script);
    } else {
        initTrendRadar();
    }
});
