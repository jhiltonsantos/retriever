import { getEmbeddingsStatus } from '$lib/api/embeddings';
import type { EmbeddingsStatus } from '$lib/api/types';

let status = $state<EmbeddingsStatus>('unreachable');
let provider = $state('ollama');
let model = $state('nomic-embed-text');
let checking = $state(false);
let loaded = $state(false);
let inflight: Promise<void> | null = null;

export function getEmbeddingsState() {
	return {
		get status() {
			return status;
		},
		get provider() {
			return provider;
		},
		get model() {
			return model;
		},
		get checking() {
			return checking;
		},
		get loaded() {
			return loaded;
		}
	};
}

export function refreshEmbeddingsStatus(): Promise<void> {
	if (inflight) return inflight;
	checking = true;
	inflight = getEmbeddingsStatus()
		.then((res) => {
			status = res.status;
			provider = res.provider;
			model = res.model;
		})
		.catch(() => {
			status = 'unreachable';
		})
		.finally(() => {
			loaded = true;
			checking = false;
			inflight = null;
		});
	return inflight;
}

// Revalida quando a janela volta a ter foco (ex.: depois de instalar o Ollama), sem polling.
export function watchEmbeddingsStatus(): () => void {
	void refreshEmbeddingsStatus();
	const onFocus = () => void refreshEmbeddingsStatus();
	window.addEventListener('focus', onFocus);
	return () => window.removeEventListener('focus', onFocus);
}
