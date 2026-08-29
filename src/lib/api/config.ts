const TAURI_DESKTOP_API_PORT = '18765';

function isTauriDesktop(): boolean {
	return typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window;
}

export function getApiBaseUrl(): string {
	if (isTauriDesktop()) {
		return `http://127.0.0.1:${TAURI_DESKTOP_API_PORT}`;
	}
	return import.meta.env.PUBLIC_API_URL ?? 'http://127.0.0.1:8000';
}
