// $(function() {

// 	// Get the form.
// 	var form = $('#contact-form');

// 	// Get the messages div.
// 	var formMessages = $('.ajax-response');

// 	// Set up an event listener for the contact form.
// 	$(form).submit(function(e) {
// 		// Stop the browser from submitting the form.
// 		e.preventDefault();

// 		// Serialize the form data.
// 		var formData = $(form).serialize();

// 		// Submit the form using AJAX.
// 		$.ajax({
// 			type: 'POST',
// 			url: $(form).attr('action'),
// 			data: formData
// 		})
// 		.done(function(response) {
// 			// Make sure that the formMessages div has the 'success' class.
// 			$(formMessages).removeClass('error');
// 			$(formMessages).addClass('success');

// 			// Set the message text.
// 			$(formMessages).text(response);

// 			// Clear the form.
// 			$('#contact-form input,#contact-form textarea').val('');
// 		})
// 		.fail(function(data) {
// 			// Make sure that the formMessages div has the 'error' class.
// 			$(formMessages).removeClass('success');
// 			$(formMessages).addClass('error');

// 			// Set the message text.
// 			if (data.responseText !== '') {
// 				$(formMessages).text(data.responseText);
// 			} else {
// 				$(formMessages).text('Oops! An error occured and your message could not be sent.');
// 			}
// 		});
// 	});

// });


document.getElementById('addTo-Cart').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default anchor behavior
    var quantity = document.getElementById("qty-cart").value;
    var foodId = document.getElementById("foodId").value;
//    alert(quantity+" "+foodId);
    var response = confirm("Do you want to Add into Cart");
    if(response)
    {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content; 
    fetch('/addToCart/'+foodId+'/'+quantity, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken 
        }
    })
    .then(response => {
        alert("Food Item added to the Cart");  
        location.reload();      // Handle response
    })
    .catch(error => {
        alert("error");    // Handle error
    });
}
});