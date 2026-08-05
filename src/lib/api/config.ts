export function getApiBaseUrl(): string {
	if (typeof window !== 'undefined' && window.retriever?.getApiUrl) {
		return window.retriever.getApiUrl();
	}
	return import.meta.env.PUBLIC_API_URL ?? 'http://127.0.0.1:8000';
}
