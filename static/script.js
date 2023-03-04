/* script.js */

// Get the popup and the button that opens it
var popup = document.querySelector('.popup');
var popupBtn = document.getElementById('popup-btn');

// Get the close button
var closeBtn = document.querySelector('.close');

// Open the popup when the button is clicked
popupBtn.onclick = function() {
	popup.style.display = "block";
}

// Close the popup when the close button is clicked
closeBtn.onclick = function() {
	popup.style.display = "none";
}

// Close the popup when the user clicks outside of it
window.onclick = function(event) {
	if (event.target == popup) {
		popup.style.display = "none";
	}
}
