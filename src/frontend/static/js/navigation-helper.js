/**
 * Navigation Helper Script for TrendSense
 *
 * This script handles all navigation-related functionality:
 * - Highlighting active navigation items
 * - Mobile navigation
 * - Breadcrumb navigation
 * - Workflow navigation
 * - Navigation tooltips
 */

// Initialize navigation when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Navigation Helper: Initializing...');

    try {
        // Initialize navigation components
        initNavigation();
    } catch (error) {
        console.error('Navigation Helper: Error initializing navigation', error);
    }
});

/**
 * Initialize all navigation components
 */
function initNavigation() {
    // Highlight the active navigation item
    highlightActiveNavItem();

    // Initialize mobile navigation
    initMobileNavigation();

    // Add breadcrumb navigation if container exists
    if (document.getElementById('breadcrumb-container')) {
        addBreadcrumbNavigation();
    }

    // Add tooltips to navigation items
    addNavigationTooltips();

    // Initialize workflow navigation if container exists
    if (document.getElementById('workflow-navigation')) {
        initWorkflowNavigation();
    }

    // Log successful initialization
    console.log('Navigation Helper: Navigation initialized successfully');
}

/**
 * Highlights the active navigation item based on the current URL
 */
function highlightActiveNavItem() {
    // Get the current path and normalize it
    const currentPath = window.location.pathname;
    const normalizedPath = currentPath === '/' ? '/' : currentPath.replace(/\/$/, '');

    console.log('Navigation Helper: Current path:', normalizedPath);

    // Get all navigation links (excluding generative UI buttons)
    const navLinks = document.querySelectorAll('#main-navigation a.nav-link');

    // First pass: Look for exact matches
    let exactMatchFound = false;

    navLinks.forEach(link => {
        // Get the link path and normalize it
        const linkPath = link.getAttribute('href');
        const normalizedLinkPath = linkPath === '/' ? '/' : linkPath.replace(/\/$/, '');

        // Check for exact match
        if (normalizedPath === normalizedLinkPath) {
            console.log('Navigation Helper: Exact match found:', normalizedLinkPath);
            markLinkActive(link);
            exactMatchFound = true;
        }
    });

    // Second pass: If no exact match was found, look for parent paths
    if (!exactMatchFound) {
        navLinks.forEach(link => {
            // Get the link path and normalize it
            const linkPath = link.getAttribute('href');
            const normalizedLinkPath = linkPath === '/' ? '/' : linkPath.replace(/\/$/, '');

            // Skip the root path for parent matching
            if (normalizedLinkPath === '/') {
                return;
            }

            // Check if the current path starts with this link path
            if (normalizedPath.startsWith(normalizedLinkPath + '/')) {
                console.log('Navigation Helper: Parent match found:', normalizedLinkPath);
                markLinkActive(link);
            }
        });
    }

    // If still no match found, default to home if we're on a non-standard page
    if (!exactMatchFound && normalizedPath !== '/') {
        const homeLink = document.querySelector('#main-navigation a[href="/"]');
        if (homeLink) {
            console.log('Navigation Helper: No match found, defaulting to home');
            markLinkActive(homeLink);
        }
    }
}

/**
 * Marks a navigation link as active and handles parent elements
 *
 * @param {HTMLElement} link - The link element to mark as active
 */
function markLinkActive(link) {
    // Add active classes to the link
    link.classList.add('active-nav-item');
    link.classList.add('bg-gray-700');
    link.classList.add('text-white');

    // Find and activate the list item containing this link
    const listItem = link.closest('li.nav-item');
    if (listItem) {
        listItem.classList.add('active');
    }

    // Find and activate the parent category
    const category = link.closest('li.nav-category');
    if (category) {
        category.classList.add('active');

        // Highlight the category header
        const categoryHeader = category.querySelector('h3');
        if (categoryHeader) {
            categoryHeader.classList.add('text-white');
            categoryHeader.classList.remove('text-gray-500');
        }
    }
}

/**
 * Initializes mobile navigation functionality
 */
function initMobileNavigation() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');

    if (sidebarToggle && sidebar && sidebarOverlay) {
        // Toggle sidebar on mobile
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('hidden');
        });

        // Close sidebar when clicking overlay
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('open');
            this.classList.add('hidden');
        });
    }
}

/**
 * Adds tooltips to navigation items
 */
function addNavigationTooltips() {
    const navItems = document.querySelectorAll('#main-navigation a');

    navItems.forEach(item => {
        const title = item.getAttribute('title');
        if (title) {
            // Create tooltip element if it doesn't already exist
            if (!item.querySelector('.nav-tooltip')) {
                const tooltip = document.createElement('span');
                tooltip.className = 'nav-tooltip';
                tooltip.textContent = title;

                // Add tooltip to navigation item
                item.appendChild(tooltip);
            }
        }
    });
}

/**
 * Adds breadcrumb navigation based on current URL
 */
function addBreadcrumbNavigation() {
    const breadcrumbContainer = document.getElementById('breadcrumb-container');
    if (!breadcrumbContainer) return;

    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(segment => segment !== '');

    // Create breadcrumb HTML
    let breadcrumbHTML = `
        <a href="/" class="hover:text-white transition-colors">Home</a>
    `;

    let currentPathBuildup = '';

    // Add each path segment to breadcrumb
    pathSegments.forEach((segment, index) => {
        currentPathBuildup += `/${segment}`;

        // Format segment name for display
        const displayName = segment
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');

        breadcrumbHTML += `
            <i class="fas fa-chevron-right mx-2 text-xs"></i>
        `;

        // If it's the last segment, don't make it a link
        if (index === pathSegments.length - 1) {
            breadcrumbHTML += `<span class="text-white">${displayName}</span>`;
        } else {
            breadcrumbHTML += `
                <a href="${currentPathBuildup}" class="hover:text-white transition-colors">
                    ${displayName}
                </a>
            `;
        }
    });

    // Set breadcrumb HTML
    breadcrumbContainer.innerHTML = breadcrumbHTML;
}

/**
 * Initializes workflow navigation
 */
function initWorkflowNavigation() {
    // Get the current path
    const currentPath = window.location.pathname;

    // Determine the current module based on the path
    let currentModule = null;

    if (currentPath.startsWith('/trendsense')) {
        currentModule = 'trendsense';
    } else if (currentPath.startsWith('/trendradar')) {
        currentModule = 'trendradar';
    } else if (currentPath.startsWith('/vc-lens')) {
        currentModule = 'vc_lens';
    } else if (currentPath.startsWith('/graph-analytics')) {
        currentModule = 'vc_lens';
    } else if (currentPath.startsWith('/lifecycle')) {
        currentModule = 'vc_lens';
    } else if (currentPath.startsWith('/strategy')) {
        currentModule = 'strategy';
    }

    // Update workflow navigation if we have a current module
    if (currentModule) {
        updateWorkflowNavigation(currentModule);
    }
}

/**
 * Updates workflow navigation based on current page
 * @param {string} currentModule - The current module name
 */
function updateWorkflowNavigation(currentModule) {
    const workflowContainer = document.getElementById('workflow-navigation');
    if (!workflowContainer) return;

    // Define workflow steps for different modules
    const workflows = {
        'trendsense': [
            { name: 'TrendSense', path: '/trendsense', icon: 'chart-line', active: true },
            { name: 'TrendRadar', path: '/trendradar', icon: 'chart-pie', active: false },
            { name: 'VC Lens', path: '/vc-lens', icon: 'search-dollar', active: false },
            { name: 'Strategy Hub', path: '/strategy', icon: 'chess', active: false }
        ],
        'trendradar': [
            { name: 'TrendSense', path: '/trendsense', icon: 'chart-line', active: false },
            { name: 'TrendRadar', path: '/trendradar', icon: 'chart-pie', active: true },
            { name: 'VC Lens', path: '/vc-lens', icon: 'search-dollar', active: false },
            { name: 'Strategy Hub', path: '/strategy', icon: 'chess', active: false }
        ],
        'vc_lens': [
            { name: 'TrendSense', path: '/trendsense', icon: 'chart-line', active: false },
            { name: 'TrendRadar', path: '/trendradar', icon: 'chart-pie', active: false },
            { name: 'VC Lens', path: '/vc-lens', icon: 'search-dollar', active: true },
            { name: 'Strategy Hub', path: '/strategy', icon: 'chess', active: false }
        ],
        'strategy': [
            { name: 'TrendSense', path: '/trendsense', icon: 'chart-line', active: false },
            { name: 'TrendRadar', path: '/trendradar', icon: 'chart-pie', active: false },
            { name: 'VC Lens', path: '/vc-lens', icon: 'search-dollar', active: false },
            { name: 'Strategy Hub', path: '/strategy', icon: 'chess', active: true }
        ]
    };

    // Get workflow for current module
    const workflow = workflows[currentModule];
    if (!workflow) return;

    // Create workflow HTML
    let workflowHTML = `
        <div class="flex items-center justify-center space-x-4">
    `;

    // Add each workflow step
    workflow.forEach((step, index) => {
        const activeClass = step.active ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-300';

        workflowHTML += `
            <a href="${step.path}" class="flex flex-col items-center group">
                <div class="${activeClass} w-12 h-12 rounded-full flex items-center justify-center mb-2 group-hover:bg-blue-500 transition-colors">
                    <i class="fas fa-${step.icon}"></i>
                </div>
                <span class="text-xs ${step.active ? 'text-white' : 'text-gray-400'}">${step.name}</span>
            </a>
        `;

        // Add connector line between steps (except after the last step)
        if (index < workflow.length - 1) {
            workflowHTML += `
                <div class="w-8 h-0.5 bg-gray-700"></div>
            `;
        }
    });

    workflowHTML += `
        </div>
    `;

    // Set workflow HTML
    workflowContainer.innerHTML = workflowHTML;
}
