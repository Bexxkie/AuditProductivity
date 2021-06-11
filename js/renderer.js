import * as timeMan from './modules/timeManager.mjs';
import * as clockMan from './modules/clockManager.mjs';
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();
document.onreadystatechange = (event) => {
    if (document.readyState == "complete") {
        checkState();
        handleWindowControls();
        clockMan.showTime();
    }
};
var btnOpn = ['70px',0];
var btnCls = ['40px','transparent'];
//import theming
// - dark
var colorDarkFont = getComputedStyle(document.documentElement).getPropertyValue('--col-dark-font');
var colorDark = getComputedStyle(document.documentElement).getPropertyValue('--col-dark');
var colorDark1 = getComputedStyle(document.documentElement).getPropertyValue('--col-dark-a');
var colorDark2 = getComputedStyle(document.documentElement).getPropertyValue('--col-dark-b');
// - light
var colorLightFont = getComputedStyle(document.documentElement).getPropertyValue('--col-light-font');
var colorLight = getComputedStyle(document.documentElement).getPropertyValue('--col-light');
var colorLight1 = getComputedStyle(document.documentElement).getPropertyValue('--col-light-a');
var colorLight2 = getComputedStyle(document.documentElement).getPropertyValue('--col-light-b');
// - universal
var colorBlurpleLight = getComputedStyle(document.documentElement).getPropertyValue('--col-blurple-l');
var colorConsoleLight = getComputedStyle(document.documentElement).getPropertyValue('--col-console-l');
var colorBlurple = getComputedStyle(document.documentElement).getPropertyValue('--col-blurple-d');
var colorConsole = getComputedStyle(document.documentElement).getPropertyValue('--col-console');
// setup theming support

let themeMap = new Map();
themeMap.set("dark", [colorDarkFont,colorDark,colorDark1,colorDark2,colorBlurple,colorConsole]);
themeMap.set("light", [colorLightFont,colorLight,colorLight1,colorLight2,colorBlurpleLight,colorConsoleLight]);
// themeMap.get(str)[int] 0=font 1=background 2=inactive/titlebar 3=hover/active
let toggleMap = new Map();
toggleMap.set("log_toggle",false);
toggleMap.set("mod_toggle",false);
window.onbeforeunload=(event)=>{
  win.removeAllListeners();
}

//ensures ui is rendered right,
// -buttons locked when they should be and stuff
function checkState(){
    if(document.getElementById("auditFunctions").style.display != 'none'){
      updateElement("btn_aud",btnOpn,getThemeColor(4));
    }else{
      updateElement("btn_aud",btnCls,getThemeColor(2));
    }
    if(document.getElementById("historyPane").style.display != 'none'){
      updateElement("btn_hst",btnOpn,getThemeColor(4));
    }else{
        updateElement("btn_hst",btnCls,getThemeColor(2));
    }
    if(document.getElementById("generalFunctions").style.display != 'none'){
      updateElement("btn_gen",btnOpn,getThemeColor(4));
    }else{
      updateElement("btn_gen",btnCls,getThemeColor(2));
    }
    if(toggleMap.get("mod_toggle")){
      document.getElementById("mod_toggle").style.background = getThemeColor(4);
    }else{
      document.getElementById("mod_toggle").style.background = getThemeColor(2);
    }
    if(toggleMap.get("log_toggle")){
      document.getElementById("log_toggle").style.background = getThemeColor(4);
    }else{
      document.getElementById("log_toggle").style.background = getThemeColor(2);
    }
  changeTheme();
}
//
//used for updating button styles, for switches and stuff.
function updateElement(str,val,col){
  document.getElementById(str).style.width = val[0];
  if(val[1]=='transparent'){
      document.getElementById(str).style.color = val[1];
  }
  else{
    document.getElementById(str).style.color = getThemeColor(val[1]);
  }
  document.getElementById(str).style.background = col
}
//
// add listeners to buttonpress events
function handleWindowControls(){
  //Window buttons
  document.getElementById('btn_min').addEventListener("click", event => {
    myConsole.log("min");
    win.minimize();
  });
  document.getElementById('btn_cls').addEventListener("click", event => {
    myConsole.log("close");
    win.close();
  });
  // Menu buttons
  document.getElementById('btn_hst').addEventListener("click", event => {
    toggleElement('historyPane');
  });
  document.getElementById('btn_gen').addEventListener("click", event => {
    toggleElement('generalFunctions');
  });
  document.getElementById('btn_aud').addEventListener("click", event => {
    toggleElement('auditFunctions');
  });
  document.getElementById('log_toggle').addEventListener("click", event => {
    toggleElement('log_toggle',false);
  });
  document.getElementById('mod_toggle').addEventListener("click", event => {
    toggleElement('mod_toggle',false);
  });
}
//changesthe css values
function changeTheme(){
 document.documentElement.style.setProperty('--col-dark-font', getThemeColor(0));
 document.documentElement.style.setProperty('--col-dark', getThemeColor(1));
 document.documentElement.style.setProperty('--col-dark-a', getThemeColor(2));
 document.documentElement.style.setProperty('--col-dark-b', getThemeColor(3));
 document.documentElement.style.setProperty('--col-blurple-d', getThemeColor(4));
 document.documentElement.style.setProperty('--col-console', getThemeColor(5));

}
/**
@param int  0=font 1=background 2=inactive/titlebar 3=hover/active 4=blurple 5=console
**/
function getThemeColor(int){ //pass 0-3
  if(toggleMap.get("mod_toggle")){   //lightModeActive
    return(themeMap.get("light")[int]);
  }
  else{
    return(themeMap.get("dark")[int])
  }
}
//general functions -autolog
function toggleElement(str,b=true){
  var val = "";
  if(b==false){
      toggleMap.set(str,!toggleMap.get(str));
      if(toggleMap.get(str)){
        document.getElementById(str).style.background = colorBlurple;
    }else{
      document.getElementById(str).style.background = getThemeColor(1);
    }
    //updateHistory(str +' '+ toggleMap.get(str));
    //return;
  }
  else if(document.getElementById(str).style.display == 'none'){
    document.getElementById(str).style.display = 'block';
    val="show";
    }
  else{
    document.getElementById(str).style.display = 'none';
    val="hide";
    }
  myConsole.log(val+str);
  checkState();
  }
// writes to historypane, autoscrolls to newest line
function updateHistory(str){
  var pan = document.getElementById('history_box');
  pan.textContent+=(timeMan.getTime()+"] "+str+"\n[");
  pan.scrollTop = pan.scrollHeight;
  }
