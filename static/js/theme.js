// Function to apply theme across the entire application
function applyTheme(theme) {
    if (theme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
        document.documentElement.setAttribute('data-theme', theme);
    }
    localStorage.setItem('theme', theme);
}

// Function to initialize theme on page load
function initializeTheme() {
    let theme = localStorage.getItem('theme') || 'system';
    applyTheme(theme);
}

// Initialize theme when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTheme);

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if ((localStorage.getItem('theme') || 'system') === 'system') {
        applyTheme('system');
    }
});