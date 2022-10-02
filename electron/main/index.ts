// The built directory structure
//
// ├─┬ dist
// │ ├─┬ electron
// │ │ ├─┬ main
// │ │ │ └── index.js
// │ │ └─┬ preload
// │ │   └── index.js
// │ ├── index.html
// │ ├── ...other-static-files-from-public
// │
process.env.DIST = join(__dirname, "../..");
process.env.PUBLIC = app.isPackaged
  ? process.env.DIST
  : join(process.env.DIST, "../public");
const PYPATH = app.isPackaged
  ? process.env.DIST
  : join(process.env.DIST, "../py");

import { app, BrowserWindow, shell, ipcMain, session } from "electron";
import { release } from "os";
import { join } from "path";

// Disable GPU Acceleration for Windows 7
if (release().startsWith("6.1")) app.disableHardwareAcceleration();

// Set application name for Windows 10+ notifications
if (process.platform === "win32") app.setAppUserModelId(app.getName());

if (!app.requestSingleInstanceLock()) {
  app.quit();
  process.exit(0);
}

// Remove electron security warnings
// This warning only shows in development mode
// Read more on https://www.electronjs.org/docs/latest/tutorial/security
// process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'

/*************************************************************
 * py process
 *************************************************************/

const PY_MODULE = "main"; // without .py suffix

let pyProc = null;
let pyPort = null;

const getScriptPath = () => {
  if (!app.isPackaged) {
    console.log("not packaged");
    return join(PYPATH, PY_MODULE + ".py");
  }
  if (process.platform === "win32") {
    console.log(process.platform);
    return join(PYPATH, PY_MODULE + ".exe");
  }
  // TODO, for MAC and LINUX, do something else?
  console.log(process.platform);
  // return join(PYPATH, PY_MODULE + ".exe");
};

const selectPort = () => {
  pyPort = 4242;
  return pyPort;
};

const createPyProc = () => {
  let script = getScriptPath();
  let port = "" + selectPort();

  if (app.isPackaged) {
    // disable calling pyProc in packaged app, run separately
    // pyProc = require("child_process").execFile(script, [port]);
    console.log("current setup: separate python server start up");
    console.log(
      "Please ensure server is running by going to http://127.0.0.1:4242/"
    );
    pyProc = null;
  } else {
    pyProc = require("child_process").spawn("python", [script, "-p", port]);
  }

  if (pyProc != null) {
    //console.log(pyProc)
    console.log("child process forced on port " + port);
    console.log("port: " + port + ", script: " + script);
  } else {
    console.log(" ");
    // console.log("port: " + port + ", script: " + script);
  }
};

process.on("unhandledRejection", (error) => {
  console.error(error);
});

/*************************************************************
 * window management
 *************************************************************/
let win: BrowserWindow | null = null;
// const pyHandler = new PyHandler();

// Here, you can also use other preload
const preload = join(__dirname, "../preload/index.js");
const url = process.env.VITE_DEV_SERVER_URL as string;

const indexHtml = join(process.env.DIST, "index.html");

async function createWindow() {
  win = new BrowserWindow({
    title: "Main window",
    icon: join(process.env.PUBLIC, "favicon.ico"),
    webPreferences: {
      preload,
      // Warning: Enable nodeIntegration and disable contextIsolation is not secure in production
      // Consider using contextBridge.exposeInMainWorld
      // Read more on https://www.electronjs.org/docs/latest/tutorial/context-isolation
      nodeIntegration: true,
      contextIsolation: false,
    },
    minWidth: 780,
    show: false, // along with win.maximize() and win.show() ensure screen is maximized before being shown.
  });

  // ensure screen is maximized before being shown.
  win.maximize();
  win.show();

  if (app.isPackaged) {
    win.loadFile(indexHtml);
  } else {
    win.loadURL(url);
    // Open devTool if the app is not packaged
    win.webContents.openDevTools();
  }

  // Test actively push message to the Electron-Renderer
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  // Make all links open with the browser, not with the application
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https:") || url.startsWith("http:"))
      shell.openExternal(url);

    return { action: "deny" };
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  win = null;
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("second-instance", () => {
  if (win) {
    // Focus on the main window if the user tried to open another
    if (win.isMinimized()) win.restore();
    win.focus();
  }
});

app.on("activate", () => {
  const allWindows = BrowserWindow.getAllWindows();
  if (allWindows.length) {
    allWindows[0].focus();
  } else {
    createWindow();
  }
});

// this might not be enough when app is being packaged.
const exitPyProc = () => {
  if (pyProc) {
    pyProc.kill();
    pyProc = null;
    pyPort = null;
  }
};

app.on("ready", createPyProc);
app.on("will-quit", exitPyProc);

// new window example arg: new windows url
ipcMain.handle("open-win", (event, arg) => {
  const childWindow = new BrowserWindow({
    webPreferences: {
      preload,
    },
  });

  if (app.isPackaged) {
    childWindow.loadFile(indexHtml, { hash: arg });
  } else {
    childWindow.loadURL(`${url}/#${arg}`);
    // childWindow.webContents.openDevTools({ mode: "undocked", activate: true })
  }
});
