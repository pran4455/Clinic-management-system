// Function to enable fields and button
function enableFieldsAndButton() {
  document.getElementById("otp").disabled = false;
  document.getElementById("new-password").disabled = false;
  document.getElementById("confirm-password").disabled = false;
  document.getElementById("reset-password-button").disabled = false
}

// Function to disbable fields and button
function disableFieldsAndButton() {
  document.getElementById("otp").disabled = true;
  document.getElementById("new-password").disabled = true;
  document.getElementById("confirm-password").disabled = true;
  document.getElementById("reset-password-button").disabled = true
}


// Event listener for Send OTP button click
window.onload=function(){ // Wait for the webpage to load all the DOM contents or else
  // add the script tag to the end of the page, i.e end of the body
  // because the script gets executed even before the content
  // of the webpage loads up

  disableFieldsAndButton(); // initally we disable the fields and buttons
  // necessary because if the page reloads, then we need to disable the fields and btns

  sendOTPButton = document.getElementById("send-otp-button");
  sendOTPButton.addEventListener("click", enableFieldsAndButton);

}

