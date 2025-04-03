#!/usr/bin/env node
/**
 * Simple Node.js Server for SustainaTrend Dashboard
 * Using only built-in modules, no dependencies
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// Configuration
const PORT = process.env.PORT || 8080;
const HOST = '0.0.0.0';

// Mime types for serving static files
const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

// Sample data for our dashboard
function generateMetricsData() {
  return {
    carbon_intensity: {
      value: Math.round((Math.random() * 5 + 10) * 10) / 10,
      change: Math.round((Math.random() * 10 - 20) * 10) / 10,
      trend: 'negative'  // Lower is better for carbon intensity
    },
    esg_score: {
      value: Math.round((Math.random() * 10 + 70) * 10) / 10,
      change: Math.round((Math.random() * 4 + 1) * 10) / 10,
      trend: 'positive'
    },
    renewable_energy: {
      value: Math.round(Math.random() * 15 + 30),
      change: Math.round(Math.random() * 5 + 5),
      trend: 'positive'
    },
    water_intensity: {
      value: Math.round((Math.random() * 1 + 2) * 10) / 10,
      change: Math.round((Math.random() * 7 - 15) * 10) / 10,
      trend: 'negative'  // Lower is better for water intensity
    }
  };
}

function generateEmissionsData() {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  
  // Generate a decreasing trend for carbon emissions
  const values = [];
  let startValue = Math.random() * 5 + 15;
  for (let i = 0; i < 6; i++) {
    const value = Math.max(startValue - (Math.random() * 2 + 1) * i, 5);
    values.push(Math.round(value * 10) / 10);
  }
  
  return {
    labels: months,
    data: values
  };
}

function generateInsights() {
  return [
    {
      title: 'Emissions Trend Analysis',
      content: 'Your emissions reduction is outpacing industry benchmarks by 6.2%. Key contributors: Renewable energy adoption and facility upgrades.'
    },
    {
      title: 'Regulatory Readiness',
      content: 'CSRD preparation is at 75% completion, with data collection systems fully implemented. Focus areas: scope 3 emissions and biodiversity impacts.'
    },
    {
      title: 'Water Risk Alert',
      content: 'Three manufacturing facilities are in high water stress regions. Consider implementing advanced water recycling technologies.'
    }
  ];
}

// Create the server
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  
  // API endpoints
  if (pathname === '/api/metrics') {
    sendJsonResponse(res, generateMetricsData());
    return;
  }
  
  if (pathname === '/api/emissions') {
    sendJsonResponse(res, generateEmissionsData());
    return;
  }
  
  if (pathname === '/api/insights') {
    sendJsonResponse(res, generateInsights());
    return;
  }
  
  if (pathname === '/health') {
    sendJsonResponse(res, { status: 'ok', time: new Date().toISOString() });
    return;
  }
  
  // Serve dashboard for root or dashboard path
  if (pathname === '/' || pathname === '/dashboard') {
    try {
      const content = fs.readFileSync('frontend/templates/dashboard.html');
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(content);
    } catch (err) {
      // Fallback to the simple dashboard if template is not available
      try {
        const content = fs.readFileSync('fallback.html');
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(content);
      } catch (fallbackErr) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error: Could not load dashboard template');
      }
    }
    return;
  }
  
  // Attempt to serve static files
  let filePath = pathname;
  if (filePath.startsWith('/')) {
    filePath = filePath.slice(1);
  }
  
  // Check if file exists
  try {
    const stat = fs.statSync(filePath);
    if (stat.isFile()) {
      const ext = path.extname(filePath);
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';
      
      const content = fs.readFileSync(filePath);
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
      return;
    }
  } catch (err) {
    // File not found or other error
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
    return;
  }
  
  // Default response for unhandled paths
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('404 Not Found');
});

// Helper function to send JSON responses
function sendJsonResponse(res, data) {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

// Start the server
server.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}/`);
});