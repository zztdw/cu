// Get time when the webpage is loaded
var startCountdownTime = new Date().getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // get time
  var now = new Date().getTime();
    
  // get 5 minutes countdown time
  var reminderMinutes = 5;
  var countDownTime = new Date(startCountdownTime + (reminderMinutes*60*1000));

  // Find the distance between now and the count down date
  var distance = countDownTime - now;

  // Time calculations for minutes and seconds
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="timer"
  document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";

  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "EXPIRED";
    window.alert("Please update time!");

  }
}, 1000);


