export type UploadResponse = {
	message: string;
	filename: string;
	chunks_indexed: number;
};

export type ChatHistoryRole = 'user' | 'assistant';

export type AskHistoryMessage = {
	role: ChatHistoryRole;
	content: string;
};

export type AskRequest = {
	question: string;
	history?: AskHistoryMessage[];
	conversation_id?: string;
};

export type AskSource = {
	source: string;
	type: 'pdf' | 'text';
	page: number | null;
	snippet: string;
};

export type AskAgentStep = {
	step: string;
	loop: number;
	detail: string;
};

export type AskResponse = {
	answer: string;
	sources?: AskSource[];
	agent_steps?: AskAgentStep[];
};

export type IngestTextResponse = {
	message: string;
	source: string;
	type: 'text';
	chunks_indexed: number;
};

export type DocumentInfo = {
	source: string;
	type: 'pdf' | 'text';
	chunks: number;
	ingested_at: string | null;
};

export type DocumentsResponse = {
	documents: DocumentInfo[];
};

export type FastApiError = {
	detail: string | { msg: string }[];
};

// --- Stage 2: Conversations ---
export type ConversationSummary = {
	id: string;
	title: string;
	created_at: string;
	updated_at: string;
	message_count: number;
};

export type ConversationsListResponse = {
	conversations: ConversationSummary[];
};

export type StoredMessage = {
	id: string;
	role: 'user' | 'assistant';
	content: string;
	sources?: AskSource[];
	agent_steps?: AskAgentStep[];
	created_at: string;
};

export type ConversationDetail = {
	id: string;
	title: string;
	created_at: string;
	updated_at: string;
	messages: StoredMessage[];
};

// --- Stage 2: Materials catalog ---
export type MaterialInfo = {
	id: string;
	source: string;
	type: 'pdf' | 'text';
	title: string | null;
	chunk_count: number;
	ingested_at: string;
};

export type MaterialsListResponse = {
	materials: MaterialInfo[];
};

// --- Stage 2: Profile ---
export type UserProfile = {
	id: number;
	display_name: string | null;
	created_at: string;
	updated_at: string;
};

// --- Stage 3: Materials graph ---
export type MaterialGraphNode = {
	id: string;
	label: string;
	source: string;
	type: 'pdf' | 'text';
	chunk_count: number;
};

export type GraphEdge = {
	source: string;
	target: string;
	weight: number;
	strong: boolean;
};

export type MaterialsGraphResponse = {
	nodes: MaterialGraphNode[];
	edges: GraphEdge[];
};
