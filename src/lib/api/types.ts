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
