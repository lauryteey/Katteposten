// const for å hete elementene fra html til side menu
document.addEventListener('DOMContentLoaded', function() {
    const openMenu = document.getElementById('open-menu');
    const closeMenu = document.getElementById('close-menu');
    const sideMenu = document.getElementById('side-menu');
    const overlay = document.getElementById('overlay');
  
    if (openMenu && closeMenu && sideMenu && overlay) {
      openMenu.addEventListener('click', () => {
        sideMenu.classList.add('active');
        overlay.classList.add('active');
      });
  
      closeMenu.addEventListener('click', () => {
        sideMenu.classList.remove('active');
        overlay.classList.remove('active');
      });
  
      overlay.addEventListener('click', () => {
        sideMenu.classList.remove('active');
        overlay.classList.remove('active');
      });
    }
  });
  
