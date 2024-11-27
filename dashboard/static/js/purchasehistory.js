const sidebarLinks = document.querySelectorAll('.menu-item');
sidebarLinks.forEach(link => {
    link.addEventListener('click', function() {
        sidebarLinks.forEach(item => item.classList.remove('active'));
        this.classList.add('active');
    });
});

// Filter Orders by Status
document.getElementById('filter-orders').addEventListener('click', function() {
    const filterValue = document.getElementById('status-filter').value;
    const orderRows = document.querySelectorAll('#order-table tbody tr');
    orderRows.forEach(row => {
        const orderStatus = row.getAttribute('data-status');
        if (filterValue === 'all' || orderStatus === filterValue) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Reset Filters
document.getElementById('reset-filters').addEventListener('click', function() {
    document.getElementById('status-filter').value = 'all';
    const orderRows = document.querySelectorAll('#order-table tbody tr');
    orderRows.forEach(row => {
        row.style.display = '';
    });
});

// Search Functionality
document.querySelector('.search-bar input').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const orderRows = document.querySelectorAll('#order-table tbody tr');
    orderRows.forEach(row => {
        const customerName = row.cells[1].textContent.toLowerCase();
        if (customerName.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

document.getElementById('applyFilter').addEventListener('click', function() {
    const dateFilter = document.getElementById('filter-date').value;
    const orderTypeFilter = document.getElementById('filter-order-type').value;
    const orderStatusFilter = document.getElementById('filter-order-status').value;

    // Logic to filter the table or data goes here.
    console.log('Date Filter:', dateFilter);
    console.log('Order Type Filter:', orderTypeFilter);
    console.log('Order Status Filter:', orderStatusFilter);

    // You can add code here to filter your table rows based on these values.

    // Close the modal after applying the filter
    const filterModal = new bootstrap.Modal(document.getElementById('filterModal'));
    filterModal.hide();
});

// Optionally handle reset
document.querySelector('.reset-filter-button').addEventListener('click', function() {
    document.getElementById('filter-date').selectedIndex = 0;
    document.getElementById('filter-order-type').selectedIndex = 0;
    document.getElementById('filter-order-status').selectedIndex = 0;

    // Code to reset the table view goes here.
    
});
