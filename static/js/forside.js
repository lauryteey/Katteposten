const openMenu = document.getElementById('open-menu');
const closeMenu = document.getElementById('close-menu');
const sideMenu = document.getElementById('side-menu');
const overlay = document.getElementById('overlay');

// Open side menu
openMenu.addEventListener('click', () => {
  sideMenu.classList.add('active');
  overlay.classList.add('active');
});

// Close side menu bye bye
closeMenu.addEventListener('click', () => {
  sideMenu.classList.remove('active');
  overlay.classList.remove('active');
});

overlay.addEventListener('click', () => {
  sideMenu.classList.remove('active');
  overlay.classList.remove('active');
});
