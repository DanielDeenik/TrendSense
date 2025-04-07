// Chart configuration and helper functions
const Charts = {
    // Default chart options
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    },

    // Create a line chart
    createLineChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });
    },

    // Create a bar chart
    createBarChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });
    },

    // Create a pie chart
    createPieChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options
            }
        });
    },

    // Create a doughnut chart
    createDoughnutChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options
            }
        });
    },

    // Create a radar chart
    createRadarChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'radar',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                scales: {
                    r: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });
    },

    // Update chart data
    updateChart(chart, newData) {
        chart.data = newData;
        chart.update();
    },

    // Destroy chart
    destroyChart(chart) {
        chart.destroy();
    }
};

// Export the Charts module
export default Charts; 