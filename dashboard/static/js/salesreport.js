

const menuButton = document.getElementById('menuButton');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');

menuButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    mainContent.classList.toggle('hidden'); // Toggle the main content's hidden class
});

// Get all the menu items
const menuItems = document.querySelectorAll('.menu-item');

// Loop through each menu item and add a click event listener
menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
        // Prevent the default action of the link (optional)
        // event.preventDefault();

        // Remove the 'active' class from all menu items
        menuItems.forEach(i => i.classList.remove('active'));

        // Add the 'active' class to the clicked menu item
        this.classList.add('active');
    });
});


const stars = document.querySelectorAll('.star-rating input');
const ratingOutput = document.getElementById('rating-output');

stars.forEach(star => {
    star.addEventListener('change', (event) => {
        const ratingValue = event.target.value;
        ratingOutput.textContent = `You rated this ${ratingValue} star${ratingValue > 1 ? 's' : ''}.`;
    });
});


document.querySelectorAll('.favorites').forEach(icon => {
    icon.addEventListener('click', function() {
        this.classList.toggle('favorited');
        
        // Change icon based on favorited state
        const iconImage = this.querySelector('.favorites-icon');
        if (this.classList.contains('favorited')) {
            iconImage.src = 'https://www.svgrepo.com/show/422431/favorite-heart-interface.svg'; // Update to a filled heart or similar
        } else {
            iconImage.src = 'https://www.svgrepo.com/show/54280/favorite.svg'; // Original icon
        }
    });
});
