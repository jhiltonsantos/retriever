import type { LlmProviderId } from './types';

// Rotulos de exibicao. A lista de provedores vem do backend (chaves de `providers`
// em GET /settings/llm); um id sem entrada aqui aparece com o proprio id.
export const PROVIDER_LABELS: Record<string, string> = {
	ollama: 'Ollama local',
	openrouter: 'OpenRouter',
	custom: 'Custom'
};

export function providerLabel(id: LlmProviderId): string {
	return PROVIDER_LABELS[id] ?? id;
}
