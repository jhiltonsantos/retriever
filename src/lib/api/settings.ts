import { getApiBaseUrl } from './config';
import type { FastApiError } from './types';
import type {
	LlmModelsResponse,
	LlmProviderId,
	LlmSettings,
	TestConnectionResult,
	UpdateLlmSettingsPayload
} from '$lib/settings/types';

function parseErrorDetail(body: FastApiError): string {
	if (typeof body.detail === 'string') {
		return body.detail;
	}
	if (Array.isArray(body.detail) && body.detail.length > 0) {
		return body.detail.map((item) => item.msg).join('; ');
	}
	return 'Não foi possível completar a operação.';
}

async function parseJsonOrThrow<T>(response: Response, fallback: string): Promise<T> {
	if (!response.ok) {
		let message = `${fallback} (${response.status}).`;
		try {
			const body = (await response.json()) as FastApiError;
			message = parseErrorDetail(body);
		} catch {
			// keep default message
		}
		throw new Error(message);
	}
	return (await response.json()) as T;
}

export async function getLlmSettings(): Promise<LlmSettings> {
	const response = await fetch(`${getApiBaseUrl()}/settings/llm`);
	return parseJsonOrThrow<LlmSettings>(response, 'Erro ao carregar as configurações');
}

export async function updateLlmSettings(payload: UpdateLlmSettingsPayload): Promise<LlmSettings> {
	const response = await fetch(`${getApiBaseUrl()}/settings/llm`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});
	return parseJsonOrThrow<LlmSettings>(response, 'Erro ao salvar as configurações');
}

export async function getLlmModels(provider?: LlmProviderId): Promise<LlmModelsResponse> {
	const query = provider ? `?provider=${encodeURIComponent(provider)}` : '';
	const response = await fetch(`${getApiBaseUrl()}/settings/llm/models${query}`);
	return parseJsonOrThrow<LlmModelsResponse>(response, 'Erro ao listar os modelos');
}

export async function testLlmConnection(
	payload: UpdateLlmSettingsPayload
): Promise<TestConnectionResult> {
	const response = await fetch(`${getApiBaseUrl()}/settings/llm/test`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});
	return parseJsonOrThrow<TestConnectionResult>(response, 'Erro ao testar a conexão');
}
