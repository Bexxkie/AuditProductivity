var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const remote = require('electron').remote;
const win = remote.getCurrentWindow();
document.onreadystatechange = (event) => {
    if (document.readyState == "complete") {
        checkState();
        handleWindowControls();
    }
};
var btnOpn = ['70px','white'];
var btnCls = ['40px','transparent'];
var c1 = getComputedStyle(document.documentElement).getPropertyValue('--col-dark-a');
var c2 = getComputedStyle(document.documentElement).getPropertyValue('--col-dark-b');
var c3 = getComputedStyle(document.documentElement).getPropertyValue('--col-blurple-d');
var autoLogToggleActive = false;
window.onbeforeunload=(event)=>{
  win.removeAllListeners();
}

function checkState(){
    if(document.getElementById("auditFunctions").style.display != 'none'){
      updateElement("btn_aud",btnOpn,c3);
    }else{
      updateElement("btn_aud",btnCls,c1);
    }
    if(document.getElementById("historyPane").style.display != 'none'){
      updateElement("btn_hst",btnOpn,c3);
    }else{
        updateElement("btn_hst",btnCls,c1);
    }
    if(document.getElementById("generalFunctions").style.display != 'none'){
      updateElement("btn_gen",btnOpn,c3);
    }else{
      updateElement("btn_gen",btnCls,c1);
    }
}
function updateElement(str,val,col){
  document.getElementById(str).style.width = val[0];
  document.getElementById(str).style.color = val[1];
  document.getElementById(str).style.background = col
}


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
}

function toggleButton(){

}

//general functions -autolog
function toggleElement(str,b=true){
  var val = "";
  if(b==false){
      autoLogToggleActive= !autoLogToggleActive;
      if(autoLogToggleActive){
      document.getElementById(str).style.background = c3;
    }else{
      document.getElementById(str).style.background = c1;
    }
    updateHistory('log_toggle: '+ autoLogToggleActive);
    return;
  }
  if(document.getElementById(str).style.display == 'none'){
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

function getTime(){
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var t = h+":"+m+":"+s;
  return(t+"]");
}

function updateHistory(str){
  var pan = document.getElementById('history_box');
  pan.textContent+=(getTime()+" "+str+"\n[");
  pan.scrollTop = pan.scrollHeight;
  }
