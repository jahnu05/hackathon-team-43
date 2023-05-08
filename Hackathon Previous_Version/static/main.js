// Get the user's name from a cookie
var userName = getCookie("username");

// Display the user's name on the page
document.write("Welcome, " + userName + "!");

// Function to get a cookie by name
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) {
    return parts.pop().split(";").shift();
  }
}
