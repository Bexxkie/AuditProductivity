import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();
const { spawn } = require('child_process');

const relay = spawn('python',['./py/test.py']);


//slider:checkbox
var slider_map = {'slider-history':["tog-hist",'tog-hist-p'],
                  'slider-general':['tog-gen','tog-gen-p'],
                  'slider-audit':['tog-aud','tog-aud-p']};
// same as above, but for the toggleButtons
var btn_map = {'btn-theme':'tog-thme',
                  'btn-autolog':'tog-alo'};
// stylesheets (cause i wanna just use +bool)
var stylesheets = ['v2-style.css','v2-style-light.css']
// done laoding event
document.onreadystatechange = (event) => {
    if (document.readyState == "complete") {
        eventListeners();
        clockMan.showTime();
    }
};
// preload event
window.onbeforeunload = (event) => {
  win.removeAllListeners();
};


//==============================================================================
//==============================================================================
//--------------------Setters---------------------------------------------------
/**
 * updateHistory - sends messages to history_pane
 * @param  {string} message printed message
 */
function updateHistory(message){
  var pan = getElement('history-box');
  pan.textContent+=("["+timeMan.getTime()+"]"+message+"\n");
  //Keep most recent message displayed
  pan.scrollTop = pan.scrollHeight;
}

/**
 * toggleElement - description
 * @param  {str} element      element being updated
 * @param  {bool} button=false true for toggleButton
 */
function toggleElement(element,button=false){
  if(!button){
    getElement(slider_map[element][0]).checked = !getElement(slider_map[element][0]).checked;
    getElement(slider_map[element][1]).checked = !getElement(slider_map[element][1]).checked;

    for(var el in slider_map){
      if(getElement(slider_map[el][0]).checked){
          getElement('tog-fot-p').checked = true;
          return;
        }
      }
    getElement('tog-fot-p').checked = false;
    return;
  }
  getElement(btn_map[element]).checked = !getElement(btn_map[element]).checked;
}

function changeTheme(){
    getElement('stylesheet').href = stylesheets[+(getElement('tog-thme').checked)];
}
function sendToRelay(msg){
  relay.stdin.write(msg);
  relay.stdin.end();
}
//==============================================================================
//==============================================================================
//--------------------Getters---------------------------------------------------
function getStyle(styleID){
  return(getComputedStyle(document.documentElement).getPropertyValue(styleID));
}
function getElement(elementID){
  return(document.getElementById(elementID));
}
//==============================================================================
//==============================================================================
//--------------------Event Handler---------------------------------------------
function eventListeners(){
  getElement('win-btn-close').addEventListener("click", event => {
    win.close();
  });
  getElement('win-btn-minimize').addEventListener("click", event => {
    win.minimize();
  });
  getElement('slider-history').addEventListener("click", event => {
    toggleElement("slider-history");
    sendToRelay('slider-history');
  });
  getElement('slider-general').addEventListener("click", event => {
    toggleElement("slider-general");
    sendToRelay('slider-general');
  });
  getElement('slider-audit').addEventListener("click", event => {
    toggleElement("slider-audit");
    sendToRelay('slider-audit');
  });
  getElement('btn-autolog').addEventListener("click", event => {
    toggleElement('btn-autolog',true);
    sendToRelay('btn-autolog');
  });
  getElement('btn-theme').addEventListener("click", event => {
    toggleElement('btn-theme',true);
    sendToRelay('btn-theme');
    changeTheme();
  });
  relay.stdout.on('data', function(data)
  {
    updateHistory(data)
  });

}

//------------------------------------------------------------------------------
