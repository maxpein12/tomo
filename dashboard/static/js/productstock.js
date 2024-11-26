// Search Functionality
const searchBar = document.querySelector('.search-bar');
const tableRows = document.querySelectorAll('tbody tr');

searchBar.addEventListener('input', function () {
    const searchTerm = searchBar.value.toLowerCase();
    tableRows.forEach(row => {
        const productName = row.cells[1].textContent.toLowerCase();
        if (productName.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Pagination (for demo purposes, we can add a function to load different pages)
const prevButton = document.querySelector('.pagination-controls button:first-child');
const nextButton = document.querySelector('.pagination-controls button:last-child');

prevButton.addEventListener('click', function () {
    console.log('Previous page');
});

nextButton.addEventListener('click', function () {
    console.log('Next page');
});
