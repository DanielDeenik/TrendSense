#!/bin/bash

echo "Testing Benchmarking Engine Route Structure..."

# Test main benchmarking route and redirect
echo -e "\nTesting /benchmarking route (should redirect to benchmarking.index):"
curl -s -I http://localhost:5000/benchmarking | grep "Location\|HTTP"

# Test framework selector route
echo -e "\nTesting /benchmarking/framework-selector route:"
curl -s -I http://localhost:5000/benchmarking/framework-selector | grep HTTP

# Test peer comparison route
echo -e "\nTesting /benchmarking/peer-comparison route:"
curl -s -I http://localhost:5000/benchmarking/peer-comparison | grep HTTP

# Test data needs route
echo -e "\nTesting /benchmarking/data-needs route:"
curl -s -I http://localhost:5000/benchmarking/data-needs | grep HTTP

# Test document upload route
echo -e "\nTesting /benchmarking/document-upload route:"
curl -s -I http://localhost:5000/benchmarking/document-upload | grep HTTP

# Test extract data route
echo -e "\nTesting /benchmarking/extract-data route:"
curl -s -I http://localhost:5000/benchmarking/extract-data | grep HTTP

# Test legacy routes
echo -e "\nTesting legacy /benchmark-analysis route (should redirect):"
curl -s -I http://localhost:5000/benchmark-analysis | grep "Location\|HTTP"

# Test API endpoints
echo -e "\nTesting /benchmarking/api/suggest-framework endpoint:"
curl -s -I -X POST http://localhost:5000/benchmarking/api/suggest-framework -H "Content-Type: application/json" | grep HTTP

echo -e "\nTesting /benchmarking/api/peer-companies endpoint:"
curl -s -I -X POST http://localhost:5000/benchmarking/api/peer-companies -H "Content-Type: application/json" | grep HTTP

echo -e "\nTesting /benchmarking/api/benchmark-data endpoint:"
curl -s -I -X POST http://localhost:5000/benchmarking/api/benchmark-data -H "Content-Type: application/json" | grep HTTP

echo -e "\nTesting /benchmarking/api/framework-data-needs endpoint:"
curl -s -I http://localhost:5000/benchmarking/api/framework-data-needs | grep HTTP

echo -e "\nTesting /benchmarking/api/vc-benchmark-match endpoint:"
curl -s -I -X POST http://localhost:5000/benchmarking/api/vc-benchmark-match -H "Content-Type: application/json" | grep HTTP

echo -e "\nAll tests completed."