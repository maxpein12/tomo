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

// prevButton.addEventListener('click', function () {
//     console.log('Previous page');
// });

// nextButton.addEventListener('click', function () {
//     console.log('Next page');
// });

const menuButton = document.getElementById('menuButton');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');


menuButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    mainContent.classList.toggle('hidden'); // Toggle the main content's hidden class

});


function searchReports() {
    var rows = document.querySelectorAll('.table tbody tr');
    let input = document.getElementById('search').value.toLowerCase();
  
    for (i = 0; i < rows.length; i++) {
      let cells = rows[i].querySelectorAll('td');
      let match = false;
  
      for (j = 0; j < cells.length; j++) {
        let cellText = cells[j].textContent.toLowerCase();
        if (cellText.includes(input)) {
          match = true;
          break;
        }
      }
  
      if (match) {
        rows[i].style.display = 'table-row';
      } else {
        rows[i].style.display = 'none';
      }
    }
  }

  