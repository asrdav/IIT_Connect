$(document).ready(function() {
    $("#profile-image-submit").on("change", function(){

        var data = {};

        var file = this.files[0]

        console.log(file);

        var form = $("#fupForm");
        var formData = new FormData(form[0]);
        var token  = $('#csrfmiddlewaretoken').val();

        $.ajax({
            url: "./upload",
            type: "POST",

//            processData: false,
//            contentType: 'application/octet-stream',

            data: {
                fileData: file.name,
                csrfmiddlewaretoken: token
                },
            success : function(json) {
            //    alert("Successfully sent the URL to Django");
//                window.location.href=  './upload';
            },
            error : function(xhr, textStatus, errorThrown) {
 //               alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
            }
        });
    });
});



//
////
////
////const userImage = document.getElementsByClassName('user-image');
//////  const backUp = userImage.src;
////console.log(userImage);
////  const fupForm = document.getElementsByClassName('fupForm');
////  const imageUsername = document.getElementsByClassName('image-username');
////  const imageSubmit = document.getElementsByClassName('profile-image-submit');
////
////    console.log(imageSubmit);
////
////imageSubmit.addEventListener("change", (event) => {
////  iitpConnect.startLoader();
////  userImage.setAttribute("src", baseUrl + '/src/image/load.gif');
////  setTimeout(function() {
////    updateProfileImage(event);
////  }, 1000);
////});
////
////
////// Update user profile.
////const updateProfileImage = (event) => {
////
////  const xhttp = new XMLHttpRequest();
////  const url = baseUrl + '/src/Upload.php';
////  const method = 'POST';
////
////  xhttp.open(method, url, true);
////
////    xhttp.onreadystatechange = function() {
////      if(this.readyState == 4 && this.status == 200) {
////        const responseData = JSON.parse(xhttp.responseText);
////
////
////        userImage.setAttribute("src", baseUrl + '/src/image/load.gif');
////
////        if(responseData.response == 'error') {
////          userImage.setAttribute("src", backUp);
////          iitpConnect.renderMessage(responseData.text, responseData.response);
////          iitpConnect.stopLoader();
////        }
////        else if(responseData.response == 'success') {
////          iitpConnect.renderMessage(responseData.text, responseData.response);
////          userImage.setAttribute("src", baseUrl + '/' + responseData.path);
////          imageSubmit.value = imageSubmit.defaultValue;
////          iitpConnect.stopLoader();
////        }
////      }
////
////      if(this.status == 400 || this.status == 500) {
////        console.log('Server Error');
////        iitpConnect.renderMessage('Server error try again.','warning',5000);
////        iitpConnect.stopLoader();
////      }
////    };
////
////    const formData = new FormData(fupForm);
////    formData.append('tok', tok.value);
////    xhttp.send(formData);
////    event.preventDefault();
////};
