// Add an event listener to each edit button
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        alert('Edit function coming soon!');
    });
});

const menuButton = document.getElementById('menuButton');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');


menuButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    mainContent.classList.toggle('hidden'); // Toggle the main content's hidden class

});