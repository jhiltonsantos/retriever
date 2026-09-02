import type { ConversationSummary } from '$lib/api/types';
import { listConversations as apiListConversations } from '$lib/api/conversations';

export type { ConversationSummary };

// Reactive store — components import this and get live data
let conversationsCache = $state<ConversationSummary[]>([]);
let loaded = $state(false);

export async function loadConversations(): Promise<ConversationSummary[]> {
	try {
		conversationsCache = await apiListConversations();
		loaded = true;
	} catch {
		conversationsCache = [];
	}
	return conversationsCache;
}

export function listRecentConversations(): ConversationSummary[] {
	return conversationsCache.slice(0, 5);
}

export function getAllConversations(): ConversationSummary[] {
	return conversationsCache;
}

export function invalidateConversations(): void {
	loaded = false;
}

export function isLoaded(): boolean {
	return loaded;
}
