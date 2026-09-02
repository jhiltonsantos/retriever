import { getApiBaseUrl } from './config';
import type { FastApiError, UploadResponse } from './types';

function parseErrorDetail(body: FastApiError): string {
	if (typeof body.detail === 'string') {
		return body.detail;
	}
	if (Array.isArray(body.detail) && body.detail.length > 0) {
		return body.detail.map((item) => item.msg).join('; ');
	}
	return 'Erro ao enviar o PDF.';
}

export async function uploadPdf(file: File): Promise<UploadResponse> {
	const formData = new FormData();
	formData.append('file', file);

	const response = await fetch(`${getApiBaseUrl()}/upload`, {
		method: 'POST',
		body: formData
	});

	if (!response.ok) {
		let message = `Falha no upload (${response.status}).`;
		try {
			const body = (await response.json()) as FastApiError;
			message = parseErrorDetail(body);
		} catch {
			// keep default message
		}
		throw new Error(message);
	}

	return (await response.json()) as UploadResponse;
}
