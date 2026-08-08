import { getApiBaseUrl } from './config';
import type { MaterialsListResponse } from './types';

export async function listMaterials(): Promise<MaterialsListResponse> {
	const response = await fetch(`${getApiBaseUrl()}/materials`);
	if (!response.ok) throw new Error(`Erro ao listar materiais (${response.status}).`);
	return (await response.json()) as MaterialsListResponse;
}

export async function deleteMaterial(id: string): Promise<void> {
	const response = await fetch(`${getApiBaseUrl()}/materials/${id}`, { method: 'DELETE' });
	if (!response.ok) throw new Error(`Erro ao excluir material (${response.status}).`);
}
