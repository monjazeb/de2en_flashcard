const timerDisplay = document.getElementById("timer");

if (!localStorage.getItem("focusTime")){
  localStorage.setItem("focusTime", 25);
}
if (!localStorage.getItem("breakTime")){
  localStorage.setItem("breakTime", 5);
}
const workDuration = localStorage.getItem("focusTime")*60;
const breakDuration = localStorage.getItem("breakTime")*60;

const audio = document.querySelector("audio");

let isWorkTime = true;
let timeLeft = workDuration;
let timer = null;
let cycles = 0;

function updateCyclesDisplay (){
  document.getElementById('cycles').textContent = cycles;
}

function updateTimerDisplay(){
  const minutes = String(Math.floor(timeLeft/60)).padStart(2,"0");
  const seconds = String(timeLeft % 60).padStart(2,"0");

  timerDisplay.textContent = `${minutes}:${seconds}`;
}

function startTimer() {
  timer = setInterval(() =>{
    if (timeLeft>0){
      timeLeft--;
      updateTimerDisplay();
    } else {
      stopTimer();
      toggleStatus();
    updateTimerDisplay();
    startTimer();
    }
  }, 1000);
}

function stopTimer(){
  clearInterval(timer);
  timer = null;
}

function resetTimer(){
  stopTimer();
  timeLeft = workDuration;
  cycles = 0;
  updateTimerDisplay();
}

function toggleStatus(){
  isWorkTime = !isWorkTime;
  timeLeft = isWorkTime ? workDuration : breakDuration;
  document.getElementById('status').textContent = isWorkTime ? "Focus Time":"Break Time";
  document.getElementById('timer').style.color = isWorkTime ? "":"green";
  audio.play();
  if(isWorkTime) {
    cycles +=1;
    updateCyclesDisplay();
  }
}

document.getElementById("startBtn").addEventListener('click', () =>{
  startTimer();
});
document.getElementById("resetBtn").addEventListener('click', () =>{
  resetTimer();
});
document.getElementById("pauseBtn").addEventListener('click', () =>{
  stopTimer();
});

updateTimerDisplay();
updateCyclesDisplay();

function confirm_delete(card_id){
  let c = confirm("Are you sure you want to delete this flashcard?");
  if (c){ 
    window.location.href = `/delete/${card_id}`;
  }
}
document.getElementById("home").addEventListener('click', () =>{
  window.location.href = '/';
});