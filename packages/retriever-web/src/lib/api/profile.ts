import { getApiBaseUrl } from './config';
import type { UserProfile } from './types';

export async function getProfile(): Promise<UserProfile> {
	const response = await fetch(`${getApiBaseUrl()}/profile`);
	if (!response.ok) throw new Error(`Erro ao carregar perfil (${response.status}).`);
	return (await response.json()) as UserProfile;
}

export async function updateProfile(display_name: string | null): Promise<UserProfile> {
	const response = await fetch(`${getApiBaseUrl()}/profile`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ display_name })
	});
	if (!response.ok) throw new Error(`Erro ao atualizar perfil (${response.status}).`);
	return (await response.json()) as UserProfile;
}
