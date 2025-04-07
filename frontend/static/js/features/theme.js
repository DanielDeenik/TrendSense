// Theme System
const ThemeManager = {
    init() {
        this.themeSwitch = document.getElementById('checkbox');
        this.htmlElement = document.documentElement;
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
        
        // Set initial switch state
        this.themeSwitch.checked = savedTheme === 'dark';
        
        // Add event listener
        this.themeSwitch.addEventListener('change', () => {
            const newTheme = this.themeSwitch.checked ? 'dark' : 'light';
            this.setTheme(newTheme);
        });
    },
    
    setTheme(theme) {
        this.htmlElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', theme === 'dark' ? '#1a1a1a' : '#ffffff');
        } else {
            const meta = document.createElement('meta');
            meta.name = 'theme-color';
            meta.content = theme === 'dark' ? '#1a1a1a' : '#ffffff';
            document.head.appendChild(meta);
        }
    }
};

// Initialize theme system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
}); 