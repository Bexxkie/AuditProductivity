// okay so how do i use jscript..
const {app, BrowserWindow} = require('electron')
var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
// creates the window, with defaults
function createWindow()
{
  const mainWindow = new BrowserWindow(
    {
    minWidth: 400,
    minHeight: 500,
    maxWidth: 400,
    maxHeight: 500,
    width:400,
    height:500,
    frame: false,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        enableRemoteModule: true
    }
  })
  mainWindow.webContents.openDevTools();

  /*
    So im going to use a tab system, which will be handled in the HTML/css i think
    I would /like/ multiple windows but i havent figured that out yet
  */
  // what should be displayed
  mainWindow.loadFile('v2.html')

  //historyWindow.loadFile('historyPane.html')
  // ctrl+r to reload app

}

// after (electron?) is loaded go ahead and actually show what i want.
app.whenReady().then(() => {
  createWindow();
  myConsole.log("ready");
//for macOS, preocesses remain open in mOS unless cmd+Q
  app.on('activate', function () {
   if (BrowserWindow.getAllWindows().length === 0) createWindow()
 })

})

// when the window is closed, end the process.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})
