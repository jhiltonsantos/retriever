import { getApiBaseUrl } from './config';
import type { AskHistoryMessage, AskRequest, AskResponse, FastApiError } from './types';

function parseErrorDetail(body: FastApiError): string {
	if (typeof body.detail === 'string') {
		return body.detail;
	}
	if (Array.isArray(body.detail) && body.detail.length > 0) {
		return body.detail.map((item) => item.msg).join('; ');
	}
	return 'Não foi possível obter uma resposta.';
}

export async function askQuestion(
	question: string,
	history: AskHistoryMessage[] = [],
	conversationId?: string
): Promise<AskResponse> {
	const body: AskRequest = { question, history, conversation_id: conversationId };
	const response = await fetch(`${getApiBaseUrl()}/ask`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body)
	});

	if (!response.ok) {
		let message = `Erro na API (${response.status}). Verifique se o backend está rodando.`;
		try {
			const errorBody = (await response.json()) as FastApiError;
			message = parseErrorDetail(errorBody);
		} catch {
			// keep default message
		}
		throw new Error(message);
	}

	const data = (await response.json()) as AskResponse;
	return data;
}
