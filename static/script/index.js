const btnOpenMenu = document.querySelector('.burger'),
      menuMobile = document.querySelector('.menu-mobile'),
      btnCloseMenu = document.querySelector('.close span');


btnOpenMenu.addEventListener('click', () => {
    menuMobile.style.display = 'block';
    btnCloseMenu.addEventListener('click', () => {
        menuMobile.style.display = 'none';
    })
});


