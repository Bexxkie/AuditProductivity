import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();

//slider:checkbox
var slider_map = {'slider-history':["tog-hist",'tog-hist-p'],
                  'slider-general':['tog-gen','tog-gen-p'],
                  'slider-audit':['tog-aud','tog-aud-p']};
// same as above, but for the toggleButtons
var btn_map = {'btn-theme':'tog-thme',
                  'btn-autolog':'tog-alo'};


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
 *
 * @param  {string} message printed message
 * @return {none}
 */
function updateHistory(message){
  var pan = document.getElementById('history-box');
  pan.textContent+=("["+timeMan.getTime()+"]"+message+"\n");
  //Keep most recent message displayed
  pan.scrollTop = pan.scrollHeight;
}


/**
 * togglePane - toggle display of panes
 *
 * @param  {string} pane window pane to update
 * @return {none}
 */
function togglePane(pane){
  updateHistory(pane);
  getElement(slider_map[pane][0]).checked = !getElement(slider_map[pane][0]).checked;
  getElement(slider_map[pane][1]).checked = !getElement(slider_map[pane][1]).checked;
}


/**
 * toggleButton - description
 *
 * @param  {string} button button name to update
 * @return {none}
 */
function toggleButton(button){
  updateHistory(btn_map[button]);
  getElement(btn_map[button]).checked = !getElement(btn_map[button]).checked;
}

/**
 * changeTheme - update the stylesheet being used.
 *
 * @return {none}
 */
function changeTheme(){
    var stylesheet = 'v2-style.css';
    if(getToggleState('btn-theme')){
      stylesheet = 'v2-style-light.css';
    }
    getElement('stylesheet').href = stylesheet;
}


//==============================================================================
//==============================================================================
//--------------------Getters---------------------------------------------------

/**
 * isToggled - check togglestate of a button
 *
 * @param  {str} btn button
 * @return {bool}    button state
 */
function getToggleState(btn){
  if(getElement(btn_map[btn]).checked){
    return(true);
  }
  return(false);
}
/**
 * getStyle - short for getComputedStyle....
 *
 * @param  {str} styleID css styleId
 * @return {obj}         style object
 */
function getStyle(styleID){
  return(getComputedStyle(document.documentElement).getPropertyValue(styleID));
}


/**
 * getElement - short for getElementById
 *
 * @param  {str} elementID  css elementId
 * @return {obj}            element object
 */
function getElement(elementID){
  return(document.getElementById(elementID));
}

//==============================================================================
//==============================================================================
//--------------------Event Handler(s?)---------------------------------------------
/**
 * clickEventHandler - setup clickEvents
 *
 * @return {none}
 */
function eventListeners(){
  getElement('win-btn-close').addEventListener("click", event => {
    win.close();
  });
  getElement('win-btn-minimize').addEventListener("click", event => {
    win.minimize();
  });
  getElement('slider-history').addEventListener("click", event => {
    togglePane("slider-history");
  });
  getElement('slider-general').addEventListener("click", event => {
    togglePane("slider-general");
  });
  getElement('slider-audit').addEventListener("click", event => {
    togglePane("slider-audit");
  });
  getElement('btn-autolog').addEventListener("click", event => {
    toggleButton('btn-autolog');
  });
  getElement('btn-theme').addEventListener("click", event => {
    toggleButton('btn-theme')
    changeTheme();
  });
}
