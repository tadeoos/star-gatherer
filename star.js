// document.getElementById("").innerHTML = "Hello World!";
console.log('check')

/* Toggle Nav with Raw JavaScript */
// Set variables for key elements
var reddit = document.getElementById('nav-red');
console.log(reddit);
var main_reddit = document.getElementsByClassName('reddit');

// Start by adding the class "collapse" to the reddit
// main_reddit[0].classList.add('collapsed');

// Establish a function to toggle the class "collapse"
function redditToggle() {
    main_reddit[0].classList.toggle('collapsed');
}

// Add a click event to run the redditToggle function
reddit.addEventListener('click', redditToggle);
