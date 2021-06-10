import * as timeMan from './timeManager.mjs';
export function showTime(){
    var clock = document.getElementById('clock');
    var time =timeMan.getTime();
    clock.textContent = time;
    setTimeout(showTime, 1000);
}
