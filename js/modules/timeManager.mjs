export function getTime(){
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var t = h+":"+m+":"+s;
  return(t);
}
