export function getTime(){
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  if(h < 10){
    h='0'+h;
  }
  if(m < 10){
    m='0'+m;
  }
  if(s < 10){
    s='0'+s;
  }
  var t = h+":"+m+":"+s;
  return(t);
}
