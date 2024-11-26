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
