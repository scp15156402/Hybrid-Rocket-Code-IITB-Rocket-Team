document.addEventListener('DOMContentLoaded', () => {
  const ribbon = document.getElementById('ribbon');
  const collapseIcon = document.getElementById('collapse-icon');
  const collapseBtn = document.getElementById('collapse-btn');
  const tabButtons = document.querySelectorAll('.ribbon-tabs button');

  // Restore previous collapsed state
  const collapsed = sessionStorage.getItem('ribbonCollapsed') === 'true';
  ribbon.classList.toggle('collapsed', collapsed);
  collapseBtn.style.display = collapsed ? 'none' : 'block';  // Hide chevron when collapsed
  collapseIcon.classList.toggle('bi-chevron-down', collapsed);
  collapseIcon.classList.toggle('bi-chevron-up', !collapsed);

  // Collapse ribbon
  window.toggleCollapse = function () {
    const nowCollapsed = ribbon.classList.toggle('collapsed');
    sessionStorage.setItem('ribbonCollapsed', nowCollapsed);
    collapseIcon.classList.toggle('bi-chevron-up', !nowCollapsed);
    collapseIcon.classList.toggle('bi-chevron-down', nowCollapsed);
    collapseBtn.style.display = nowCollapsed ? 'none' : 'block'; // Hide chevron when collapsed
  };

  // Expand ribbon when clicking any tab
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      if (ribbon.classList.contains('collapsed')) {
        ribbon.classList.remove('collapsed');
        sessionStorage.setItem('ribbonCollapsed', false);
        collapseIcon.classList.remove('bi-chevron-down');
        collapseIcon.classList.add('bi-chevron-up');
        collapseBtn.style.display = 'block';
      }

      // Activate tab and panel
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const activeTab = btn.getAttribute('data-tab');
      document.querySelectorAll('.ribbon-panel').forEach(panel => {
        panel.classList.toggle('active', panel.id === activeTab);
      });
    });
  });
});
