// When the "show-delete-form" button is clicked
document.getElementById("show-delete-form").addEventListener("click", function () {

  // Show the delete form by setting its display to "block"
  document.getElementById("delete-form").style.display = "block";

  // Hide the button that was clicked
  this.style.display = "none";
});


