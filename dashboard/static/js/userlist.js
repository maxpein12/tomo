// Show the form and hide the contact list
document.getElementById('add-contact-btn').addEventListener('click', function () {
  document.getElementById('contact-list').style.display = 'none';
  document.getElementById('contact-input-container').style.display = 'block';
});

// Save the new contact and show the contact list again
document.getElementById('save-contact-btn').addEventListener('click', function () {
  const name = document.getElementById('new-contact-name').value;
  const email = document.getElementById('new-contact-email').value;
  const picturePreviewSrc = document.getElementById('contact-picture-preview').src;

  if (name === '' || email === '' || picturePreviewSrc === '#') return;

  const contactList = document.getElementById('contact-list');

  // Create a new list item
  const newContact = document.createElement('li');
  newContact.classList.add('contact');

  newContact.innerHTML = `
    <img src="${picturePreviewSrc}" alt="Profile Picture" class="profile-picture">
    <div class="contact-info">
      <span class="contact-name">${name}</span>
      <span class="contact-email">${email}</span>
      <button class="message-btn">Message</button>
    </div>
  `;

  contactList.appendChild(newContact);

  document.getElementById('new-contact-name').value = '';
  document.getElementById('new-contact-email').value = '';
  document.getElementById('new-contact-picture').value = '';
  document.getElementById('contact-picture-preview').style.display = 'none';

  document.getElementById('contact-list').style.display = 'flex';
  document.getElementById('contact-input-container').style.display = 'none';
});

// Cancel the new contact and restore the contact list
document.getElementById('cancel-contact-btn').addEventListener('click', function () {
  document.getElementById('new-contact-name').value = '';
  document.getElementById('new-contact-email').value = '';
  document.getElementById('new-contact-picture').value = '';
  document.getElementById('contact-picture-preview').style.display = 'none';

  document.getElementById('contact-list').style.display = 'flex';
  document.getElementById('contact-input-container').style.display = 'none';
});

// Display image preview when an image is uploaded
document.getElementById('new-contact-picture').addEventListener('change', function (event) {
  const file = event.target.files[0]; // Get the uploaded file
  const reader = new FileReader();

  // Check if a file was uploaded
  if (file) {
    reader.onload = function (e) {
      const preview = document.getElementById('contact-picture-preview'); // Select the preview element
      preview.src = e.target.result; // Set the preview source to the uploaded image
      preview.style.display = 'block'; // Make sure the image is visible
    };
    reader.readAsDataURL(file); // Convert the file into a base64 URL for preview
  }
});


document.getElementById('newProfilePhoto').addEventListener('change', function (event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  if (file) {
      reader.onload = function (e) {
          document.getElementById('profilePic').src = e.target.result;
      };
      reader.readAsDataURL(file);
  }
});



// Handle profile picture selection and preview
document.addEventListener('change', function (event) {
  if (event.target.classList.contains('uploadProfileInput')) {
    const triggerInput = event.target;
    const holder = triggerInput.closest('.pic-holder');
    const wrapper = triggerInput.closest('.profile-pic-wrapper');
    const currentImg = holder.querySelector('.pic').src;

    triggerInput.blur();
    const files = triggerInput.files || [];

    if (!files.length || !window.FileReader) return;

    if (/^image/.test(files[0].type)) {
      const reader = new FileReader();
      reader.readAsDataURL(files[0]);

      reader.onloadend = function () {
        holder.classList.add('uploadInProgress');
        holder.querySelector('.pic').src = this.result;

        const loader = document.createElement('div');
        loader.classList.add('upload-loader');
        loader.innerHTML =
          '<div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div>';
        holder.appendChild(loader);

        setTimeout(function () {
          holder.classList.remove('uploadInProgress');
          loader.remove();

          // Show a snackbar notification when the picture is updated
          const snackbar = document.createElement('div');
          snackbar.className = 'snackbar';
          snackbar.innerText = 'Profile picture updated!';
          wrapper.appendChild(snackbar);
          snackbar.classList.add('show');
          setTimeout(() => snackbar.classList.remove('show'), 3000);
        }, 1500);
      };
    }
  }
});
function searchContacts() {
  var li = document.getElementsByClassName("contact");
  let input = document.getElementById('search').value.toLowerCase();
  let status = document.getElementById('status').value;
  let sortOrder = document.getElementById('status').value;

  let count = 0; // Initialize a variable to count the number of results

  // Filter the contacts based on the search input and status
  for (i = 0; i < li.length; i++) {
    let name = li[i].querySelector('.contact-name').textContent.toLowerCase();
    let email = li[i].querySelector('.contact-email').textContent.toLowerCase();
    let ageVerified = li[i].querySelector('#age-verified').textContent.toLowerCase();
    let onlineOfflineStatus = li[i].querySelector('.message-btn').textContent.toLowerCase();

    if (status !== "all") {
      if (status === "online" && onlineOfflineStatus === "online") {
        li[i].style.display = "block";
        count++; // Increment the count if the contact is displayed
      } else if (status === "offline" && onlineOfflineStatus === "offline") {
        li[i].style.display = "block";
        count++; // Increment the count if the contact is displayed
      } else if (status === "It was not accepted due to a comprehensive judgement." && ageVerified.includes("it was not accepted due to a comprehensive judgement")) {
        li[i].style.display = "block";
        count++; // Increment the count if the contact is displayed
      } else if (ageVerified.includes(status)) {
        li[i].style.display = "block";
        count++; // Increment the count if the contact is displayed
      } else {
        li[i].style.display = "none";
      }
    } else if (input !== "" && (!name.includes(input) && !email.includes(input))) {
      li[i].style.display = "none";
    } else {
      li[i].style.display = "block";
      count++; // Increment the count if the contact is displayed
    }
  }

  // Update the count display
  document.getElementById('total-users-count').innerHTML = count;

  // If the sort order is 'newest' or 'oldest', send a request to the server to re-sort the data
  if (sortOrder === "newest" || sortOrder === "oldest") {
    let url = window.location.href;
    let params = new URLSearchParams(url.split('?')[1]);
    params.set('sort', sortOrder);
    window.location.href = url.split('?')[0] + '?' + params.toString();
  }
}

// function updateTotalUsersCount() {
//   console.log('updateTotalUsersCount called'); // Add this line to see if the function is being called
//   var filterValue = document.getElementById('status').value;
//   var url = "{{ url 'update_total_users_count' }}"; // URL of the new view
//   var data = {'filter': filterValue, 'csrfmiddlewaretoken': '{{ csrf_token }}'};

//   $.ajax({
//     type: 'POST',
//     url: url,
//     data: data,
//     success: function(response) {
//       document.getElementById('total-users-count').innerHTML = response.total_users;
//     }
//   });
// }


// var pkuser = '{{ user_with_post_count.user.pk }}';
// var img = document.getElementById('profile-picture');

// // Make an AJAX request to get the profile photo
// var xhr = new XMLHttpRequest();
// xhr.open('GET', '/get_profile_photo/' + pkuser, true);
// xhr.onload = function() {
//   if (xhr.status === 200) {
//     img.src = xhr.responseText;
//   }
// };
// xhr.send();

