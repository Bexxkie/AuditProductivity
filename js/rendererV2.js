import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();

// panes to iter through for updating display
var pane_map = {'history_pane':["page-history","slider-history"],
                  'general_pane':["page-general-controls","slider-general"],
                  'audit_pane':["page-audit-controls","slider-audit"]};
// same as above, but for the toggleButtons
var btn_map = {'btn-theme':false,
                  'btn-autolog':false};


// done laoding event
document.onreadystatechange = (event) => {
    if (document.readyState == "complete") {
        updateState();
        clickEventHandler();
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
 * updateState - ensures interface is shown properly
 *
 * @return {none}
 */
function updateState(){
  var values = [['40px','transparent'],
                getStyle('--forecolor')];
  for(var pane in pane_map){
    if(document.getElementById(pane_map[pane][0]).style.display!='none'){
        values = [['70px',getStyle('--font-color')],
                       getStyle('--highlitecolor')];
      }
    updateSlider(pane_map[pane][1],values);
  }
  for(var button in btn_map){
    toggleButton(button,true);
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
  getElement(slider).style.color=state[0][1];
  getElement(slider).style.width=state[0][0];
  getElement(slider).style.background=state[1];
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
  var displayStyle = "block";
  if(getElement(pane).style.display != 'none'){
    displayStyle = "none";
  }
  getElement(pane).style.display = displayStyle;

  updateState();
}


/**
 * toggleButton - description
 *
 * @param  {string} button button name to update
 * @return {none}
 */
function toggleButton(button,refresh=false){
  updateHistory(button +"-re="+ refresh);
  var style = '--forecolor';
  //Toggle button state, if refreshing the style this is skipped
  if(refresh==false){
    btn_map[button] = !btn_map[button];
  }
  // setappropriate style to buttons
  if(getToggleState(button)){
      style = '--highlitecolor';
  }
  getElement(button).style.background = getStyle(style);
}


/**
 * changeTheme - update the CSS sheet being used.
 *
 * @return {bool}  completion state
 */
function changeTheme(){
  var stylesheet = 'v2-style.css';
  if(getToggleState('btn-theme')){
    stylesheet = 'v2-style-light.css';
  }
  getElement('stylesheet').href = stylesheet;
  return(true);
  //toggleButton('btn-autolog', true);
  //toggleButton('btn-theme', true);
}


//==============================================================================
//==============================================================================
//--------------------Getters---------------------------------------------------

/**
 * isToggled - check togglestate of a button
 *
 * @param  {str} btn button
 * @return {bool}     state of button
 */
function getToggleState(btn){
  updateHistory(btn+"=="+btn_map[btn]);
  if(btn_map[btn]){
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
//--------------------Event Handler---------------------------------------------
/**
 * clickEventHandler - setup clickEvents
 *
 * @return {none}
 */
function clickEventHandler(){
  getElement('win-btn-close').addEventListener("click", event => {
    win.close();
  });
  getElement('win-btn-minimize').addEventListener("click", event => {
    win.minimize();
  });
  getElement('slider-history').addEventListener("click", event => {
    togglePane("page-history");
  });
  getElement('slider-general').addEventListener("click", event => {
    togglePane("page-general-controls");
  });
  getElement('slider-audit').addEventListener("click", event => {
    togglePane("page-audit-controls");
  });
  getElement('btn-autolog').addEventListener("click", event => {
    toggleButton('btn-autolog');
  });
  getElement('btn-theme').addEventListener("click", event => {
    toggleButton('btn-theme');
    if(changeTheme()){
      updateState();
    }
  });
}
