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
	import type { AskHistoryMessage, AskResponse } from '$lib/api/types';
	import { clearChatSession, loadChatSession, saveChatSession } from '$lib/chat/storage';
	import { createChatMessage, type ChatMessage as ChatMessageType } from '$lib/chat/types';
	import { showConfirm } from '$lib/alerts.svelte';
	import ChatComposer from './ChatComposer.svelte';
	import ChatMessage from './ChatMessage.svelte';

	type Props = {
		initialQuestion?: string;
	};

	let { initialQuestion }: Props = $props();

	let submitting = $state(false);
	let question = $state('');
	let error = $state<string | null>(null);
	let messages = $state<ChatMessageType[]>([]);
	let threadEl = $state<HTMLElement | null>(null);

	onMount(() => {
		messages = loadChatSession().messages;

		if (initialQuestion && messages.length === 0) {
			question = initialQuestion;
			handleSubmit();
		}
	});

	$effect(() => {
		if (!threadEl || messages.length === 0) return;
		threadEl.scrollTop = threadEl.scrollHeight;
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
		messages = [];
		error = null;
		clearChatSession();
	}

	function persistMessages(next: ChatMessageType[]) {
		messages = next;
		saveChatSession({ messages: next, updatedAt: new Date().toISOString() });
	}

	function appendExchange(userContent: string, response: AskResponse) {
		persistMessages([
			...messages,
			createChatMessage('user', userContent),
			createChatMessage('assistant', response.answer, {
				sources: response.sources,
				agentSteps: response.agent_steps
			})
		]);
	}

	function toHistory(current: ChatMessageType[]): AskHistoryMessage[] {
		return current.map(({ role, content }) => ({ role, content }));
	}

	async function handleSubmit() {
		const trimmed = question.trim();
		if (!trimmed || submitting) return;

		submitting = true;
		error = null;

		try {
			const response = await askQuestion(trimmed, toHistory(messages));
			appendExchange(trimmed, response);
			question = '';
		} catch (err) {
			error = err instanceof Error ? err.message : 'Não foi possível obter uma resposta.';
		} finally {
			submitting = false;
		}
	}
</script>
