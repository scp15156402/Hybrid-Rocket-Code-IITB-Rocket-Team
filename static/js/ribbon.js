// static/ribbon.js

document.addEventListener('DOMContentLoaded', () => {
  const ribbon       = document.getElementById('ribbon');
  const collapseIcon = document.getElementById('collapse-icon');
  const collapseBtn  = document.getElementById('collapse-btn');
  const tabButtons   = document.querySelectorAll('.ribbon-tabs button');
  const panels       = document.querySelectorAll('.ribbon-panel');

  // Restore previous collapsed state
  const collapsed = sessionStorage.getItem('ribbonCollapsed') === 'true';
  ribbon.classList.toggle('collapsed', collapsed);
  collapseBtn.style.display = collapsed ? 'none' : 'block';  // Hide chevron when collapsed
  collapseIcon.classList.toggle('bi-chevron-down', collapsed);
  collapseIcon.classList.toggle('bi-chevron-up', !collapsed);

  // Collapse ribbon (clears all highlights)
  window.toggleCollapse = function () {
    const nowCollapsed = ribbon.classList.toggle('collapsed');
    sessionStorage.setItem('ribbonCollapsed', nowCollapsed);
    collapseIcon.classList.toggle('bi-chevron-up', !nowCollapsed);
    collapseIcon.classList.toggle('bi-chevron-down', nowCollapsed);
    collapseBtn.style.display = nowCollapsed ? 'none' : 'block'; // Hide chevron when collapsed

    if (nowCollapsed) {
      // Clear all tab and panel highlights when collapsed
      tabButtons.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
    }
  };

  // Expand ribbon and activate tab when clicking any tab
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // If collapsed, expand first
      if (ribbon.classList.contains('collapsed')) {
        ribbon.classList.remove('collapsed');
        sessionStorage.setItem('ribbonCollapsed', false);
        collapseIcon.classList.remove('bi-chevron-down');
        collapseIcon.classList.add('bi-chevron-up');
        collapseBtn.style.display = 'block';
      }

      // Activate tab and matching panel
      tabButtons.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const activeTab = btn.getAttribute('data-tab');
      const targetPanel = document.getElementById(activeTab);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });
});
