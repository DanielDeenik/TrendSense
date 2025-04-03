const http = require('http');
const fs = require('fs');
const path = require('path');

// Create an HTTP server
const server = http.createServer((req, res) => {
  console.log(`Request received: ${req.url}`);

  // Serve the overview page for root URL
  if (req.url === '/' || req.url === '/index.html') {
    fs.readFile('trendsense_overview.html', (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading overview page');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
    return;
  }

  // Handle other requests
  res.writeHead(404);
  res.end('Not found');
});

// Set the port (use environment variable or default to 3000)
const PORT = process.env.PORT || 3000;

// Start the server
server.listen(PORT, () => {
  console.log(`TrendSense overview server running at http://localhost:${PORT}/`);
});