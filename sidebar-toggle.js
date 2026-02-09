/* sidebar-toggle.js - Touch-friendly sidebar toggle for responsive layout */

document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');

  if (!toggleBtn || !sidebar) {
    // No sidebar or toggle button present; nothing to do.
    return;
  }

  // Toggle sidebar visibility
  const toggleSidebar = () => {
    sidebar.classList.toggle('open');
  };

  // Click / tap handler
  toggleBtn.addEventListener('click', toggleSidebar);
  toggleBtn.addEventListener('touchend', function (e) {
    e.preventDefault(); // Prevent 300ms delay on some browsers
    toggleSidebar();
  });

  // Optional: close sidebar when clicking outside of it (mobile)
  document.addEventListener('click', function (e) {
    if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
});