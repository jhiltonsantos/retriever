<div class="relative flex h-full min-h-0 flex-1 flex-col">
	<div
		class="mx-auto flex w-full max-w-[896px] min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-4 pb-40"
		bind:this={threadEl}
	>
		{#if messages.length === 0}
			<p class="m-auto max-w-80 text-center text-sm text-[var(--color-outline)]">
				Nenhuma mensagem ainda. Faça uma pergunta sobre os PDFs que você indexou.
			</p>
		{:else}
			{#each messages as message (message.id)}
				<ChatMessage {message} />
			{/each}
		{/if}

		{#if submitting}
			<div role="status" class="alert alert-info mx-auto w-full max-w-[896px] text-sm">
				<span class="loading loading-spinner loading-sm"></span>
				<span>Consultando ChromaDB e gerando resposta com Ollama…</span>
			</div>
		{/if}

		{#if error}
			<div role="alert" class="alert alert-error mx-auto w-full max-w-[896px] text-sm">
				<span>{error}</span>
			</div>
		{/if}
	</div>

	<ChatComposer bind:value={question} {submitting} onSubmit={handleSubmit} />
</div>

<script lang="ts">
	import { onMount } from 'svelte';
	import { askQuestion } from '$lib/api/ask';
	import {
		addMessage,
		createConversation,
		deleteConversation,
		getConversation
	} from '$lib/api/conversations';
	import type { AskHistoryMessage, AskResponse, StoredMessage } from '$lib/api/types';
	import { createChatMessage, type ChatMessage as ChatMessageType } from '$lib/chat/types';
	import { showConfirm } from '$lib/alerts.svelte';
	import ChatComposer from './ChatComposer.svelte';
	import ChatMessage from './ChatMessage.svelte';

	type Props = {
		initialQuestion?: string;
		conversationId?: string;
		onConversationCreated?: (id: string) => void;
	};

	let { initialQuestion, conversationId = $bindable(), onConversationCreated }: Props = $props();

	let submitting = $state(false);
	let question = $state('');
	let error = $state<string | null>(null);
	let messages = $state<ChatMessageType[]>([]);
	let threadEl = $state<HTMLElement | null>(null);
	let loadingConversation = $state(false);

	function fromStoredMessage(stored: StoredMessage): ChatMessageType {
		return {
			id: stored.id,
			role: stored.role,
			content: stored.content,
			createdAt: stored.created_at,
			sources: stored.sources,
			agentSteps: stored.agent_steps
		};
	}

	async function loadConversation(id: string) {
		loadingConversation = true;
		try {
			const detail = await getConversation(id);
			messages = detail.messages.map(fromStoredMessage);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar conversa.';
		} finally {
			loadingConversation = false;
		}
	}

	onMount(() => {
		if (initialQuestion && messages.length === 0) {
			question = initialQuestion;
			handleSubmit();
		}
	});

	$effect(() => {
		if (!threadEl || messages.length === 0) return;
		threadEl.scrollTop = threadEl.scrollHeight;
	});

	$effect(() => {
		if (conversationId) {
			loadConversation(conversationId);
		} else {
			messages = [];
			error = null;
		}
	});

	export async function clearHistory() {
		if (
			!(await showConfirm('Limpar todo o histórico desta conversa?', {
				confirmLabel: 'Limpar histórico',
				variant: 'error'
			}))
		) {
			return;
		}

		if (conversationId) {
			try {
				await deleteConversation(conversationId);
			} catch (err) {
				error = err instanceof Error ? err.message : 'Erro ao excluir conversa.';
				return;
			}
		}

		messages = [];
		error = null;
		conversationId = undefined;
	}

	function toHistory(current: ChatMessageType[]): AskHistoryMessage[] {
		return current.map(({ role, content }) => ({ role, content }));
	}

	async function ensureConversation(userContent: string): Promise<string> {
		if (conversationId) return conversationId;

		const title = userContent.slice(0, 48);
		try {
			const created = await createConversation(title);
			conversationId = created.id;
			onConversationCreated?.(created.id);
			return created.id;
		} catch (err) {
			throw err instanceof Error ? err : new Error('Erro ao criar conversa.');
		}
	}

	async function persistUserMessage(id: string, content: string): Promise<ChatMessageType> {
		const stored = await addMessage(id, 'user', content);
		return fromStoredMessage(stored);
	}

	async function persistAssistantMessage(
		id: string,
		response: AskResponse
	): Promise<ChatMessageType> {
		const stored = await addMessage(
			id,
			'assistant',
			response.answer,
			response.sources,
			response.agent_steps
		);
		return fromStoredMessage(stored);
	}

	async function handleSubmit() {
		const trimmed = question.trim();
		if (!trimmed || submitting || loadingConversation) return;

		submitting = true;
		error = null;

		try {
			const id = await ensureConversation(trimmed);

			const userMessage = await persistUserMessage(id, trimmed);
			messages = [...messages, userMessage];
			question = '';

			const response = await askQuestion(trimmed, toHistory(messages), id);
			const assistantMessage = await persistAssistantMessage(id, response);
			messages = [...messages, assistantMessage];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Não foi possível obter uma resposta.';
		} finally {
			submitting = false;
		}
	}
</script>
