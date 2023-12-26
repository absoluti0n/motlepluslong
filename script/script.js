// Get the element with the class 'hover-word'
var hoverWord = document.querySelector('.hover-word');

// Get the pop-up element
var popup = document.getElementById('popup');

// Function to display pop-up
function showPopup() {
    popup.style.display = 'block';
}

// Function to hide pop-up
function hidePopup() {
    popup.style.display = 'none';
}

// Add event listeners for hovering
hoverWord.addEventListener('mouseover', showPopup);
hoverWord.addEventListener('mouseout', hidePopup);