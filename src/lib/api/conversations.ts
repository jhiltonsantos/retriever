import { getApiBaseUrl } from './config';
import type {
	ConversationsListResponse,
	ConversationDetail,
	ConversationSummary,
	StoredMessage,
	FastApiError,
	AskSource,
	AskAgentStep
} from './types';

function parseErrorDetail(body: FastApiError): string {
	if (typeof body.detail === 'string') return body.detail;
	if (Array.isArray(body.detail) && body.detail.length > 0)
		return body.detail.map((item) => item.msg).join('; ');
	return 'Erro na operação.';
}

export async function listConversations(): Promise<ConversationSummary[]> {
	const response = await fetch(`${getApiBaseUrl()}/conversations`);
	if (!response.ok) throw new Error(`Erro ao listar conversas (${response.status}).`);
	const data = (await response.json()) as ConversationsListResponse;
	return data.conversations;
}

export async function getConversation(id: string): Promise<ConversationDetail> {
	const response = await fetch(`${getApiBaseUrl()}/conversations/${id}`);
	if (!response.ok) throw new Error(`Erro ao carregar conversa (${response.status}).`);
	return (await response.json()) as ConversationDetail;
}

export async function createConversation(title: string): Promise<ConversationSummary> {
	const response = await fetch(`${getApiBaseUrl()}/conversations`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ title })
	});
	if (!response.ok) throw new Error(`Erro ao criar conversa (${response.status}).`);
	return (await response.json()) as ConversationSummary;
}

export async function deleteConversation(id: string): Promise<void> {
	const response = await fetch(`${getApiBaseUrl()}/conversations/${id}`, { method: 'DELETE' });
	if (!response.ok) throw new Error(`Erro ao excluir conversa (${response.status}).`);
}

export async function addMessage(
	conversationId: string,
	role: 'user' | 'assistant',
	content: string,
	sources?: AskSource[],
	agentSteps?: AskAgentStep[]
): Promise<StoredMessage> {
	const response = await fetch(`${getApiBaseUrl()}/conversations/${conversationId}/messages`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ role, content, sources, agent_steps: agentSteps })
	});
	if (!response.ok) throw new Error(`Erro ao salvar mensagem (${response.status}).`);
	return (await response.json()) as StoredMessage;
}

export async function updateConversationTitle(id: string, title: string): Promise<void> {
	const response = await fetch(`${getApiBaseUrl()}/conversations/${id}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ title })
	});
	if (!response.ok) throw new Error(`Erro ao atualizar conversa (${response.status}).`);
}
