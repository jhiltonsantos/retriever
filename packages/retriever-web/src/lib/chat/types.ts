import type { AskAgentStep, AskSource } from '$lib/api/types';

export type ChatRole = 'user' | 'assistant';

export type ChatMessage = {
	id: string;
	role: ChatRole;
	content: string;
	createdAt: string;
	sources?: AskSource[];
	agentSteps?: AskAgentStep[];
};

export type ChatSession = {
	messages: ChatMessage[];
	updatedAt: string;
};

export function createChatMessage(
	role: ChatRole,
	content: string,
	extras?: { sources?: AskSource[]; agentSteps?: AskAgentStep[] }
): ChatMessage {
	return {
		id: crypto.randomUUID(),
		role,
		content,
		createdAt: new Date().toISOString(),
		...(extras?.sources?.length ? { sources: extras.sources } : {}),
		...(extras?.agentSteps?.length ? { agentSteps: extras.agentSteps } : {})
	};
}

export function emptyChatSession(): ChatSession {
	return {
		messages: [],
		updatedAt: new Date().toISOString()
	};
}
