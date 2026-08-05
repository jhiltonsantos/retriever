import { contextBridge, ipcRenderer } from 'electron';

const DESKTOP_API_PORT = '18765';

contextBridge.exposeInMainWorld('retriever', {
	getApiUrl: () => `http://127.0.0.1:${DESKTOP_API_PORT}`,
	checkOllama: () => ipcRenderer.invoke('ollama:check'),
	isDesktop: true
});
