const http = require('http');
const fs = require('fs');
const path = require('path');

// Port should be 3000 for Replit
const PORT = process.env.PORT || 3000;
console.log(`Starting server on port ${PORT}`);

// Dashboard data (static for demo)
const dashboardData = {
  carbon_intensity: { value: 12.4, change: -15.3 },
  esg_score: { value: 73.8, change: 2.5 },
  renewable_energy: { value: 38, change: 8 },
  water_intensity: { value: 2.3, change: -12.2 }
};

// Insights data (static for demo)
const insightsData = {
  emissions_trend: {
    title: "Emissions Trend Analysis",
    content: "Your emissions reduction is outpacing industry benchmarks by 6.2%. Key contributors: Renewable energy adoption and facility upgrades."
  },
  regulatory_readiness: {
    title: "Regulatory Readiness",
    content: "CSRD preparation is at 75% completion, with data collection systems fully implemented. Focus areas: scope 3 emissions and biodiversity impacts."
  },
  water_risk: {
    title: "Water Risk Alert",
    content: "Three manufacturing facilities are in high water stress regions. Consider implementing advanced water recycling technologies."
  }
};

// Create a simple HTTP server
const server = http.createServer((req, res) => {
  console.log(`${req.method} ${req.url}`);
  
  // Parse the URL
  const url = req.url;
  
  // API endpoints
  if (url === '/api/dashboard-data') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(dashboardData));
  } 
  else if (url === '/api/insights') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(insightsData));
  }
  else if (url === '/api/health' || url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', version: '1.0.0' }));
  }
  // Main route - serve the dashboard
  else if (url === '/' || url === '/dashboard') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SustainaTrend™ Dashboard</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { background-color: #1a202c; color: white; }
            .metric-card { background-color: #2d3748; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; }
            .metric-value { font-size: 1.875rem; font-weight: 700; }
            .trend-positive { color: #48bb78; }
            .trend-negative { color: #f56565; }
            .sidebar { background-color: #2d3748; width: 250px; height: 100vh; position: fixed; }
            .main-content { margin-left: 250px; padding: 2rem; }
            .nav-item { padding: 0.75rem 1rem; display: flex; align-items: center; }
            .nav-item:hover { background-color: #4a5568; }
            .nav-item.active { background-color: #4a5568; color: white; }
            .nav-item svg { margin-right: 0.75rem; }
        </style>
    </head>
    <body>
        <div class="flex">
            <!-- Sidebar -->
            <div class="sidebar">
                <div class="p-4 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-2 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4 2a2 2 0 00-2 2v11a3 3 0 106 0V4a2 2 0 00-2-2H4zm1 14a1 1 0 100-2 1 1 0 000 2zm5-14a2 2 0 00-2 2v5a2 2 0 104 0V4a2 2 0 00-2-2h-1zm1 7a1 1 0 10-2 0 1 1 0 002 0zm3-7a2 2 0 00-2 2v8a2 2 0 104 0V4a2 2 0 00-2-2h-1zm1 10a1 1 0 10-2 0 1 1 0 002 0z" clip-rule="evenodd" />
                    </svg>
                    <h1 class="text-xl font-bold">SustainaTrend™</h1>
                </div>
                
                <div class="px-4 py-2 text-sm font-semibold text-gray-400">PLATFORM</div>
                <a href="/" class="nav-item active">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                        <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                    </svg>
                    Dashboard
                </a>
                <a href="#" class="nav-item text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    Performance
                </a>
                
                <div class="px-4 py-2 text-sm font-semibold text-gray-400 mt-4">INTELLIGENCE</div>
                <a href="#" class="nav-item text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7z" clip-rule="evenodd" />
                    </svg>
                    Trend Analysis
                </a>
                <a href="#" class="nav-item text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
                    </svg>
                    Strategy Hub
                </a>
            </div>

            <!-- Main Content -->
            <div class="main-content">
                <h1 class="text-2xl font-bold mb-6">Sustainability Dashboard</h1>

                <!-- Metrics Row -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <!-- Carbon Intensity -->
                    <div class="metric-card">
                        <h3 class="text-gray-400 mb-2">Carbon Intensity</h3>
                        <div class="metric-value" id="carbon-intensity-value">12.4</div>
                        <div class="flex items-center mt-2">
                            <span class="trend-negative" id="carbon-intensity-trend">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                                </svg>
                                <span id="carbon-intensity-change">-15.3%</span>
                            </span>
                        </div>
                    </div>
                    
                    <!-- ESG Score -->
                    <div class="metric-card">
                        <h3 class="text-gray-400 mb-2">ESG Score</h3>
                        <div class="metric-value" id="esg-score-value">73.8</div>
                        <div class="flex items-center mt-2">
                            <span class="trend-positive" id="esg-score-trend">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                                <span id="esg-score-change">+2.5%</span>
                            </span>
                        </div>
                    </div>
                    
                    <!-- Renewable Energy -->
                    <div class="metric-card">
                        <h3 class="text-gray-400 mb-2">Renewable Energy</h3>
                        <div class="metric-value" id="renewable-energy-value">38%</div>
                        <div class="flex items-center mt-2">
                            <span class="trend-positive" id="renewable-energy-trend">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                                <span id="renewable-energy-change">+8%</span>
                            </span>
                        </div>
                    </div>
                    
                    <!-- Water Intensity -->
                    <div class="metric-card">
                        <h3 class="text-gray-400 mb-2">Water Intensity</h3>
                        <div class="metric-value" id="water-intensity-value">2.3</div>
                        <div class="flex items-center mt-2">
                            <span class="trend-negative" id="water-intensity-trend">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                                </svg>
                                <span id="water-intensity-change">-12.2%</span>
                            </span>
                        </div>
                    </div>
                </div>
                
                <!-- Charts & Insights -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Emissions Chart -->
                    <div class="bg-gray-800 rounded-lg p-4">
                        <h3 class="text-lg font-semibold mb-4">Emissions Trend</h3>
                        <canvas id="emissions-chart" height="200"></canvas>
                    </div>
                    
                    <!-- AI Insights -->
                    <div>
                        <h3 class="text-lg font-semibold mb-4">AI Insights</h3>
                        <div id="insights-container">
                            <!-- Insights will be loaded dynamically -->
                        </div>
                    </div>
                </div>

                <script>
                    // Initialize charts
                    const ctx = document.getElementById('emissions-chart').getContext('2d');
                    const emissionsChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                            datasets: [{
                                label: 'Carbon Emissions (tCO2e)',
                                data: [12, 19, 15, 12, 8, 6],
                                backgroundColor: 'rgba(72, 187, 120, 0.2)',
                                borderColor: 'rgba(72, 187, 120, 1)',
                                tension: 0.4
                            }]
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.1)'
                                    },
                                    ticks: {
                                        color: 'rgba(255, 255, 255, 0.7)'
                                    }
                                },
                                x: {
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.1)'
                                    },
                                    ticks: {
                                        color: 'rgba(255, 255, 255, 0.7)'
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: {
                                        color: 'rgba(255, 255, 255, 0.7)'
                                    }
                                }
                            }
                        }
                    });

                    // Load dashboard data with fetch
                    fetch('/api/dashboard-data')
                        .then(response => response.json())
                        .then(data => {
                            // Update metric values and changes
                            document.getElementById('carbon-intensity-value').textContent = data.carbon_intensity.value;
                            document.getElementById('carbon-intensity-change').textContent = data.carbon_intensity.change + '%';
                            
                            document.getElementById('esg-score-value').textContent = data.esg_score.value;
                            document.getElementById('esg-score-change').textContent = data.esg_score.change + '%';
                            
                            document.getElementById('renewable-energy-value').textContent = data.renewable_energy.value + '%';
                            document.getElementById('renewable-energy-change').textContent = data.renewable_energy.change + '%';
                            
                            document.getElementById('water-intensity-value').textContent = data.water_intensity.value;
                            document.getElementById('water-intensity-change').textContent = data.water_intensity.change + '%';
                        })
                        .catch(error => console.error('Error loading dashboard data:', error));

                    // Load insights with fetch
                    fetch('/api/insights')
                        .then(response => response.json())
                        .then(data => {
                            // Update insights
                            const insightsContainer = document.getElementById('insights-container');
                            
                            for (const key in data) {
                                const insight = data[key];
                                const insightElement = document.createElement('div');
                                insightElement.className = 'bg-gray-800 rounded-lg p-4 mb-4';
                                insightElement.innerHTML = \`
                                    <h3 class="text-lg font-semibold mb-2">\${insight.title}</h3>
                                    <p class="text-gray-300">\${insight.content}</p>
                                \`;
                                insightsContainer.appendChild(insightElement);
                            }
                        })
                        .catch(error => console.error('Error loading insights:', error));
                </script>
            </div>
        </div>
    </body>
    </html>
    `);
  } 
  // 404 for all other routes
  else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>404 Not Found</h1><p>The page you requested was not found.</p>');
  }
});

// Start the server
server.listen(PORT, () => {
  console.log(`Server running at http://0.0.0.0:${PORT}/`);
});