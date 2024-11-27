// Chart.js - Sales Chart Example
const ctx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        datasets: [{
            label: 'Sales',
            data: [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec],
            backgroundColor: 'rgba(52, 152, 219, 0.5)',
            fontColor: '#fff',
            borderColor: '#3498db',
            borderWidth: 2,
            fill: true,
            tension: 0.5,
            spanGaps: true
        }],
    },
    options: {
        scales: {
            y: {
                grid: {
                    color: "#6c757d"
                },
                beginAtZero: true,
                ticks: {
                    color: "white"
                }
            },
            x: {
                grid: {
                    color: "#6c757d"
                },
                ticks: {
                    color: "white"
                },
                beginAtZero: true
            }
        },
        grid: {
            color: "white"
        },
        responsive: true,
        plugins: {
            tooltip: {
                enabled: true
            }
        }
    }
});

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


// Handle dropdown toggles
const dropdowns = document.querySelectorAll('.dropdown-toggle');

// Toggle dropdown menu when clicked
dropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', function () {
        const parentDropdown = this.parentElement;
        parentDropdown.classList.toggle('show');
    });
});

// Hide dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-toggle')) {
        const openDropdowns = document.querySelectorAll('.dropdown');
        openDropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });
    }
};

// Language selection functionality
const languageLinks = document.querySelectorAll('.dropdown-menu a');
languageLinks.forEach(link => {
    link.addEventListener('click', function() {
        const selectedLang = this.dataset.lang;
        alert('You selected: ' + selectedLang);
    });
});

// Update the chart when the year filter changes
