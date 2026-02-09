/* responsive.js - Handles sidebar toggle for touch devices and small screens */

document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('sidebar');
  const hamburger = document.getElementById('hamburger');

  if (!sidebar || !hamburger) return;

  // Toggle function
  function toggleSidebar() {
    if (window.innerWidth <= 480) {
      // Mobile: use overlay class
      sidebar.classList.toggle('open');
    } else {
      // Tablet/Desktop: collapse/expand
      sidebar.classList.toggle('collapsed');
    }
  }

  // Click/tap on hamburger
  hamburger.addEventListener('click', toggleSidebar);
  hamburger.addEventListener('touchstart', function (e) {
    e.preventDefault(); // Prevent double-trigger on some browsers
    toggleSidebar();
  });

  // Optional: close sidebar when clicking outside (mobile overlay)
  document.addEventListener('click', function (e) {
    if (window.innerWidth <= 480 && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && e.target !== hamburger) {
        sidebar.classList.remove('open');
      }
    }
  });
});