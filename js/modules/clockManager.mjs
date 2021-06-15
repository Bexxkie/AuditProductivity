import * as timeMan from './timeManager.mjs';
export function showTime(){
    var clock = document.getElementById('footer-clock');
    var time =timeMan.getTime();
    clock.textContent = timeMan.getTime();
    setTimeout(showTime, 1000);
}
