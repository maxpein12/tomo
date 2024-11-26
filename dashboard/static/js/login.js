// // Validate the login form
// function validateLogin() {
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const errorMessage = document.getElementById('errorMessage');

//     // Simple validation: check if email and password are non-empty
//     if (email && password.length >= 4) {
//         $.ajax({
//             type: 'POST',
//             url: '/login',
//             data: {
//               // any data you want to pass to the view
//               email: email,
//               password: password
//             },
//             success: function(response) {
//               // handle the response from the view
//             }
//           });
//          } else {
//         errorMessage.textContent = "Please enter a valid email and password (6+ characters).";
//         errorMessage.style.display = "block";
//         return false;  // Prevent form submission
//     }
// }



$(document).ready(function(){

	// $('.container').css('height', $(window).height() + 'px');
	// $('.copyright').css('top', ($('.container').height() - 50) + 'px');

	$('#login-btn').click(function(){

		let request = {'email' : $('#email').val(), 'password' : $('#password').val()};

		Utilities.Post({

			url:"{% url 'login' %}",
			data:request,
			method:"POST",
			contenttype:"json",
			success:function(res){

				let jsonRes = JSON.parse(res);

				if(parseInt(jsonRes['status']) == 3){
					window.location = "{% url 'index' %}";
					// alert(JSON.stringify(request))
				}else{
					$('.warning-container').removeClass('hidden');
				}

			}

		});



	});

});