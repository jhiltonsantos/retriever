import { getApiBaseUrl } from './config';
import type { DocumentsResponse, FastApiError, IngestTextResponse } from './types';

function parseErrorDetail(body: FastApiError): string {
	if (typeof body.detail === 'string') {
		return body.detail;
	}
	if (Array.isArray(body.detail) && body.detail.length > 0) {
		return body.detail.map((item) => item.msg).join('; ');
	}
	return 'Erro ao indexar o texto.';
}

export async function ingestText(title: string, text: string): Promise<IngestTextResponse> {
	const response = await fetch(`${getApiBaseUrl()}/ingest/text`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ title, text })
	});

	if (!response.ok) {
		let message = `Falha ao indexar o texto (${response.status}).`;
		try {
			const body = (await response.json()) as FastApiError;
			message = parseErrorDetail(body);
		} catch {
			// keep default message
		}
		throw new Error(message);
	}

	return (await response.json()) as IngestTextResponse;
}

export async function getDocuments(): Promise<DocumentsResponse> {
	const response = await fetch(`${getApiBaseUrl()}/documents`);
	if (!response.ok) {
		throw new Error(`Erro ao listar documentos (${response.status}).`);
	}
	return (await response.json()) as DocumentsResponse;
}
