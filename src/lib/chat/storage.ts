import { emptyChatSession, type ChatSession } from './types';

const STORAGE_KEY = 'retriever:chat-history';

export function loadChatSession(): ChatSession {
	if (typeof window === 'undefined') {
		return emptyChatSession();
	}

	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		if (!raw) {
			return emptyChatSession();
		}

		const parsed = JSON.parse(raw) as ChatSession;
		if (!Array.isArray(parsed.messages)) {
			return emptyChatSession();
		}

		return parsed;
	} catch {
		return emptyChatSession();
	}
}

export function saveChatSession(session: ChatSession): void {
	if (typeof window === 'undefined') {
		return;
	}

	localStorage.setItem(
		STORAGE_KEY,
		JSON.stringify({
			...session,
			updatedAt: new Date().toISOString()
		})
	);
}

export function clearChatSession(): void {
	if (typeof window === 'undefined') {
		return;
	}

	localStorage.removeItem(STORAGE_KEY);
}
