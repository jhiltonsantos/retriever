// Ids vindos do backend (fonte unica: app/providers/registry.py).
export type LlmProviderId = string;

export type ProviderConfig = {
	model: string | null;
	base_url: string;
	api_key_masked: string | null;
	api_key_set: boolean;
};

export type LlmSettings = {
	active_provider: LlmProviderId;
	providers: Record<LlmProviderId, ProviderConfig>;
};

export type LlmModel = {
	id: string;
	label: string;
};

export type LlmModelsResponse = {
	provider: LlmProviderId;
	models: LlmModel[];
};

export type UpdateLlmSettingsPayload = {
	provider: LlmProviderId;
	model: string;
	base_url?: string | null;
	api_key?: string | null;
};

export type TestConnectionReason = 'network' | 'auth' | 'model_not_found' | 'quota' | null;

export type TestConnectionResult = {
	ok: boolean;
	reason: TestConnectionReason;
	message: string;
};
