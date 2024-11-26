document.getElementById('add-task-btn').addEventListener('click', function () {
    document.getElementById('task-input-container').style.display = 'block';
});

document.getElementById('save-task-btn').addEventListener('click', function () {
    const taskText = document.getElementById('new-task-input').value;

    if (taskText === '') return; // Don't add empty tasks

    const taskList = document.getElementById('task-list');

    // Create a new list item
    const newTask = document.createElement('li');
    newTask.classList.add('task');

    // Task HTML structure
    newTask.innerHTML = `
    <div class="chck-box-tx">
    <input type="checkbox">

        </div>
        <span>${taskText}</span>
        <div class="star-dlt-btn">
                        <button class="star-btn">&#9734;</button>
                        <button class="delete-btn">&times;</button>
                    </div>
    `;

    taskList.appendChild(newTask);

    // Clear the input field and hide the input form
    document.getElementById('new-task-input').value = '';
    document.getElementById('task-input-container').style.display = 'none';

    // Add event listeners for the newly added task
    newTask.querySelector('.delete-btn').addEventListener('click', function () {
        newTask.remove();
    });

    newTask.querySelector('.star-btn').addEventListener('click', function () {
        this.innerHTML = this.innerHTML === '&#9734;' ? '&#9733;' : '&#9734;';
    });
});
