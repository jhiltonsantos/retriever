// O webview do Tauri ignora `target="_blank"`; no desktop o link precisa passar pelo plugin shell.
export function openExternal(url: string): void {
	if (typeof window === 'undefined') return;
	const tauri = (window as unknown as {
		__TAURI_INTERNALS__?: { invoke: (cmd: string, args: object) => Promise<unknown> };
	}).__TAURI_INTERNALS__;
	if (tauri) {
		tauri.invoke('plugin:shell|open', { path: url }).catch((err) => {
			console.warn('Não foi possível abrir o link externo', err);
		});
		return;
	}
	window.open(url, '_blank', 'noopener,noreferrer');
}

export function externalLinkHandler(url: string) {
	return (event: MouseEvent) => {
		event.preventDefault();
		openExternal(url);
	};
}
