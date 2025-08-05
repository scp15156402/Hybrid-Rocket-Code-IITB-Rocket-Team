// Enhanced Dark Mode Toggle with Smooth Transitions
document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.getElementById('dark-mode-toggle');
  const icon = document.getElementById('dark-mode-icon');
  const html = document.documentElement;

  // Check for saved theme preference or default to light mode
  const savedTheme = localStorage.getItem('darkMode');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  let isDark = false;
  if (savedTheme !== null) {
    isDark = savedTheme === 'true';
  } else {
    isDark = systemPrefersDark;
  }

  // Apply theme without transition for initial load
  applyDarkMode(isDark, false);

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('darkMode') === null) {
      applyDarkMode(e.matches, true);
    }
  });

  // Handle manual toggle
  toggleButton.addEventListener('click', () => {
    const currentlyDark = html.hasAttribute('data-theme') && 
                          html.getAttribute('data-theme') === 'dark';
    const nextState = !currentlyDark;
    
    applyDarkMode(nextState, true);
    localStorage.setItem('darkMode', String(nextState));
  });

  function applyDarkMode(enabled, withTransition = true) {
    // Add transition class for smooth switching
    if (withTransition) {
      html.classList.add('theme-transition');
      
      // Remove transition class after animation completes
      setTimeout(() => {
        html.classList.remove('theme-transition');
      }, 300);
    }

    // Apply theme
    if (enabled) {
      document.getElementById('dark-style').disabled = !enabled;
      icon.className = 'bi bi-sun';
      icon.setAttribute('aria-label', 'Switch to light mode');
    } else {
      html.removeAttribute('data-theme');
      icon.className = 'bi bi-moon';
      icon.setAttribute('aria-label', 'Switch to dark mode');
    }

    // Update meta theme-color for mobile browsers
    updateMetaThemeColor(enabled);
  }

  function updateMetaThemeColor(isDark) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
      metaThemeColor = document.createElement('meta');
      metaThemeColor.name = 'theme-color';
      document.head.appendChild(metaThemeColor);
    }
    
    metaThemeColor.content = isDark ? '#0f172a' : '#ffffff';
  }
});

// Add smooth transition styles
const transitionStyles = `
  .theme-transition * {
    transition: background-color 0.3s ease, 
                border-color 0.3s ease, 
                color 0.3s ease,
                box-shadow 0.3s ease !important;
  }
`;

// Inject transition styles
const styleSheet = document.createElement('style');
styleSheet.textContent = transitionStyles;
document.head.appendChild(styleSheet);