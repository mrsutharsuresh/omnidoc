// Theme Management
const ThemeManager = {
    init() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);

        // Attach click handlers if element exists
        const btn = document.querySelector('.theme-toggle');
        if (btn) {
            btn.addEventListener('click', () => this.toggle());
        }
    },

    toggle() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        this.setTheme(next);
    },

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Update Icon
        const icon = document.getElementById('themeIcon');
        if (icon) {
            if (icon.classList.contains('bi')) {
                // Class-based (Bootstrap Icons)
                icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
                icon.textContent = '';
            } else {
                // Text-based (Legacy/Emoji)
                icon.textContent = theme === 'dark' ? '☀️' : '🌙';
            }
        }

        // Update Syntax Highlight if present
        const highlightTheme = document.getElementById('highlightTheme');
        if (highlightTheme) {
            const cssUrl = theme === 'dark'
                ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css'
                : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css';
            highlightTheme.href = cssUrl;
        }
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
});

// Immediate apply to prevent flash (also call this inline in head if possible)
(function () {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();
