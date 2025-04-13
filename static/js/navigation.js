
const navBarMenu = document.querySelector('.navbar_menu'); //primaryNav
const hamburger = document.querySelector('.hamburger_menu'); //NavToggle


hamburger.addEventListener('click', () =>{
    const visibility = navBarMenu.getAttribute('data-visible')
    if(visibility === "false"){
        navBarMenu.setAttribute('data-visible', 'true')
        hamburger.setAttribute('aria-expanded', 'true')
    } else {
        visibility === "true"
        navBarMenu.setAttribute('data-visible', 'false')
        hamburger.setAttribute('aria-expanded', 'false')
        visibility = "false"
    }
})


// Close mobile menu when any nav link is clicked (especially anchor scrolls)
const navLinks = document.querySelectorAll('.navbar_menu .navbar_links');
const sunMoonLink = document.querySelector('.moon-sun')

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        const visibility = navBarMenu.getAttribute('data-visible');
        if (visibility === "true") {
            navBarMenu.setAttribute('data-visible', 'false');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });

    sunMoonLink.addEventListener('click', () => {
        const visibility = navBarMenu.getAttribute('data-visible');
        if (visibility === "true") {
            navBarMenu.setAttribute('data-visible', 'false');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });
});