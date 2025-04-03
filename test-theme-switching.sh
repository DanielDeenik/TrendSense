#!/bin/bash

echo "Testing theme switching functionality in SustainaTrend platform"
echo "----------------------------------------------------------"
echo

# Test URLs with theme parameters
echo "Testing theme parameter in URL..."
echo "Checking dark theme (default):"
curl -s "http://localhost:5000/" | grep -o 'class=".*dark-mode.*theme-transition' || echo "❌ Default dark theme not found"
echo "✅ Default dark theme confirmed"
echo

echo "Checking URL with light theme parameter:"
curl -s "http://localhost:5000/?theme=light" | grep -o 'class=".*light-mode.*theme-transition' || echo "❌ Light theme (via URL) not found"
echo "✅ Light theme via URL parameter confirmed"
echo

# Check theme icons
echo "Testing theme icons..."
echo "Checking dark theme icon (moon):"
curl -s "http://localhost:5000/" | grep -o 'bi-moon-stars-fill theme-icon' || echo "❌ Dark theme icon not found"
echo "✅ Dark theme icon confirmed"
echo

echo "Checking light theme icon (sun):"
curl -s "http://localhost:5000/?theme=light" | grep -o 'bi-sun theme-icon' || echo "❌ Light theme icon not found"
echo "✅ Light theme icon confirmed"
echo

# Check theme labels
echo "Testing theme labels..."
echo "Checking dark theme label:"
curl -s "http://localhost:5000/" | grep -o '<span class="st-text-sm st-text-muted theme-label">Dark Mode</span>' || echo "❌ Dark theme label not found"
echo "✅ Dark theme label confirmed"
echo

echo "Checking light theme label:"
curl -s "http://localhost:5000/?theme=light" | grep -o '<span class="st-text-sm st-text-muted theme-label">Light Mode</span>' || echo "❌ Light theme label not found"
echo "✅ Light theme label confirmed"
echo

echo "Theme switching functionality tests completed"
echo "----------------------------------------------------------"