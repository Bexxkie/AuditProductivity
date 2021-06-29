import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';

var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();


  // for build uses MAIN.EXE
const relay = require('child_process').spawn('python',['./py/MAIN.py'] ,{stdio: 'pipe'});
//const relay = require("child_process").execFile("MAIN.exe");
// Backend testing here
function sendToRelay(msg){
  //relay.stdin.write(msg+'\n');
  relay.stdin.write(msg+'*'+getElement('footer-t-pass').value+'\n');
  //updateHistory(msg+'\n');
  }

// return calls from python
function interpret(msg){
  /* this is getting over-complicated, simplify..
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
  }*/

  //
  // So this function is basically the input for everything from 'relay'
  // We need to read the string and determine what it is
  // So set up a format to read
  // were going to need the following
  // text output for INFO (w or w/o timestamp)
  // control settings/adjustments (like i wanna toggle a button or something)
  // This is the stuff PY is asking/telling us
  // split msg by %
  // [0] [1] [2] [3]
  // @info%timestamp(bool)%String to print to historyPane(may contain spaces)
  // @ctrl%set/get(bool)%controlName

  msg = msg.split('%');
  if(msg[0] == '@info'){
    var print_string = msg[2];
    if(msg[1]){
      print_string = "["+timeMan.getTime()+"]"+msg[2];
    }
    updateHistory(print_string);
  }
  //@uvar%[0,1 set/get]%comName
  if(msg[0]=='@uvar'){
    setVariable(msg[2],msg[3])
    //if(msg[1]):

  }
}
// >>>>> upstream, TALK to  py
function writeCommand(cmdName){
  return('@comd%'+cmdName);
}
function writeToPy(varName,value){
  //getElement(varName).checked = +value
  return('@ctrl%1%'+varName+"%"+value);
}
function readVariable(varName){
  return("@ctrl%0%"+varName);
}

// <<<<<<<< downstream, LISTEN to python
// we should only really need to have python tell us to change a variable, for
// the KB interrupt signal
function setVariable(varName,value){
  if(varName == 'tog-alo'){
    getElement('tog-pass').checked = +value
  }
  getElement(varName).checked = +value
}


/* stuff is getting stupid so im gonna refactor
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
*/


//slider:checkbox
var slider_map = {'slider-history':["tog-hist",'tog-hist-p'],
                  'slider-general':['tog-gen','tog-gen-p'],
                  'slider-audit':['tog-aud','tog-aud-p']};
// same as above, but for the toggleButtons
var btn_map = {'btn-theme':'tog-thme',
                  'btn-autolog':'tog-alo'};
// stylesheets (cause i wanna just use +bool)
var stylesheets = ['styles/v2-style.css','styles/v2-style-light.css']
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
      var value = getElement(btn_map['btn-autolog']).checked
      getElement('tog-pass').checked = getElement(btn_map['btn-autolog']).checked
      sendToRelay(writeToPy('autoLog',+value));
      sendToRelay(writeCommand('set_auto_log'))
    }

  });
  getElement('btn-theme').addEventListener("click", event => {
    toggleElement('btn-theme',true);
    changeTheme();
  });
  getElement('btn-departures').addEventListener("click",event =>{
    sendToRelay(writeCommand('print_departures_list'))
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
