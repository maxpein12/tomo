document.addEventListener("DOMContentLoaded", function() {
    const calendarBody = document.getElementById('calendarBody');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');

    let currentDate = new Date();

    function renderCalendar() {
        calendarBody.innerHTML = '';

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        // Get the first and last day of the month
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);

        // Find out the day the month starts and ends on
        const startDay = firstDay.getDay();
        const totalDays = lastDay.getDate();

        // Update the current month in the header
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        currentMonthElement.innerText = `${monthNames[month]} ${year}`;

        let daysHTML = '';
        let dayCount = 0;

        // Create empty cells for days before the first day of the month
        for (let i = 0; i < startDay; i++) {
            daysHTML += '<td class="empty"></td>';
            dayCount++;
        }

        // Add the days of the month
        for (let day = 1; day <= totalDays; day++) {
            if (dayCount % 7 === 0) {
                daysHTML += '<tr>';
            }

            // Highlight the current day
            const today = new Date();
            if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                daysHTML += `<td class="current-day">${day}</td>`;
            } else {
                daysHTML += `<td>${day}</td>`;
            }

            dayCount++;

            if (dayCount % 7 === 0) {
                daysHTML += '</tr>';
            }
        }

        // Fill in the remaining cells of the last row
        while (dayCount % 7 !== 0) {
            daysHTML += '<td class="empty"></td>';
            dayCount++;
        }

        calendarBody.innerHTML = daysHTML;
    }

    // Event listeners for previous and next month buttons
    prevMonthBtn.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextMonthBtn.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    // Render the initial calendar
    renderCalendar();
});
