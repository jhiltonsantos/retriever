import { getApiBaseUrl } from './config';
import type { EmbeddingsStatusResponse } from './types';

export async function getEmbeddingsStatus(): Promise<EmbeddingsStatusResponse> {
	const response = await fetch(`${getApiBaseUrl()}/settings/embeddings`);
	if (!response.ok) {
		throw new Error(`Erro ao verificar os embeddings (${response.status}).`);
	}
	return (await response.json()) as EmbeddingsStatusResponse;
}
