export function getApiBaseUrl(): string {
	return import.meta.env.PUBLIC_API_URL ?? 'http://127.0.0.1:8000';
}
