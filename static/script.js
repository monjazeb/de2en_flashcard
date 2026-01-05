const timerDisplay = document.getElementById("timer");

const WORK_MINUTES = 0.2;
const BREAK_MINUTES = 0.1;
const workDuration = WORK_MINUTES*60;
const breakDuration = BREAK_MINUTES*60;

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
  pauseTimer();
});

updateTimerDisplay();
updateCyclesDisplay();