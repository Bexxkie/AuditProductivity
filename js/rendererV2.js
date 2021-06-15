import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();

// panes to be itered through, insert into update_map
var history_pane = ["page-history","slider-history"];
var general_pane = ["page-general-controls","slider-general"];
var audit_pane = ["page-audit-controls","slider-audit"];

// panes to iter through for updating display
var update_map = {'history_pane':history_pane,'general_pane':general_pane,'audit_pane':audit_pane};

var toggle_map = {'btn-theme':false,'btn-autolog':false};


document.onreadystatechange = (event) => {
    if (document.readyState == "complete") {
        updateState();
        clickEventHandler();
        clockMan.showTime();
    }
};

window.onbeforeunload=(event)=>{
  win.removeAllListeners();
}
/**
 * updateState - ensures interface is shown properly
 *
 * @return {none}
 */
function updateState(){
  var values = [];
  for(var pane in update_map){
    if(document.getElementById(update_map[pane][0]).style.display!='none'){
      values = [['70px',getComputedStyle(document.documentElement).getPropertyValue('--font-color')],getComputedStyle(document.documentElement).getPropertyValue('--highlitecolor')];
    }else{
      values = [['40px','transparent'],getComputedStyle(document.documentElement).getPropertyValue('--forecolor')];
    }
    updateSlider(update_map[pane][1],values);
  }
}

/**
 * updateSlider - updates sliders to reflect open/close state
 *
 * @param  {string} slider slider name
 * @param  {array}  state  [width,color]
 * @return {none}
 */
function updateSlider(slider,state){
  document.getElementById(slider).style.color=state[0][1];
  document.getElementById(slider).style.width=state[0][0];
  document.getElementById(slider).style.background=state[1];
}
/**
 * updateHistory - sends messages to history_pane
 *
 * @param  {string} message printed message
 * @return {none}
 */
function updateHistory(message){
  var pan = document.getElementById('history-box');
  pan.textContent+=("["+timeMan.getTime()+"]"+message+"\n");
  pan.scrollTop = pan.scrollHeight;
}

/**
 * togglePane - toggle display of panes
 *
 * @param  {string} pane window pane to update
 * @return {none}
 */
function togglePane(pane){
  if(document.getElementById(pane).style.display != 'none'){
    document.getElementById(pane).style.display = "none";
  }
  else{document.getElementById(pane).style.display = "block";}
  updateState();
}

/**
 * toggleButton - description
 *
 * @param  {string} button button name to update
 * @return {none}
 */
function toggleButton(button,refresh=false){
  if(refresh==false){
    toggle_map[button] = !toggle_map[button];
  }
    if(toggle_map[button]==true){
      document.getElementById(button).style.background = getComputedStyle(document.documentElement).getPropertyValue('--highlitecolor');
  }else{
    document.getElementById(button).style.background = getComputedStyle(document.documentElement).getPropertyValue('--forecolor');
  }
}
function changeTheme(stylesheet){
  document.getElementById('stylesheet').href = stylesheet;
  updateState();
  toggleButton('btn-autolog', true);
  toggleButton('btn-theme', true);
}
/**
 * clickEventHandler - setup clickEvents
 *
 * @return {none}
 */
function clickEventHandler(){
  document.getElementById('win-btn-close').addEventListener("click", event => {
    win.close();
  });
  document.getElementById('win-btn-minimize').addEventListener("click", event => {
    win.minimize();
  });
  document.getElementById('slider-history').addEventListener("click", event => {
    togglePane("page-history");
  });
  document.getElementById('slider-general').addEventListener("click", event => {
    togglePane("page-general-controls");
  });
  document.getElementById('slider-audit').addEventListener("click", event => {
    togglePane("page-audit-controls");
  });

  document.getElementById('btn-autolog').addEventListener("click", event => {
    toggleButton('btn-autolog');
  });
  document.getElementById('btn-theme').addEventListener("click", event => {
    toggleButton('btn-theme');
    if(toggle_map['btn-theme']){
      //true - set to light
      changeTheme("v2-style-light.css");
      changeTheme("v2-style-light.css");
    }else{
      changeTheme("v2-style.css");
      changeTheme("v2-style.css");
    }

  });
}
