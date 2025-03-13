document.addEventListener("DOMContentLoaded", function () {
    let isSoundOn = false;
    let soundBtn = document.getElementById("sound");
    let soundOnIcon = soundBtn.querySelector(".sound-on");
    let soundOffIcon = soundBtn.querySelector(".sound-off");
    let audio = new Audio("static/music/background.mp3");
    audio.loop = true; // Keeps looping the background music

    soundBtn.addEventListener("click", function () {
        isSoundOn = !isSoundOn;

        if (isSoundOn) {
            soundOnIcon.style.display = "block";
            soundOffIcon.style.display = "none";
            audio.play();
        } else {
            soundOnIcon.style.display = "none";
            soundOffIcon.style.display = "block";
            audio.pause();
        }
    });
});
