import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { app } from 'electron';

export const DESKTOP_API_PORT = '18765';

export function getApiUrl(): string {
	return `http://127.0.0.1:${DESKTOP_API_PORT}`;
}

export function getUserDataDir(): string {
	return path.join(app.getPath('appData'), 'Retriever');
}

export function getChromaDir(): string {
	return path.join(getUserDataDir(), 'chroma_data');
}

export function getTmpUploadDir(): string {
	return path.join(getUserDataDir(), 'tmp_uploads');
}

/** Dev: sibling retriever-api. Prod: bundled under resources/api. */
export function resolveApiRoot(): string {
	if (app.isPackaged) {
		return path.join(process.resourcesPath, 'api');
	}
	const webRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
	return path.resolve(webRoot, '..', 'retriever-api');
}

export function resolveApiExecutable(): string {
	if (app.isPackaged) {
		return path.join(process.resourcesPath, 'api', 'retriever-api.exe');
	}
	return '';
}

export function resolvePythonExecutable(apiRoot: string): string {
	return path.join(apiRoot, '.venv', 'Scripts', 'python.exe');
}

export function resolveWebBuildDir(): string {
	if (app.isPackaged) {
		return path.join(app.getAppPath(), 'build');
	}
	return '';
}

export function resolveDevServerUrl(): string {
	return process.env.VITE_DEV_SERVER_URL ?? 'http://localhost:5173';
}
