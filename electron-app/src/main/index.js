import { app, shell, BrowserWindow, ipcMain, Tray, Menu } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { exec } from 'child_process'
import path from 'path'

let mainWindow = null
let tray = null

function fetchVisaData(mainWindow) {
  const pythonScript = path.join(__dirname, '../../../main.py')

  exec(`python "${pythonScript}"`, { env: { ...process.env, PYTHONIOENCODING: 'utf-8' } }, (error, stdout, stderr) => {
    if (error) {
      console.error(`Python execution error: ${error}`) //Returns python execution error
      return
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`)
    }

    try {
      const frontendData = JSON.parse(stdout) //Attempts to get JSON
      console.log('Received Visa Data:', frontendData)
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('visa-data-update', frontendData) // Sends it to the front end
      }
    } catch (parseError) {
      console.error('Failed to parse JSON from python script:', parseError, stdout)
    }
  })
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    icon,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  }) // Creates a 900 x 670 window

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault()
      mainWindow.hide() // Runs in BG
    }
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.electron')

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  createWindow()

  fetchVisaData(mainWindow)

  tray = new Tray(icon) //  Exits  to tray
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show App', click: () => mainWindow.show() },
    {
      label: 'Quit',
      click: () => {
        app.isQuitting = true
        app.quit()
      }}


  ])

  tray.setToolTip('Background App')
  tray.setContextMenu(contextMenu)

  tray.on('click', () => {
    mainWindow.show()
  })

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {

  }
})
