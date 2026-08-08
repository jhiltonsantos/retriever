import { loadChatSession, clearChatSession } from './storage';

export type ConversationSummary = {
	id: string;
	title: string;
	updatedAt: string;
	messageCount: number;
};

/**
 * Etapa 1 do F-REDESIGN: adaptador sobre a sessao unica em localStorage.
 * Na Etapa 2 isso chama a API real (multi-conversa em SQLite) sem que
 * SideNav/`/history` precisem mudar.
 */
export function listRecentConversations(): ConversationSummary[] {
	const session = loadChatSession();
	if (session.messages.length === 0) {
		return [];
	}

	const firstUserMessage = session.messages.find((message) => message.role === 'user');

	return [
		{
			id: 'current',
			title: firstUserMessage ? firstUserMessage.content.slice(0, 48) : 'Nova conversa',
			updatedAt: session.updatedAt,
			messageCount: session.messages.length
		}
	];
}

export function startNewConversation(): void {
	clearChatSession();
}
