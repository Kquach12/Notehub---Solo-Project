// Convert time to a format of hours, minutes, seconds, and milliseconds
let time1 

function timeToString(time) {
    let diffInHrs = time / 3600000;
    let hh = Math.floor(diffInHrs);

    let diffInMin = (diffInHrs - hh) * 60;
    let mm = Math.floor(diffInMin);

    let diffInSec = (diffInMin - mm) * 60;
    let ss = Math.floor(diffInSec);

    // let diffInMs = (diffInSec - ss) * 100;
    // let ms = Math.floor(diffInMs);

    let formattedHH = hh.toString().padStart(2, "0");
    let formattedMM = mm.toString().padStart(2, "0");
    let formattedSS = ss.toString().padStart(2, "0");
    // let formattedMS = ms.toString().padStart(2, "0");

    time1 = `${formattedHH}:${formattedMM}:${formattedSS}`
    return time1;
}

// Declare variables to use in our functions below

let startTime;
let elapsedTime = 0;
let timerInterval;

// Create function to modify innerHTML

function print(txt) {
    document.getElementById("display").innerHTML = txt;
    document.getElementById("timestamp").value = txt
}

// Create "start", "pause" and "reset" functions

function start() {
    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(function printTime() {
        elapsedTime = Date.now() - startTime;
        print(timeToString(elapsedTime));
    }, 10);
    showButton("PAUSE");
}

function pause() {
    clearInterval(timerInterval);
    showButton("PLAY");
}

function reset() {
    clearInterval(timerInterval);
    print("00:00:00");
    elapsedTime = 0;
    showButton("PLAY");
}

// Create function to display buttons

function showButton(buttonKey) {
    const buttonToShow = buttonKey === "PLAY" ? playButton : pauseButton;
    const buttonToHide = buttonKey === "PLAY" ? pauseButton : playButton;
    buttonToShow.style.display = "block";
    buttonToHide.style.display = "none";
}

// function record(){
//     console.log(time1)
//     console.log(document.getElementById('timestamp').value)
// }

// Create event listeners

let playButton = document.getElementById("playButton");
let pauseButton = document.getElementById("pauseButton");
let resetButton = document.getElementById("resetButton");

playButton.addEventListener("click", start);
pauseButton.addEventListener("click", pause);
resetButton.addEventListener("click", reset);



let myForm = document.getElementById('form')


function submit(){
    header = document.getElementById('header').value
    note = document.getElementById('note').value
    timestamp = document.getElementById('timestamp').value
    res = `<div class = "card mb-1 p-2">
                <h3 class="card-title">${header}</h3>
                <p class="card-text">${note}</p>
                <p>${timestamp}</p>
            </div>`
    document.getElementById('written-notes').innerHTML = res + document.getElementById('written-notes').innerHTML
    document.getElementById('header').value = ""
    document.getElementById('note').value = ""
}

document.getElementById('submit').addEventListener("click", function(event){
    event.preventDefault()
    let form = new FormData(myForm)
    fetch("http://localhost:5000/save/note", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => console.log(data) )
    submit()
})