import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();
const { spawn } = require('child_process');


const relay = spawn('python',['./py/listener.py'] ,{
    stdio: 'pipe'
});
// Backend testing here
function sendToRelay(msg){
  relay.stdin.write(msg+'*'+getElement('footer-t-pass').value+'\n');
  }
// return calls from python
function interpret(msg){
  var content = msg.split('<<');
  updateHistory(content[1])
  switch(content[0]){
    case '@req':
      // request updates, py wants to know something
      //updateHistory(msg);
      break;
    case '@inf':
      // print output, standard just print stuff. info
      updateHistory(content[1]);
      break;
    case '@tim':
      updateHistory("["+timeMan.getTime()+"]"+content[1]);
      break;
    case '@psh':
      // push updates, py did something we need to know
      // @psh<<objName%value
      recieveData(content[1])
      break
    default:
      updateHistory(msg);
  }
}
function recieveData(data){
  data = data.split('%')
  updateHistory(data[0])
  getElement(btn_map[data[0]]).checked = +data[1]

}
function sendCommand(comName){
  return('@com>>'+comName)
}


function updateVar(varName){
  switch(varName){
    case 'autoLog':
      // @inf>>autoLog%'BOOL'
      return('@set>>autoLog%'+(+getElement(btn_map['btn-autolog']).checked))
      break
    case 'threadStop':
      break
    case 'delay':
      break
  }
}


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
 * story - sends messages to history_pane
 * @param  {string} message printed message
 */
function updateHistory(message){
  var pan = getElement('history-box');
  pan.textContent+=(message);
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

      if(el !='slider-history' && getElement(slider_map[el][0]).checked){
          getElement('tog-fot-p').checked = true;
          return true;
        }
      }
    getElement('tog-fot-p').checked = false;
    return true;
  }
  getElement(btn_map[element]).checked = !getElement(btn_map[element]).checked;
  return true;
}

function changeTheme(){
    getElement('stylesheet').href = stylesheets[+(getElement('tog-thme').checked)];
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
    relay.kill();
    win.close();
  });
  getElement('win-btn-minimize').addEventListener("click", event => {
    win.minimize();
  });
  getElement('slider-history').addEventListener("click", event => {
    toggleElement("slider-history");
  });
  getElement('slider-general').addEventListener("click", event => {
    toggleElement("slider-general");
  });
  getElement('slider-audit').addEventListener("click", event => {
    toggleElement("slider-audit");
  });
  getElement('btn-autolog').addEventListener("click", event => {
    if(toggleElement('btn-autolog',true)){
      sendToRelay(updateVar('autoLog'));
      sendToRelay(sendCommand('btn-autolog'))
    }

  });
  getElement('btn-theme').addEventListener("click", event => {
    toggleElement('btn-theme',true);
    changeTheme();
  });
  relay.stdout.on('data', function(data)
  {
    interpret(data.toString());
    //updateHistory(data.toString());
  });
  relay.stderr.on('data', function(data)
  {
    updateHistory(data.toString())
  });
  relay.on('close', function(close)
  {
    updateHistory("err"+close.toString());
  });



}

//------------------------------------------------------------------------------
