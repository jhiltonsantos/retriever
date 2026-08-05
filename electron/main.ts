import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { app, BrowserWindow, ipcMain } from 'electron';
import type { ChildProcess } from 'node:child_process';
import { checkOllama, startApiProcess, stopApiProcess } from './api-manager.js';
import { getApiUrl, resolveDevServerUrl, resolveWebBuildDir } from './paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let mainWindow: BrowserWindow | null = null;
let apiProcess: ChildProcess | null = null;
let isQuitting = false;

async function createWindow(): Promise<void> {
	mainWindow = new BrowserWindow({
		width: 1100,
		height: 800,
		minWidth: 720,
		minHeight: 600,
		title: 'Retriever',
		webPreferences: {
			preload: path.join(__dirname, 'preload.cjs'),
			contextIsolation: true,
			nodeIntegration: false,
			sandbox: false
		}
	});

	if (app.isPackaged) {
		const indexHtml = path.join(resolveWebBuildDir(), 'index.html');
		await mainWindow.loadFile(indexHtml);
	} else {
		await mainWindow.loadURL(resolveDevServerUrl());
	}

	mainWindow.on('closed', () => {
		mainWindow = null;
	});
}

app.whenReady().then(async () => {
	ipcMain.handle('ollama:check', () => checkOllama());

	try {
		apiProcess = await startApiProcess();
	} catch (error) {
		console.error('Falha ao iniciar API:', error);
	}

	await createWindow();

	app.on('activate', async () => {
		if (BrowserWindow.getAllWindows().length === 0) {
			await createWindow();
		}
	});
});

app.on('before-quit', () => {
	isQuitting = true;
	stopApiProcess(apiProcess);
	apiProcess = null;
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

process.on('exit', () => {
	if (!isQuitting) {
		stopApiProcess(apiProcess);
	}
});

console.log('Retriever API:', getApiUrl());
