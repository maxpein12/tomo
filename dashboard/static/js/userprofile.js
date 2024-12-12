function searchContacts() {
    let input = document.getElementById('search').value
    input = input.toLowerCase();
    let x = document.getElementsByClassName('contact-name');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display = "none";
        }
        else {
            x[i].style.display = "list-item";
        }
    }
}


// $(document).ready(function () {
//     UserDetails.getUserChatted();
//   });

  
//   UserDetails.getUserChatted = function () {
//     console.log('Getting user chat list...');
//     $.ajax({
//       type: 'GET',
//       url: '/UserList/' + Cookies.get('userid'),
//       dataType: 'json',
//       success: function (data) {
//         console.log('Received data:', data);
//         console.log('Data length:', data.length);
//         const userList = document.getElementById('user-chatted');
//         console.log('User list element:', userList);
//         userList.innerHTML = '';
  
//         data.forEach(function (user) {
//           console.log('Processing user:', user);
//           const msgCount = user.msg_count > 0 ? `<span>${user.msg_count}</span>` : '';
//           const userHtml = `
//             <div user-id="${user.pk}" class="user-chatted-container">
//               <span>${user.name}</span>
//               ${msgCount}
//             </div>
//           `;
//           userList.insertAdjacentHTML('beforeend', userHtml);
//         });
  
//         console.log('Chat list populated.');
//         document.querySelectorAll('.user-chatted-container').forEach(function (user) {
//           console.log('Adding click event listener to user:', user);
//           user.addEventListener('click', UserDetails.chattedClick);
//         });
//       },
//       error: function (xhr, status, error) {
//         console.log('Error:', error);
//       }
//     });
//   }

// Get the age_verified field


  const userList = document.getElementById('user-list');
const conversationDisplay = document.getElementById('conversation-display');

userList.addEventListener('click', (event) => {
  if (event.target.tagName === 'DIV') {
    const userId = event.target.getAttribute('data-user-id');
    const userName = event.target.getAttribute('data-user-name');
    // fetch conversation data from server using userId
    fetch(`/conversation/${userId}`)
      .then(response => response.json())
      .then(data => {
        // update conversation display
        conversationDisplay.innerHTML = '';
        data.messages.forEach((message) => {
          const messageHTML = `
            <div>
              <span>${message.from}</span>
              <span>${message.text}</span>
            </div>
          `;
          conversationDisplay.innerHTML += messageHTML;
        });
      });
  }
});
// Assuming you're using jQuery
$('#save-changes-button').click(function(event) {
  var ageVerificationValue = $('#id_age_verified').val();
  if (ageVerificationValue == 1) { // Assuming the value for "Reception Complete" is 1
    var subject = '身分証の承認が完了しました。';
    var body = '沢山のおしゃべりを楽しんでください！初回特典として、無料メッセージポイントと無料通話ポイントを購入ページから選択できます！';
    var email = $('#id_email').val();
    var url = "https://mail.google.com/mail/?view=cm&fs=1&to=" + email + "&su=" + subject + "&body=" + body;
    window.open(url, '_blank');
  }
});
const menuButton = document.getElementById('menuButton');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');


menuButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    mainContent.classList.toggle('hidden'); // Toggle the main content's hidden class

});

// $(document).ready(function() {
//     var conversationUser = $("#chat-section").data("conversation-user");
//     if (conversationUser) {
//         var chartSection = $("#conversation-display");
//         $("html, body").animate({
//             scrollTop: chartSection.offset().top
//         }, 500);
//     }
// });


$(document).ready(function() {
  $('#template-button').on('click', function() {
    console.log('Select Template button clicked');
    $('#template-options').toggle();
  });

  $('#apply-template').on('click', function() {
    var selectedValue = $('#message-template').val();
    console.log('Apply Template button clicked');
    console.log('Selected value:', selectedValue);
    selectedValue = decodeURIComponent(selectedValue);
    $('textarea[name="data"]').val(selectedValue);
    $('#template-options').toggle();
  });
});