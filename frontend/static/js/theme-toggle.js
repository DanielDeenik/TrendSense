// Theme Toggle Utility
const ThemeToggle = {
    STORAGE_KEY: 'sustainatrend-theme',
    DARK_CLASS: 'dark-theme',
    LIGHT_CLASS: 'light-theme',

    init() {
        this.theme = localStorage.getItem(this.STORAGE_KEY) || 'dark';
        this.applyTheme();
        this.setupListeners();
    },

    applyTheme() {
        document.body.classList.remove(this.DARK_CLASS, this.LIGHT_CLASS);
        document.body.classList.add(`${this.theme}-theme`);
        // Update any theme-specific elements
        document.querySelectorAll('[data-theme-update]').forEach(el => {
            el.setAttribute('data-theme', this.theme);
        });
    },

    toggle() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem(this.STORAGE_KEY, this.theme);
        this.applyTheme();
    },

    setupListeners() {
        document.querySelectorAll('[data-theme-toggle]').forEach(button => {
            button.addEventListener('click', () => this.toggle());
        });
    }
};

// Initialize theme system
document.addEventListener('DOMContentLoaded', () => ThemeToggle.init()); 